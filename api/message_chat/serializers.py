from rest_framework import serializers
from chat.models import *
from tasks.models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        read_only = ("datetime")
        fields = "__all__"
        # exclude = ("user_from_balance", "user_to_balance")
        extra_kwargs = {
            # 'creator': {'read_only': True},
            'members': {'read_only': True},
            'admin': {'read_only': True},
            }

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        read_only = ("datetime",)
        fields = "__all__"
        # exclude = ("user_from_balance", "user_to_balance")

        # exclude = ("user_from_balance", "user_to_balance")
# class MessageTaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MessageTasks
#         read_only = ("datetime",)
#         fields = "__all__"
#         # exclude = ("user_from_balance", "user_to_balance")

