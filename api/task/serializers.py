from rest_framework import serializers
from tasks.models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only = ("datetime")
        fields = "__all__"
        # exclude = ("user_from_balance", "user_to_balance")
        extra_kwargs = {
            # 'creator': {'read_only': True},
            # 'members': {'read_only': True},
            # 'admin': {'read_only': True},
            }

class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        read_only = ("datetime",)
        fields = "__all__"
        # exclude = ("user_from_balance", "user_to_balance")

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only = ("datetime",)
        fields = "__all__"
        # exclude = ("user_from_balance", "user_to_balance")
# class MessageTaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MessageTasks
#         read_only = ("datetime",)
#         fields = "__all__"
#         # exclude = ("user_from_balance", "user_to_balance")

