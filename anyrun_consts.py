# File: anyrun_consts.py
#
# Copyright (c) 2021 Splunk Inc.
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
#
#
# API Endpoints
ANYRUN_TEST_CONNECTIVITY_ENDPOINT = 'environment'
ANYRUN_DETONATE_ENDPOINT = 'analysis'
ANYRUN_GET_REPORT_ENDPOINT = 'analysis/{taskid}'

# Messages
ANYRUN_ERR_CODE_MSG = "Error code unavailable"
ANYRUN_ERR_MSG_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters"
ANYRUN_PARSE_ERR_MSG = "Unable to parse the error message. Please check the asset configuration and|or action parameters"
ANYRUN_ERR_UNABLE_TO_FETCH_FILE = "Unable to fetch the {key} file"
ANYRUN_ERR_INVALID_PARAM = "Parameter {name} is invalid. Please check action parameters documentation"

# Constants relating to 'validate_integer'
VALID_INT_MSG = "Please provide a valid integer value in the '{param}' parameter"
NON_NEG_NON_ZERO_INT_MSG = "Please provide a valid non-zero positive integer value in '{param}' parameter"
NON_NEG_INT_MSG = "Please provide a valid non-negative integer value in the '{param}' parameter"
