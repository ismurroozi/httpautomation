**** Settings ***
Library     ../../api_interface/billing_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{invalid_cvv}               cvv=505
&{expired_card}              expiryMonth=11                  expiryYear=12
&{card_non_3ds}             cardNumber=345678901234564  cvv=1051


*** Test Cases ***
Add Card 1 3DS
    [Tags]             HIGH
    ${status}          ${reason}                                @{responsedata}                                 ${redirect_link_status}=    Add Card    ${EMPTY}    ${True}
    Should Be Equal    ${status}                                ${200}
    Should Be Equal    ${reason}                                OK
    Should Contain     ${responsedata}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/
    Should Be Equal    ${redirect_link_status}                  ${200}

Add Card 2 Non 3DS
    [Tags]             HIGH
    ${status}          ${reason}                                @{responsedata}                                 ${redirect_link_status}=    Add Card    ${card_non_3ds}    ${True}
    Should Be Equal    ${status}                                ${200}
    Should Be Equal    ${reason}                                OK
    Should Contain     ${responsedata}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/
    Should Be Equal    ${redirect_link_status}                  ${200}

Add Card 3 Mismatch Card Number and CVV
    [Tags]             HIGH
    ${status}          ${reason}                  @{responsedata}    ${redirect_link_status}=    Add Card    ${invalid_cvv}    ${True}
    Should Be Equal    ${status}                  ${200}
    Should Be Equal    ${reason}                  OK
    Should Be Equal    ${redirect_link_status}    ${200}

Add Card 4 Expired Card
    [Tags]             HIGH
    ${status}          ${reason}    @{responsedata}    ${redirect_link_status}=    Add Card    ${expired_card}    ${True}
    Should Be Equal    ${status}    ${400}
    Should Be Equal    ${reason}    Bad Request