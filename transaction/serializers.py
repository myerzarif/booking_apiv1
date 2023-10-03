from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin
from .models import Transaction
from account.models import User
from account.serializers import UserSerializer
from hotel.base.availability import Availability
from common.utils import generate_unique_id


class TransactionSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Transaction
        fields = [
            "id",
            "created_at",
            "user",
            "payer",
            "status",
            "comment",
        ]
        read_only_fields = ['id']

    def get_user(self, instance):
        return UserSerializer(User.objects.get(pk=instance.user_id)).data

# {
# 	id: "54e40663-93e0-4a2a-9d2b-04c1001d1ec2",
# 	room_code: "DBL.DX",
# 	rate_key: "20231010|20231011|W|148|88930|DBL.DX|FIT..",
# 	bank_account: {},
# 	holder_info: {}
# }


class HolderSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


# class ReservationSerializer(serializers.Serializer):
#     item_id = serializers.CharField(required=True)
#     holder = HolderSerializer()
#     rate_key = serializers.CharField(required=True)
#     remark = serializers.CharField(required=False)

#     def initiate_transaction(self, params, user):
#         Transaction(
#             reference_id=generate_unique_id(),
#             user=user,

#         )

#     def reserve(self, params, user):
#         search_item = get_search_info(params.get("item_id"))
#         self.initiate_transaction(params, user)

class ReservationSerializer(serializers.Serializer):
    item_id = serializers.CharField(required=True)
    car_code = serializers.CharField(required=True)

    def initiate_reservation(self, search_item):
        pass

    def reserve(self):
        search_item = Availability().get_search_info(self.validated_data.get("item_id"))

        print("search_item", search_item)
        print("self.request.user", self.request.user)

        self.initiate_reservation(search_item)
