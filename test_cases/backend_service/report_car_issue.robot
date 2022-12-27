**** Settings ***
Library     ../../api_interface/backend_service.py
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
&{invalid_reserveBookingId}      bookingId=121212121212121212121212
&{unknown_issueType}      issueType=unknown
&{empty_issueNote}      issueNote=${EMPTY}
&{empty_issuePriority}      issuePriority=${EMPTY}
&{unknown_issuePriority}      issuePriority=UNKNOWN

*** Test Cases ***
Report Car Issue 1 Empty Struct
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${EMPTY}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request


Report Car Issue 2 Valid Bookingid
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${EMPTY}    ${True}
    Should Be Equal    ${value1}    ${200}
    Should Be Equal    ${value2}    OK
    Should Be Equal    ${value4}    ${1}
    Should Be Equal    ${value3}[0][requestId]    ${value5}[requestId] 

Report Car Issue 3 Invalid Bookingid
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${invalid_reserveBookingId}    ${True}
    Should Be Equal    ${value1}    ${404}
    Should Be Equal    ${value2}    Not Found

Report Car Issue 4 Empty Issue Type
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${invalid_reserveBookingId}    ${False}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Report Car Issue 5 Unknown Issue Type
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${unknown_issueType}    ${True}
    Should Be Equal    ${value1}    ${500}
    Should Be Equal    ${value2}    Internal Server Error

Report Car Issue 6 Empty Issue Note
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${empty_issueNote}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Report Car Issue 7 Empty Issue Priority
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${empty_issuePriority}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request

Report Car Issue 8 Unknown Issue Priority
    [Tags]             URL Cases
    ${value1}          ${value2}    @{value3}   ${value4}   ${value5}=     Report Car Issue    ${unknown_issuePriority}    ${True}
    Should Be Equal    ${value1}    ${400}
    Should Be Equal    ${value2}    Bad Request