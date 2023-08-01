[comment]: # " File: README.md"
[comment]: # ""
[comment]: # "  Copyright (c) 2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # "  "
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""
AnyRun app is compatible with Phantom **5.0.0+**

## Playbook Backward Compatibility

-   The below-mentioned action parameters have been added in the 'detonate file' action. Hence, it
    is requested to the end-user to please update their existing playbooks by re-inserting |
    modifying | deleting the corresponding action blocks or by providing appropriate values to
    these action parameters to ensure the correct functioning of the playbooks created on the
    earlier versions of the app.
    -   env_os
    -   env_bitness
    -   env_version
    -   env_type
    -   opt_network_geo
    -   opt_timeout
    -   opt_privacy_type
    -   obj_ext_startfolder
    -   obj_ext_cmd
    -   obj_ext_elevateprompt
    -   obj_ext_extension
-   The below-mentioned action has been added. Hence, it is requested to the end-user to please
    update their existing playbooks by inserting | modifying | deleting the corresponding action
    blocks for this action on the earlier versions of the app.
    -   detonate url
