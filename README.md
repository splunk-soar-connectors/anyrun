# AnyRun

Publisher: Splunk Community \
Connector Version: 2.0.3 \
Product Vendor: Any.Run \
Product Name: Any.Run \
Minimum Product Version: 5.0.0

This App implements investigative and generic actions on Any.Run, interactive malware hunting service

### Configuration variables

This table lists the configuration variables required to operate AnyRun. These variables are specified when configuring a Any.Run asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | required | string | Any.Run base URL (e.g. https://myservice/) |
**api_key** | required | password | Token used for API authentication |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[get report](#action-get-report) - Query for results of a detonation \
[detonate file](#action-detonate-file) - Run the file in the sandbox and returns the ID of created task \
[detonate url](#action-detonate-url) - Load a URL for analysis and returns the ID of created task

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'get report'

Query for results of a detonation

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | Detonation ID to get the report of | string | `anyrun task id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.id | string | `anyrun task id` | 0cf223f2-530e-4a50-b68f-563045268648 |
action_result.data.\*.status | string | | |
action_result.data.\*.analysis.scores.verdict.threatLevelText | string | | |
action_result.data.\*.analysis.scores.verdict.threatLevel | numeric | | |
action_result.data.\*.analysis.scores.verdict.score | numeric | | |
action_result.data.\*.analysis.content.mainObject.filename | string | | |
action_result.data.\*.analysis.content.mainObject.info.file | string | | |
action_result.data.\*.analysis.content.mainObject.info.mime | string | | |
action_result.data.\*.analysis.content.mainObject.hashes.sha256 | string | `hash` `sha256` | |
action_result.data.\*.analysis.content.mainObject.hashes.sha1 | string | `hash` `sha1` | |
action_result.data.\*.analysis.content.mainObject.hashes.md5 | string | `hash` `md5` | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'detonate file'

Run the file in the sandbox and returns the ID of created task

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** | required | Vault ID of the file to detonate | string | `vault id` |
**env_os** | optional | Operation System (Default: windows) | string | |
**env_bitness** | optional | Bitness of Operation System (Default: 32) | numeric | |
**env_version** | optional | Version of OS (Default: 7) | string | |
**env_type** | optional | Environment preset type (Default: complete) | string | |
**opt_network_geo** | optional | Geo location option (Default: fastest) | string | |
**opt_timeout** | optional | Timeout option (seconds) (Default: 60) (Size range: 10-660) | numeric | |
**opt_privacy_type** | optional | Privacy settings (Default: bylink) | string | |
**obj_ext_startfolder** | optional | Start object from (Default: temp) | string | |
**obj_ext_cmd** | optional | Optional command line (Size range: 2-256) | string | |
**obj_ext_elevateprompt** | optional | Encounter UAC prompts | boolean | |
**obj_ext_extension** | optional | Change extension to valid | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.vault_id | string | `vault id` | |
action_result.parameter.env_os | string | | windows |
action_result.parameter.env_bitness | numeric | | 32 64 |
action_result.parameter.env_version | string | | vista 7 8.1 10 |
action_result.parameter.env_type | string | | clean office complete |
action_result.parameter.opt_network_geo | string | | fastest AU BR DE CH FR KR US RU GB IT |
action_result.parameter.opt_timeout | numeric | | 60 |
action_result.parameter.opt_privacy_type | string | | public bylink owner |
action_result.parameter.obj_ext_startfolder | string | | desktop home downloads appdata temp windows root |
action_result.parameter.obj_ext_cmd | string | | |
action_result.parameter.obj_ext_elevateprompt | boolean | | True False |
action_result.parameter.obj_ext_extension | boolean | | True False |
action_result.data.\*.taskid | string | `anyrun task id` | 0cf223f2-530e-4a50-b68f-563045268648 |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'detonate url'

Load a URL for analysis and returns the ID of created task

Type: **generic** \
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**obj_url** | required | URL to detonate (Size range: 5-512) | string | `url` |
**obj_type** | required | Type of new task (Default: url) | string | |
**env_os** | optional | Operation System (Default: windows) | string | |
**env_bitness** | optional | Bitness of Operation System (Default: 32) | numeric | |
**env_version** | optional | Version of OS (Default: 7) | string | |
**env_type** | optional | Environment preset type (Default: complete) | string | |
**opt_network_geo** | optional | Geo location option (Default: fastest) | string | |
**opt_timeout** | optional | Timeout option (seconds) (Default: 60) (Size range: 10-660) | numeric | |
**opt_privacy_type** | optional | Privacy settings (Default: bylink) | string | |
**obj_ext_startfolder** | optional | Start object from (Default: temp) | string | |
**obj_ext_cmd** | optional | Optional command line (Size range: 2-256) | string | |
**obj_ext_browser** | optional | Browser name (Default: Internet Explorer) | string | |
**obj_ext_useragent** | optional | User agent (Size range: 2-256) | string | |
**obj_ext_elevateprompt** | optional | Encounter UAC prompts | boolean | |
**obj_ext_extension** | optional | Change extension to valid | boolean | |
**opt_privacy_hidesource** | optional | Option for hiding of source URL | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.obj_url | string | `url` | |
action_result.parameter.obj_type | string | | url download |
action_result.parameter.env_os | string | | windows |
action_result.parameter.env_bitness | numeric | | 32 64 |
action_result.parameter.env_version | string | | vista 7 8.1 10 |
action_result.parameter.env_type | string | | clean office complete |
action_result.parameter.opt_network_geo | string | | fastest AU BR DE CH FR KR US RU GB IT |
action_result.parameter.opt_timeout | numeric | | 60 |
action_result.parameter.opt_privacy_type | string | | public bylink owner |
action_result.parameter.obj_ext_startfolder | string | | desktop home downloads appdata temp windows root |
action_result.parameter.obj_ext_cmd | string | | |
action_result.parameter.obj_ext_browser | string | | Google Chrome Mozilla Firefox Opera Internet Explorer |
action_result.parameter.obj_ext_useragent | string | | |
action_result.parameter.obj_ext_elevateprompt | boolean | | True False |
action_result.parameter.obj_ext_extension | boolean | | True False |
action_result.parameter.opt_privacy_hidesource | boolean | | True False |
action_result.data.\*.taskid | string | `anyrun task id` | 0cf223f2-530e-4a50-b68f-563045268648 |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
