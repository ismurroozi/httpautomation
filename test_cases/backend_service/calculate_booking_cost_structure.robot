**** Settings ***
Library     ../../api_interface/booking_service.py
Library     DateTime
Resource    ../../api_interface/utilities/common_resource.robot

*** Variables ***
@{valid_data_noaddon}                      vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    bookingPeriod=1          
@{invalid_vehicle_id}                      vehicleId=111111111111111111111111    selectedMileage=3000    bookingPeriod=1
@{valid_data_mileage}                      vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    upgradedMileage=true     bookingPeriod=1
@{valid_data_mileage_insurance}            vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    upgradedMileage=true     bookingPeriod=1        fullInsurance=true
@{valid_data_mileage_insurance_driver}     vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    upgradedMileage=true     bookingPeriod=1        fullInsurance=true     numOfAdditionalDriver=1
@{valid_data_noaddon_promocode}            vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    upgradedMileage=false    bookingPeriod=1        fullInsurance=false    numOfAdditionalDriver=0    promoCode=ROOZITEST
@{valid_data_noaddon_promocode_6months}    vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    bookingPeriod=6          promoCode=ROOZITEST
@{default_swap}                            vehicleId=5c7e7ec18cb75c93fc6bec1d    selectedMileage=3000    bookingPeriod=1          isSwap=true
@{s2o_swap}                                vehicleId=61e5628825cb8971e93ba12f    selectedMileage=3000    bookingPeriod=1          isSwap=true


*** Test Cases ***
Calculate Booking Cost Structure 1 Valid Data, No Swap
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                       ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_noaddon}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 2 Invalid vehicleId, No Swap
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}                    ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${invalid_vehicle_id}    ${EMPTY}    ${EMPTY}
    Should Be Equal    ${code}                    ${400}
    Should Be Equal    ${status}                  Bad Request
    Should Be Equal    ${respdata}[0][message]    Vehicle / Pricing not found

Calculate Booking Cost Structure 3 Valid Data, No Swap, extra mileage
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_mileage}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][extraMileagePrice] + ${0}
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 4 Valid Data, No Swap, extra mileage, insurance
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                                                                            ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_mileage_insurance}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][extraMileagePrice] + ${vehicle_data_db}[0][pricingData][fullInsurance]
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 5 Valid Data, No Swap, extra mileage, insurance, driver
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                                                                                                                                  ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_mileage_insurance_driver}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][extraMileagePrice] + ${vehicle_data_db}[0][pricingData][fullInsurance] + ${vehicle_data_db}[0][pricingData][secondaryDriver]
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 6 Valid Data, No Swap, promocode
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                                                        ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_noaddon_promocode}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                          ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] - ${promo_data_db}[0][reward][0][value]
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 7 Valid Data, No Swap, promocode, 6 months
    [Tags]                URL Cases
    ${code}               ${status}                                         @{respdata}                                                                                        ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_noaddon_promocode_6months}    ${EMPTY}    ${EMPTY}
    Should Be Equal       ${code}                                           ${200}
    Should Be Equal       ${status}                                         OK
    ${correct_monthly}    evaluate                                          ${vehicle_data_db}[0][pricingData][sixMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                          ${vehicle_data_db}[0][pricingData][sixMonth][basePrice] - ${promo_data_db}[0][reward][0][value]
    Should Be Equal       ${respdata}[0][data][monthlyFee]                  ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                      ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                  ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]        ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]    ${0}

Calculate Booking Cost Structure 8 Invalid swap
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}                        ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAPPED_CAR    ${EMPTY}
    Should Be Equal    ${code}                    ${406}
    Should Be Equal    ${status}                  Not Acceptable
    Should Contain     ${respdata}[0][message]    is already created as swapped. 

Calculate Booking Cost Structure 9 Invalid swap, no swap data
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}                     ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    ${EMPTY}    ${EMPTY}
    Should Be Equal    ${code}                    ${400}
    Should Be Equal    ${status}                  Bad Request
    Should Be Equal    ${respdata}[0][message]    Swapped Booking Id Not Found

Calculate Booking Cost Structure 10 Invalid swap, booking id not found
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    NOT_FOUND_BOOKING    ${EMPTY}
    Should Be Equal    ${code}                    ${404}
    Should Be Equal    ${status}                  Not Found
    Should Be Equal    ${respdata}[0][message]    Booking data not found

