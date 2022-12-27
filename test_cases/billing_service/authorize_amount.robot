**** Settings ***
Library     ../../api_interface/billing_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{invalid_reserveBookingId}      reserveBookingId=121212121212121212121212
&{empty_userdata}           userData={}
&{empty_captureTransactionId}    captureTransactionId=None
&{empty_returningMetadata}       returningMetadata={}

*** Test Cases ***
Add Card 1 Booking Data Filled
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    ${EMPTY}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 2 Booking Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    invalid_card    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 3 Booking Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    invalid_cvv    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 4 Booking empty sourceid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    empty_sourceid    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 5 Booking invalid bookingid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    ${invalid_reserveBookingId}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 6 Booking empty user data
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Booking    Booking    ${empty_userdata}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 7 Invoice Data Filled
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    ${EMPTY}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 8 Invoice Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    invalid_card    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 9 Invoice Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    invalid_cvv    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 10 Invoice empty sourceid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    empty_sourceid    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 11 Invoice invalid bookingid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    ${invalid_reserveBookingId}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 12 Invoice empty user data
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Invoice    Invoice    ${empty_userdata}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 13 Return Data Filled
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    ${EMPTY}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 14 Return Invalid Card
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    invalid_card    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 15 Return Invalid CVV
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    invalid_cvv    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 16 Return empty sourceid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    empty_sourceid    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 17 Return invalid bookingid
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    ${invalid_reserveBookingId}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/

Add Card 18 Return empty user data
    [Tags]             URL Cases
    ${value1}          ${value2}                    @{value3}=                                      Authorize Amount    Return    Return    ${empty_userdata}    $(True)    $(True)
    Should Be Equal    ${value1}                    ${200}
    Should Be Equal    ${value2}                    OK
    Should Contain     ${value3}[0][redirectUrl]    https://3ds2-sandbox.ckotech.co/interceptor/