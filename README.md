[comment]: # "Auto-generated SOAR connector documentation"
# AnyRun

Publisher: Splunk Community  
Connector Version: 2\.0\.2  
Product Vendor: Any\.Run  
Product Name: Any\.Run  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.0\.0  

This App implements investigative and generic actions on Any\.Run, interactive malware hunting service

[comment]: # " File: readme.md"
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
    is requested to the end-user to please update their existing playbooks by re-inserting \|
    modifying \| deleting the corresponding action blocks or by providing appropriate values to
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
    update their existing playbooks by inserting \| modifying \| deleting the corresponding action
    blocks for this action on the earlier versions of the app.
    -   detonate url


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Any\.Run asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | Any\.Run base URL \(e\.g\. https\://myservice/\)
**api\_key** |  required  | password | Token used for API authentication

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[get report](#action-get-report) - Query for results of a detonation  
[detonate file](#action-detonate-file) - Run the file in the sandbox and returns the ID of created task  
[detonate url](#action-detonate-url) - Load a URL for analysis and returns the ID of created task  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get report'
Query for results of a detonation

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Detonation ID to get the report of | string |  `anyrun task id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.id | string |  `anyrun task id` 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.analysis\.scores\.verdict\.threatLevelText | string | 
action\_result\.data\.\*\.analysis\.scores\.verdict\.threatLevel | numeric | 
action\_result\.data\.\*\.analysis\.scores\.verdict\.score | numeric | 
action\_result\.data\.\*\.analysis\.content\.mainObject\.filename | string | 
action\_result\.data\.\*\.analysis\.content\.mainObject\.info\.file | string | 
action\_result\.data\.\*\.analysis\.content\.mainObject\.info\.mime | string | 
action\_result\.data\.\*\.analysis\.content\.mainObject\.hashes\.sha256 | string |  `hash`  `sha256` 
action\_result\.data\.\*\.analysis\.content\.mainObject\.hashes\.sha1 | string |  `hash`  `sha1` 
action\_result\.data\.\*\.analysis\.content\.mainObject\.hashes\.md5 | string |  `hash`  `md5` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'detonate file'
Run the file in the sandbox and returns the ID of created task

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault\_id** |  required  | Vault ID of the file to detonate | string |  `vault id` 
**env\_os** |  optional  | Operation System \(Default\: windows\) | string | 
**env\_bitness** |  optional  | Bitness of Operation System \(Default\: 32\) | numeric | 
**env\_version** |  optional  | Version of OS \(Default\: 7\) | string | 
**env\_type** |  optional  | Environment preset type \(Default\: complete\) | string | 
**opt\_network\_geo** |  optional  | Geo location option \(Default\: fastest\) | string | 
**opt\_timeout** |  optional  | Timeout option \(seconds\) \(Default\: 60\) \(Size range\: 10\-660\) | numeric | 
**opt\_privacy\_type** |  optional  | Privacy settings \(Default\: bylink\) | string | 
**obj\_ext\_startfolder** |  optional  | Start object from \(Default\: temp\) | string | 
**obj\_ext\_cmd** |  optional  | Optional command line \(Size range\: 2\-256\) | string | 
**obj\_ext\_elevateprompt** |  optional  | Encounter UAC prompts | boolean | 
**obj\_ext\_extension** |  optional  | Change extension to valid | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.env\_os | string | 
action\_result\.parameter\.env\_bitness | numeric | 
action\_result\.parameter\.env\_version | string | 
action\_result\.parameter\.env\_type | string | 
action\_result\.parameter\.opt\_network\_geo | string | 
action\_result\.parameter\.opt\_timeout | numeric | 
action\_result\.parameter\.opt\_privacy\_type | string | 
action\_result\.parameter\.obj\_ext\_startfolder | string | 
action\_result\.parameter\.obj\_ext\_cmd | string | 
action\_result\.parameter\.obj\_ext\_elevateprompt | boolean | 
action\_result\.parameter\.obj\_ext\_extension | boolean | 
action\_result\.data\.\*\.taskid | string |  `anyrun task id` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'detonate url'
Load a URL for analysis and returns the ID of created task

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**obj\_url** |  required  | URL to detonate \(Size range\: 5\-512\) | string |  `url` 
**obj\_type** |  required  | Type of new task \(Default\: url\) | string | 
**env\_os** |  optional  | Operation System \(Default\: windows\) | string | 
**env\_bitness** |  optional  | Bitness of Operation System \(Default\: 32\) | numeric | 
**env\_version** |  optional  | Version of OS \(Default\: 7\) | string | 
**env\_type** |  optional  | Environment preset type \(Default\: complete\) | string | 
**opt\_network\_geo** |  optional  | Geo location option \(Default\: fastest\) | string | 
**opt\_timeout** |  optional  | Timeout option \(seconds\) \(Default\: 60\) \(Size range\: 10\-660\) | numeric | 
**opt\_privacy\_type** |  optional  | Privacy settings \(Default\: bylink\) | string | 
**obj\_ext\_startfolder** |  optional  | Start object from \(Default\: temp\) | string | 
**obj\_ext\_cmd** |  optional  | Optional command line \(Size range\: 2\-256\) | string | 
**obj\_ext\_browser** |  optional  | Browser name \(Default\: Internet Explorer\) | string | 
**obj\_ext\_useragent** |  optional  | User agent \(Size range\: 2\-256\) | string | 
**obj\_ext\_elevateprompt** |  optional  | Encounter UAC prompts | boolean | 
**obj\_ext\_extension** |  optional  | Change extension to valid | boolean | 
**opt\_privacy\_hidesource** |  optional  | Option for hiding of source URL | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.obj\_url | string |  `url` 
action\_result\.parameter\.obj\_type | string | 
action\_result\.parameter\.env\_os | string | 
action\_result\.parameter\.env\_bitness | numeric | 
action\_result\.parameter\.env\_version | string | 
action\_result\.parameter\.env\_type | string | 
action\_result\.parameter\.opt\_network\_geo | string | 
action\_result\.parameter\.opt\_timeout | numeric | 
action\_result\.parameter\.opt\_privacy\_type | string | 
action\_result\.parameter\.obj\_ext\_startfolder | string | 
action\_result\.parameter\.obj\_ext\_cmd | string | 
action\_result\.parameter\.obj\_ext\_browser | string | 
action\_result\.parameter\.obj\_ext\_useragent | string | 
action\_result\.parameter\.obj\_ext\_elevateprompt | boolean | 
action\_result\.parameter\.obj\_ext\_extension | boolean | 
action\_result\.parameter\.opt\_privacy\_hidesource | boolean | 
action\_result\.data\.\*\.taskid | string |  `anyrun task id` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 