Calculate Booking Cost Structure 11 Invalid swap, first month booking
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}                            ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    FIRST_MONTH_BOOKING    ${EMPTY}
    Should Be Equal    ${code}                    ${422}
    Should Be Equal    ${status}                  Unprocessable Entity
    Should Be Equal    ${respdata}[0][message]    Swap date is within the first month

Calculate Booking Cost Structure 12 Invalid swap, Remaining days is greater than 31
    [Tags]             URL Cases
    ${code}            ${status}                  @{respdata}                          ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_40DAYS_BEFORE_NEXTPAYMENTDATE    ${EMPTY}
    Should Be Equal    ${code}                    ${406}
    Should Be Equal    ${status}                  Not Acceptable
    Should Be Equal    ${respdata}[0][message]    Remaining days is greater than 31

Calculate Booking Cost Structure 13 Valid swap, swap after recurring paid, paynow+, credit_amount 0
    [Tags]                URL Cases
    ${code}               ${status}                                                @{respdata}                                                                                                                                                                                                                                                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_AFTER_RECURRING_PAYNOW+    ${EMPTY}
    Should Be Equal       ${code}                                                  ${200}
    Should Be Equal       ${status}                                                OK
    ${correct_monthly}    evaluate                                                 ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                                 math.floor(${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal       ${respdata}[0][data][monthlyFee]                         ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                             ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                         ${0}
    Should Be Equal       ${respdata}[0][data][creditAmount]                       ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][extraDayCost]    ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][swapFee]         ${50}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]               ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]           ${0}

Calculate Booking Cost Structure 14 Valid swap, swap after recurring paid, paynow 0, credit_amount +
    [Tags]                      URL Cases
    ${code}                     ${status}                                                @{respdata}                                                                                                                                                                                                                                                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_AFTER_RECURRING_PAYNOW0    ${EMPTY}
    Should Be Equal             ${code}                                                  ${200}
    Should Be Equal             ${status}                                                OK
    ${correct_monthly}          evaluate                                                 ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_credit_amount}    evaluate                                                 math.floor(${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal             ${respdata}[0][data][monthlyFee]                         ${correct_monthly}
    Should Be Equal             ${respdata}[0][data][payNow]                             ${0}
    Should Be Equal             ${respdata}[0][data][starterFee]                         ${0}
    Should Be Equal             ${respdata}[0][data][creditAmount]                       ${correct_credit_amount}
    Should Be Equal             ${respdata}[0][data][swapCostStructure][extraDayCost]    ${0}
    Should Be Equal             ${respdata}[0][data][swapCostStructure][swapFee]         ${50}
    Should Be Equal             ${respdata}[0][data][currentWalletBalance]               ${0}
    Should Be Equal             ${respdata}[0][data][currentWalletBalanceUsed]           ${0}

Calculate Booking Cost Structure 15 Valid swap, one day before recurring
    [Tags]                URL Cases
    ${code}               ${status}                                                @{respdata}                                                                                                                                                                                                                                                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_ONE_DAY_BEFORE_RECURRING    ${EMPTY}
    Should Be Equal       ${code}                                                  ${200}
    Should Be Equal       ${status}                                                OK
    ${correct_monthly}    evaluate                                                 ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                                 math.floor(${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal       ${respdata}[0][data][monthlyFee]                         ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                             ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                         ${0}
    Should Be Equal       ${respdata}[0][data][creditAmount]                       ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][extraDayCost]    ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][swapFee]         ${50}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]               ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]           ${0}

Calculate Booking Cost Structure 16 Valid swap, on recurring
    [Tags]                URL Cases
    ${code}               ${status}                                                @{respdata}                                                                                                                                                                                                                                                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_ON_RECURRING    ${EMPTY}
    Should Be Equal       ${code}                                                  ${200}
    Should Be Equal       ${status}                                                OK
    ${correct_monthly}    evaluate                                                 ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                                 math.floor(${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal       ${respdata}[0][data][monthlyFee]                         ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                             ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                         ${0}
    Should Be Equal       ${respdata}[0][data][creditAmount]                       ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][extraDayCost]    ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][swapFee]         ${50}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]               ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]           ${0}

