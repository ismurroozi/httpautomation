import requests

def try1():
    url = "https://test-api.invygo.com/booking/createBooking"

    payload={'vehicleId': '6245aca19c1c82a7c20b568e',
    'bookingDateTime': '2022-09-11T09:00:00.000Z',
    'bookingType': '2',
    'delivery': 'true',
    'selectedMileage': '2500',
    'fullInsurance': 'false',
    'bookingPeriod': '9',
    'version': '2',
    'needAdditionalDriver': 'false'}
    files=[
        ('signatureImage',('tree.jpeg',open('C:/Users/ismurroozi/automation_framework/api_interface/utilities/template_files/tree.jpeg','rb'),'image/jpeg'))
    ]
    headers = {
        'content-language': 'en',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiI2Mzk5YzM3ODA1Njc1YjIyOGFkMjBhNDQiLCJjcmVhdGVkQnkiOiIiLCJyb2xlIjoiY3VzdG9tZXIiLCJzZXNzaW9uSUQiOiI2Mzk5YzM3ODA1Njc1YjJmNDNkMjBhNDkiLCJkYXRlIjoiMjAyMi0xMi0xNFQxMjozNzoxMi44OTZaIiwiaWF0IjoxNjcxMDIxNDMyLCJleHAiOjE2OTY5NDE0MzJ9.Shq0sa9-qg8g7jBW1tEfevrU4NAsIcRj0mXgLnoD01E'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

def main():
    try1()

if __name__ == "__main__":
    main()