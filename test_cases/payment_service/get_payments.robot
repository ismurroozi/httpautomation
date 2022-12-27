**** Settings ***
Library    ../../api_interface/payment_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Test Cases ***
Get payments test case 1
    [Tags]             smoke
    ${value1}          ${value2}           @{value3}=                              Get Payments    ${tabby_channel}    ${tabby_id}
    Should Be Equal    ${value1}           ${200}
    Should Be Empty    ${value2}
    Should Be Equal    ${value3}[0][id]    a9de1573-04a3-4b27-8d28-82094d81fd3b

Get payments test case 2
    [Tags]             smoke
    ${value1}          ${value2}              @{value3}=    Get Payments    ${EMPTY}    ${EMPTY}
    Should Be Equal    ${value1}              ${404}
    Should Be Empty    ${value2}
    Should Be Equal    ${value3}[0][error]    Not Found