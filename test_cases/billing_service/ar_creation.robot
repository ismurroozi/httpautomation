**** Settings ***
Library     ../../api_interface/billing_service.py
Resource    ../../api_interface/utilities/common_resource.robot
Library     Collections

*** Variables ***
&{invalid_currency}          currency=XXX
&{incomplete_card_number}    cardNumber=121212
&{invalid_card_number}       cardNumber=1212121212121212
&{invalid_cvv}               cvv=1212121212121212
&{expired_card}              expiryMonth=1                  expiryYear=12
&{empty_user_data}           userData={}
&{madaCard}                  madaCard=true


*** Test Cases ***
Ar Creation For Booking 1 NPD Past, Invoice Unpaid, Invoice Not created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_PAST    INVOICE_UNPAID    ${False}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 2 NPD Past, Invoice Unpaid, Invoice created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_PAST    INVOICE_UNPAID    ${True}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}


Ar Creation For Booking 3 NPD Past, Invoice Paid, Invoice Not created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_PAST    INVOICE_PAID    ${False}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 4 NPD Past, Invoice Paid, Invoice created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_PAST    INVOICE_PAID    ${True}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 5 NPD Tomorrow
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_TOMORROW    INVOICE_PAID    ${False}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 6 NPD Future, Invoice Unpaid, Invoice Not created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_FUTURE    INVOICE_UNPAID    ${False}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 7 NPD Future, Invoice Unpaid, Invoice created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_FUTURE    INVOICE_UNPAID    ${True}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}


Ar Creation For Booking 8 NPD Future, Invoice Paid, Invoice Not created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_FUTURE    INVOICE_PAID    ${False}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}

Ar Creation For Booking 9 NPD Future, Invoice Paid, Invoice created before
    [Tags]                                URL Cases
    ${startdate}                          ${enddate}                          ${expected_last_startdate}    ${expected_last_enddate}    ${next_month_year}=    Ar Creation For Booking    NPD_FUTURE    INVOICE_PAID    ${True}
    List Should Not Contain Duplicates    ${startdate}
    List Should Not Contain Duplicates    ${enddate}
    ${startdate_size}=                    Get length                          ${startdate}
    ${startdate_index}=                   evaluate                            ${startdate_size} - ${1}
    ${enddate_size}=                      Get length                          ${enddate}
    ${enddate_index}=                     evaluate                            ${enddate_size} - ${1}
    Should Be Equal                       ${startdate}[${startdate_index}]    ${expected_last_startdate}
    Should Be Equal                       ${enddate}[${enddate_index}]        ${expected_last_enddate}
    Should Not Be Equal                   ${startdate}[${startdate_index}]    ${next_month_year}