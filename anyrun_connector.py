# File: anyrun_connector.py
#
# Copyright (c) 2021-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

# Python 3 Compatibility imports

# Phantom App imports
import phantom.app as phantom
import phantom.rules as ph_rules
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector


try:
    from urllib.parse import unquote
except:
    from urllib import unquote

import json

import requests
from bs4 import BeautifulSoup

from anyrun_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AnyrunConnector(BaseConnector):
    def __init__(self):
        # Call the BaseConnectors init first
        super().__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        self._base_url = None

    def _get_error_message_from_exception(self, e):
        """This method is used to get appropriate error messages from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = ANYRUN_ERR_CODE_MSG
        error_msg = ANYRUN_ERR_MSG_UNAVAILABLE
        try:
            if e.args:
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except:
            pass

        return f"Error Code: {error_code}. Error Message: {error_msg}"

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        """
        Validate an integer.

        :param action_result: Action result or BaseConnector object
        :param parameter: input parameter
        :param key: input parameter message key
        :allow_zero: whether zero should be considered as valid value or not
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS, integer value of the parameter or None in case of failure
        """
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(phantom.APP_ERROR, VALID_INT_MSG.format(param=key)), None

                parameter = int(parameter)
            except:
                return action_result.set_status(phantom.APP_ERROR, VALID_INT_MSG.format(param=key)), None

            if parameter < 0:
                return action_result.set_status(phantom.APP_ERROR, NON_NEG_INT_MSG.format(param=key)), None
            if not allow_zero and parameter == 0:
                return action_result.set_status(phantom.APP_ERROR, NON_NEG_NON_ZERO_INT_MSG.format(param=key)), None

        return phantom.APP_SUCCESS, parameter

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(phantom.APP_ERROR, f"Status Code: {response.status_code}. Empty response, no information in header"), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = f"Status Code: {status_code}. Data from server:\n{unquote(error_text)}\n"

        message = message.replace("{", "{{").replace("}", "}}")
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Unable to parse JSON response. Error: {err}"), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        error_msg = resp_json.get("message", "Unknown error")

        # You should process the error returned in the json
        message = f"Error from server. Status Code: {r.status_code} Data from server: {error_msg}"

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {} Data from server: {}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"), resp_json)

        # Create a URL to connect to
        url = f"{self._base_url}{endpoint}"

        try:
            r = request_func(url, verify=config.get("verify_server_cert", False), **kwargs)
        except requests.exceptions.ConnectionError:
            err = f"Error connecting to server. Connection Refused from the Server for {url}"
            return RetVal(action_result.set_status(phantom.APP_ERROR, err), resp_json)
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Error Connecting to server. Details: {err}"), resp_json)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")
        # make rest call
        ret_val, response = self._make_rest_call(ANYRUN_TEST_CONNECTIVITY_ENDPOINT, action_result, params=None, headers=self._headers)

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_report(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        id = param["id"]

        # make rest call
        ret_val, response = self._make_rest_call(ANYRUN_GET_REPORT_ENDPOINT.format(taskid=id), action_result, params=None, headers=self._headers)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self.save_progress(f"Successfully fetched report for {id}")
        try:
            action_result.add_data(response["data"])
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Error occurred while processing response from server. {err}")

        return action_result.set_status(phantom.APP_SUCCESS, f"Successfully fetched report for {id}")

    def _handle_detonate_file(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        vault_id = param["vault_id"]

        try:
            success, message, vault_meta_info = ph_rules.vault_info(vault_id=vault_id)
            vault_meta_info = list(vault_meta_info)
            if not success or not vault_meta_info:
                error_msg = f" Error Details: {unquote(message)}" if message else ""
                return action_result.set_status(
                    phantom.APP_ERROR, "{}. {}".format(ANYRUN_ERR_UNABLE_TO_FETCH_FILE.format(key="vault meta info"), error_msg)
                )
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(
                phantom.APP_ERROR, "{}. {}".format(ANYRUN_ERR_UNABLE_TO_FETCH_FILE.format(key="vault meta info"), err)
            )

        try:
            # phantom vault file path
            file_path = vault_meta_info[0].get("path")
            if not file_path:
                return action_result.set_status(phantom.APP_ERROR, ANYRUN_ERR_UNABLE_TO_FETCH_FILE.format(key="path"))
        except:
            return action_result.set_status(phantom.APP_ERROR, ANYRUN_ERR_UNABLE_TO_FETCH_FILE.format(key="path"))

        self.save_progress(f"Detonating file {file_path}")

        data = {k: v for k, v in param.items() if k not in ["context", "vault_id"]}
        if "opt_timeout" in data:
            ret_val, data["opt_timeout"] = self._validate_integer(action_result, data["opt_timeout"], "opt_timeout")
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if "env_bitness" in data:
            ret_val, data["env_bitness"] = self._validate_integer(action_result, data["env_bitness"], "env_bitness")
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        files = [("file", open(file_path, "rb"))]

        # make rest call
        ret_val, response = self._make_rest_call(
            ANYRUN_DETONATE_ENDPOINT, action_result, method="post", data=data, files=files, headers=self._headers
        )

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self.save_progress("Successfully detonated file")
        try:
            action_result.add_data(response["data"])
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Error occurred while processing response from server. {err}")

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully detonated file")

    def _handle_detonate_url(self, param):
        self.save_progress(f"In action handler for: {self.get_action_identifier()}")
        action_result = self.add_action_result(ActionResult(dict(param)))

        obj_type = param["obj_type"]
        # Validating input params
        if obj_type not in ["url", "download"]:
            return action_result.set_status(phantom.APP_ERROR, ANYRUN_ERR_INVALID_PARAM.format(name="obj_type"))

        data = {k: v for k, v in param.items() if k not in ["context"]}
        if "opt_timeout" in data:
            ret_val, data["opt_timeout"] = self._validate_integer(action_result, data["opt_timeout"], "opt_timeout")
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        if "env_bitness" in data:
            ret_val, data["env_bitness"] = self._validate_integer(action_result, data["env_bitness"], "env_bitness")
            if phantom.is_fail(ret_val):
                return action_result.get_status()

        self.save_progress(f"Detonating URL ({obj_type})")
        # make rest call
        ret_val, response = self._make_rest_call(
            ANYRUN_DETONATE_ENDPOINT, action_result, method="post", data=data, files=[], headers=self._headers
        )

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self.save_progress(f"Successfully detonated URL ({obj_type})")
        try:
            action_result.add_data(response["data"])
        except Exception as e:
            err = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, f"Error occurred while processing response from server. {err}")

        return action_result.set_status(phantom.APP_SUCCESS, f"Successfully detonated URL ({obj_type})")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print(f"action_id: {self.get_action_identifier()}")

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "get_report":
            ret_val = self._handle_get_report(param)

        elif action_id == "detonate_file":
            ret_val = self._handle_detonate_file(param)

        elif action_id == "detonate_url":
            ret_val = self._handle_detonate_url(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        if not isinstance(self._state, dict):
            self.debug_print("Resetting the state file with the default format")
            self._state = {"app_version": self.get_app_json().get("app_version")}
            return self.set_status(phantom.APP_ERROR, STATE_FILE_CORRUPT_ERR)

        # get the asset config
        config = self.get_config()

        self._base_url = config["base_url"]
        self._api_key = config["api_key"]
        self._headers = {"Authorization": f"API-Key {self._api_key}"}
        # Security check on URL format
        if not self._base_url.endswith("/"):
            self._base_url += "/"

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = AnyrunConnector._get_phantom_base_url() + "/login"

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AnyrunConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)


if __name__ == "__main__":
    main()
