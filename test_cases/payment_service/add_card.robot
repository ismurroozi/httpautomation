**** Settings ***
Library    ../../api_interface/payment_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{test_data}    currency=AED    cardNumber=abababababababab

*** Test Cases ***
Add Card 1 Reqs Data Filled
    [Tags]             URL Cases
    ${value1}          ${value2}           @{value3}=                              Add Card     ${checkout_channel}    ${EMPTY}    ${True}
    Should Be Equal    ${value1}              ${200}
    Should Be Equal    ${value3}[0][responseCode]       201
    Should Be Equal    ${value3}[0][responseSummary]    Instrument created successfully