Calculate Booking Cost Structure 17 Valid swap, After scheduled recurring
    [Tags]                URL Cases
    ${code}               ${status}                                                  @{respdata}                                                                                                                                                                                                                                                                                               ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_AFTER_SCHEDULED_RECURRING    ${EMPTY}
    Should Be Equal       ${code}                                                    ${200}
    Should Be Equal       ${status}                                                  OK
    ${correct_monthly}    evaluate                                                   ${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                                   math.floor(${vehicle_data_db}[0][pricingData][oneMonth][basePrice] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal       ${respdata}[0][data][monthlyFee]                           ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                               ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                           ${0}
    Should Be Equal       ${respdata}[0][data][creditAmount]                         ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][remainingValue]    ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][swapFee]           ${50}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]                 ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]             ${0}

Calculate Booking Cost Structure 18 Valid swap, s2o
    [Tags]                URL Cases
    ${code}               ${status}                                                @{respdata}                                                                                                                                                                                                                                                                                           ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${s2o_swap}    SWAP_ON_RECURRING    ${EMPTY}
    Should Be Equal       ${code}                                                  ${200}
    Should Be Equal       ${status}                                                OK
    ${correct_monthly}    evaluate                                                 ${vehicle_data_db}[0][monthlyPricing] + ${0}
    ${correct_paynow}     evaluate                                                 math.floor(${vehicle_data_db}[0][pricingData][fixedStarterFee] + ${respdata}[0][data][swapCostStructure][earlyTerminationFee] + ${respdata}[0][data][swapCostStructure][swapFee]+ ${respdata}[0][data][swapCostStructure][extraDayCost] - ${respdata}[0][data][swapCostStructure][remainingValue])
    Should Be Equal       ${respdata}[0][data][monthlyFee]                         ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                             ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]                         ${vehicle_data_db}[0][pricingData][fixedStarterFee]
    Should Be Equal       ${respdata}[0][data][creditAmount]                       ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][extraDayCost]    ${0}
    Should Be Equal       ${respdata}[0][data][swapCostStructure][swapFee]         ${50}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]               ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalanceUsed]           ${0}

Calculate Booking Cost Structure 19 Invalid swap, s2o booking
    [Tags]             URL Cases
    ${code}            ${status}    @{respdata}    ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${default_swap}    SWAP_S2O    ${EMPTY}
    Should Be Equal    ${code}      ${200}
    Should Be Equal    ${status}    OK


Calculate Booking Cost Structure 20 Valid Data, No Swap, extra mileage, insurance, driver, use all wallet
    [Tags]                URL Cases
    ${code}               ${status}                                     @{respdata}                                                                                                                                                                  ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_mileage_insurance_driver}    ${EMPTY}    WALLET_1000
    Should Be Equal       ${code}                                       ${200}
    Should Be Equal       ${status}                                     OK
    ${correct_monthly}    evaluate                                      ${vehicle_data_db}[0][pricingData][oneMonth][extraMileagePrice] + ${vehicle_data_db}[0][pricingData][fullInsurance] + ${vehicle_data_db}[0][pricingData][secondaryDriver]
    ${correct_paynow}     evaluate                                      ${correct_monthly} - ${wallet_data_db}[0][3]
    Should Be Equal       ${respdata}[0][data][monthlyFee]              ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                  ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][starterFee]              ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]    ${wallet_data_db}[0][3]

Calculate Booking Cost Structure 21 Valid Data, No Swap, promocode, 6 months, use partial wallet
    [Tags]                URL Cases
    ${code}               ${status}                                     @{respdata}                                                                                                                                         ${vehicle_data_db}    ${promo_data_db}    ${wallet_data_db}=    Calculate Booking Cost Structure    ${valid_data_noaddon_promocode_6months}    ${EMPTY}    WALLET_1000
    Should Be Equal       ${code}                                       ${200}
    Should Be Equal       ${status}                                     OK
    ${correct_monthly}    evaluate                                      ${vehicle_data_db}[0][pricingData][sixMonth][basePrice] + ${0}
    ${correct_paynow}     evaluate                                      ${vehicle_data_db}[0][pricingData][sixMonth][basePrice] - ${promo_data_db}[0][reward][0][value] - ${respdata}[0][data][currentWalletBalanceUsed]
    Should Be Equal       ${respdata}[0][data][monthlyFee]              ${correct_monthly}
    Should Be Equal       ${respdata}[0][data][payNow]                  ${correct_paynow}
    Should Be Equal       ${respdata}[0][data][payNow]                  ${0}
    Should Be Equal       ${respdata}[0][data][starterFee]              ${0}
    Should Be Equal       ${respdata}[0][data][currentWalletBalance]    ${wallet_data_db}[0][3]
