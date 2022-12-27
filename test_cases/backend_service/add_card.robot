**** Settings ***
Library     ../../api_interface/backend_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{invalid_cvv}               cvv=505
&{expired_card}              expiryMonth=11                  expiryYear=12
&{card_non_3ds}             cardNumber=345678901234564  cvv=1051


*** Test Cases ***
Add Card 1 3DS
    [Tags]             HIGH
    ${value1}          ${value2}                          @{value3}=                                      Add Card    ${EMPTY}    ${True}
    Should Be Equal    ${value1}                          ${200}
    Should Be Equal    ${value2}                          OK
    Should Contain     ${value3}[0][data][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 2 Non 3DS
    [Tags]             HIGH
    ${value1}          ${value2}                          @{value3}=                                      Add Card    ${card_non_3ds}    ${True}
    Should Be Equal    ${value1}                          ${200}
    Should Be Equal    ${value2}                          OK
    Should Contain     ${value3}[0][data][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 3 Mismatch Card Number and CVV
    [Tags]             HIGH
    ${value1}          ${value2}    @{value3}=     Add Card    ${invalid_cvv}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK

Add Card 4 Expired Card
    [Tags]             HIGH
    ${value1}          ${value2}    @{value3}=     Add Card    ${expired_card}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request