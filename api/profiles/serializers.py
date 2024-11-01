from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    def save(self):
        user = User(
        email=self.validated_data['email'],
        username=self.validated_data['username'],
        first_name=self.validated_data['first_name'],
        last_name =self.validated_data['last_name'],
        phone_number=self.validated_data['phone_number']
        )
        password=self.validated_data['password']
        # password2 = self.validated_data['password2']
        # if password != password2:
        #     raise serializers.ValidationError({"password": "Passwords must match."})

        user.set_password(password)
        user.save()

        return user
        
    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "matric_no", "first_name", "last_name", "institution", "program_of_study", "academic_level", "profile_picture", "date_joined", "is_active", "password", "password2")
        read_only = ("date_joined", "is_active", )
        extra_kwargs = {
            'password': {'write_only': True}
            }
