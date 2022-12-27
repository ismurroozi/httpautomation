**** Settings ***
Library     ../../api_interface/addons_service.py
Library     DateTime
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{text_data_uae}                       serviceProviderId=62a1a6954d402c22610b072c
@{active_within_deadline}          within_deadline                               active
@{active_beyond_deadline}          beyond_deadline                               active
@{force_return_within_deadline}    within_deadline                               force_return
@{force_return_beyond_deadline}    beyond_deadline                               force_return
@{completed_within_deadline}       within_deadline                               completed
@{completed_beyond_deadline}       beyond_deadline                               completed

*** Test Cases ***
Upload Salik Fine 1 Valid Date, Active Booking
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${active_within_deadline}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

Upload Salik Fine 2 Beyond Deadline, Active Booking
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${active_beyond_deadline}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    DELAYED

Upload Salik Fine 3 Missing Service Provider, Active Booking
    [Tags]             URL Cases
    ${value1}          ${value2}                @{value3}=                       Upload Salik Fine Csv    ${EMPTY}    ${True}    ${active_within_deadline}
    Should Be Equal    ${value1}                ${400}
    Should Be Equal    ${value2}                Bad Request
    Should Be Equal    ${value3}[0][message]    serviceProviderId is required
Upload Salik Fine 4 Valid Date, Force Return
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${force_return_within_deadline}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

Upload Salik Fine 5 Beyond Deadline, Force Return
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${force_return_beyond_deadline}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    DELAYED

Upload Salik Fine 6 Valid Date, Completed
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${completed_within_deadline}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

# Upload Salik Fine 7 Beyond Deadline, Completed
#     [Tags]             URL Cases
#     ${value1}          ${value2}                        @{value3}=    Upload Salik Fine Csv    ${text_data_uae}    ${True}    ${completed_beyond_deadline}
#     Should Be Equal    ${value1}                        ${200}
#     Should Be Equal    ${value2}                        OK
#     Should Be Equal    ${value3}[0][data][0][status]    DELAYED