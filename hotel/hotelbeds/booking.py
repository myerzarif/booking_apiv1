from hotel.base.booking import Booking
from content.hotelbeds.config import Config
from common.types import HttpMethods
from common.utils import generate_random_string
from cache_memoize import cache_memoize


class HbBooking(Booking):

    def __init__(self, params={}):
        self.config = Config(
            endpoint="/hotel-api/1.0/bookings",
            params=None,
            json=self.create_request_data(params),
            data=None,
            method=HttpMethods.POST
        )

    def create_request_data(self, params):
        if not params:
            return None

        params = {
            "holder": {
                "name": params['holder']['first_name'],
                "surname": params['holder']['last_name'],
            },
            "rooms": [
                {
                    "rateKey": params.get("rate_key"),
                }
            ],
            "clientReference": generate_random_string(20),
            "remark": params.get("remark", "")
        }

        return params

    def book(self):
        result = Booking.book(self)
        print(result)
        # return AvailabilityData(
        #     check_in=hotels.get("checkIn"),
        #     check_out=hotels.get("checkOut"),
        #     total=hotels.get("total"),
        #     hotels=self.get_availablehotels_dataclasses(
        #         hotels.get("hotels", []))
        # )


# {
#     "auditData": {
#         "processTime": "2801",
#         "timestamp": "2023-09-24 18:42:21.349",
#         "requestHost": "146.190.92.186, 10.214.142.213, 10.214.129.156",
#         "serverId": "ip-10-214-129-54.eu-central-1.compute.internal#A+",
#         "environment": "[awseucentral1, awseucentral1c, ip_10_214_129_54, eucentral1]",
#         "release": "",
#         "token": "8009DE4DE3154539A74AEC540EFA6009",
#         "internal": "0|06~~22688~489380211~N~~~NRF~0CE0C6A06DB141A169558089064700AAUK0000002000000000722688|UK|07|2|1|||||||||||R|1|1|~1~2~0|0|0||0|70ee9c04c862f43c76bec6dff2e6a265||||"
#     },
#     "booking": {
#         "reference": "1-5513562",
#         "clientReference": "INTEGRATIONAGENCY",
#         "creationDate": "2023-09-24",
#         "status": "CONFIRMED",
#         "modificationPolicies": {
#             "cancellation": true,
#             "modification": true
#         },
#         "creationUser": "70ee9c04c862f43c76bec6dff2e6a265",
#         "holder": {
#             "name": "HOLDERFIRSTNAME",
#             "surname": "HOLDERLASTNAME"
#         },
#         "hotel": {
#             "checkOut": "2023-10-02",
#             "checkIn": "2023-10-01",
#             "code": 1533,
#             "name": "Mirador",
#             "categoryCode": "4EST",
#             "categoryName": "4 STARS",
#             "destinationCode": "PMI",
#             "destinationName": "Majorca",
#             "zoneCode": 10,
#             "zoneName": "Palma",
#             "latitude": "39.5681",
#             "longitude": "2.6312",
#             "rooms": [
#                 {
#                     "status": "CONFIRMED",
#                     "id": 1,
#                     "code": "DBL.ST",
#                     "name": "DOUBLE STANDARD",
#                     "paxes": [
#                         {
#                             "roomId": 1,
#                             "type": "AD",
#                             "name": "First Adult Name",
#                             "surname": "Surname"
#                         },
#                         {
#                             "roomId": 1,
#                             "type": "AD",
#                             "name": "Second Adult Name",
#                             "surname": "Surname"
#                         }
#                     ],
#                     "rates": [
#                         {
#                             "rateClass": "NRF",
#                             "net": "136.38",
#                             "rateComments": "1x DOUBLE Estimated total amount of taxes & fees for this booking: 6.60 Euro   payable on arrival. Car park YES (with additional debit notes) 12.00 EUR Per unit/night. Check-in hour 14:00 - .",
#                             "paymentType": "AT_WEB",
#                             "packaging": true,
#                             "boardCode": "RO",
#                             "boardName": "ROOM ONLY",
#                             "cancellationPolicies": [
#                                 {
#                                     "amount": "136.38",
#                                     "from": "2023-09-23T23:59:00+02:00"
#                                 }
#                             ],
#                             "taxes": {
#                                 "taxes": [
#                                     {
#                                         "included": false,
#                                         "amount": "6.60",
#                                         "currency": "EUR",
#                                         "clientAmount": "6.60",
#                                         "clientCurrency": "EUR"
#                                     }
#                                 ],
#                                 "allIncluded": false
#                             },
#                             "rooms": 1,
#                             "adults": 2,
#                             "children": 0
#                         }
#                     ]
#                 }
#             ],
#             "totalNet": "136.38",
#             "currency": "EUR",
#             "supplier": {
#                 "name": "HOTELBEDS PRODUCT,S.L.U.",
#                 "vatNumber": "ESB38877676"
#             }
#         },
#         "remark": "Booking remarks are to be written here.",
#         "invoiceCompany": {
#             "code": "E14",
#             "company": "HOTELBEDS S.L.U.",
#             "registrationNumber": "ESB57218372"
#         },
#         "totalNet": 136.38,
#         "pendingAmount": 136.38,
#         "currency": "EUR"
#     }
# }
