**** Settings ***
Library     ../../api_interface/addons_service.py
Library     DateTime
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{text_data_uae}                       serviceProviderId=62a1a6954d402c22610b072c   addOnChargeType=FUEL_CHARGE
&{text_data_ksa}                       serviceProviderId=5f688042012d744e48ed7e89   addOnChargeType=FUEL_CHARGE
@{active_within_deadline_uae}          within_deadline                               active          uae
@{active_beyond_deadline_uae}          beyond_deadline                               active          uae
@{force_return_within_deadline_uae}    within_deadline                               force_return    uae
@{force_return_beyond_deadline_uae}    beyond_deadline                               force_return    uae
@{completed_within_deadline_uae}       within_deadline                               completed       uae
@{completed_beyond_deadline_uae}       beyond_deadline                               completed       uae
@{active_within_deadline_ksa}          within_deadline                               active          ksa
@{active_beyond_deadline_ksa}          beyond_deadline                               active          ksa
@{force_return_within_deadline_ksa}    within_deadline                               force_return    ksa
@{force_return_beyond_deadline_ksa}    beyond_deadline                               force_return    ksa
@{completed_within_deadline_ksa}       within_deadline                               completed       ksa
@{completed_beyond_deadline_ksa}       beyond_deadline                               completed       ksa

*** Test Cases ***
Upload Fuel Charges 1 Valid Date, Active Booking, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${active_within_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

# rule is abandoned for now
Upload Fuel Charges 2 Beyond Deadline, Active Booking, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${active_beyond_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    PENDING 

Upload Fuel Charges 3 Valid Date, Force Return, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${force_return_within_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING


Upload Fuel Charges 4 Beyond Deadline, Force Return, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${force_return_beyond_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    DELAYED

Upload Fuel Charges 5 Valid Date, Completed, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${completed_within_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

Upload Fuel Charges 6 Beyond Deadline, Completed, UAE
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_uae}    ${True}    ${completed_beyond_deadline_uae}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    DELAYED

Upload Fuel Charges 7 Valid Date, Active Booking, ksa
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${active_within_deadline_ksa}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

# Upload Fuel Charges 8 Beyond Deadline, Active Booking, ksa
#     [Tags]             URL Cases
#     ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${active_beyond_deadline_ksa}
#     Should Be Equal    ${value1}                        ${200}
#     Should Be Equal    ${value2}                        OK
#     Should Be Equal    ${value3}[0][data][0][status]    DELAYED

# Upload Fuel Charges 9 Valid Date, Force Return, ksa
#     [Tags]             URL Cases
#     ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${force_return_within_deadline_ksa}
#     Should Be Equal    ${value1}                        ${200}
#     Should Be Equal    ${value2}                        OK
#     Log                ${value3}
#     Should Be Equal    ${value3}[0][data][0][status]    PENDING


# Upload Fuel Charges 10 Beyond Deadline, Force Return, ksa
#     [Tags]             URL Cases
#     ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${force_return_beyond_deadline_ksa}
#     Should Be Equal    ${value1}                        ${200}
#     Should Be Equal    ${value2}                        OK
#     Should Be Equal    ${value3}[0][data][0][status]    DELAYED

Upload Fuel Charges 11 Valid Date, Completed, ksa
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${completed_within_deadline_ksa}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Log                ${value3}
    Should Be Equal    ${value3}[0][data][0][status]    PENDING

Upload Fuel Charges 12 Beyond Deadline, Completed, ksa
    [Tags]             URL Cases
    ${value1}          ${value2}                        @{value3}=    Upload Add On Charges Csv    ${text_data_ksa}    ${True}    ${completed_beyond_deadline_ksa}
    Should Be Equal    ${value1}                        ${200}
    Should Be Equal    ${value2}                        OK
    Should Be Equal    ${value3}[0][data][0][status]    DELAYED