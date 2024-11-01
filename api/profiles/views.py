from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from django.contrib.auth import get_user_model

# from transaction.models import *
from .serializers import UserSerializer


User = get_user_model()

class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    # returns a response of all of users
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class CreateUserView(APIView):
    # creates a user with first_name, last_name, username and phoneumber
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['username'] = user.username
            data['phone_number'] = user.phone_number
            data["email"] = user.wallet_id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    # user has to be authenticated to acces this view
    permission_classes = (IsAuthenticated,)
    # parsers for json and (MultiPartParser, FormParser) for files passed in request
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    # gets current logged in user
    def get(self, request):
        p = request.user.id
        p = User.objects.get(id=p)
        serializer = UserSerializer(p)
        return Response(serializer.data)

    # updates profile of current logged in user
    def put(self, request):
        p = User.objects.get(user=request.user)

        # set file_obj to list of files passed as a parameter 'file' in the request if not set file_obj to None
        try:
            file_obj = request.data.getlist("file")   
        except:
            file_obj = None

        # if file_obj is delete, then set profile_picture to None
        if file_obj == "delete":
            if p.profile_picture:
                p.profile_picture = None
                p.save()
       
        # if file_object is not delete and not empty then set profile_picture to last picture in file_obj
        elif file_obj !="delete" and file_obj != None:
            p.profile_picture = file_obj[-1]
            p.save()
            
        serializer = UserSerializer(p)
        return Response(serializer.data)


class GetUserIdByMatricNo(APIView):
    def get(self, request):
        data = {}
        matric_no = request.data.get("matric_no")
        try:
            user = User.objects.get(matric_no = matric_no)
            data["id"] = user.id
        except:
            return Response(data, status=status.HTTP_404_NOT_FOUND) 

        return Response(data, status=status.HTTP_200_OK) 


# class GetCurrentUserMoneyInfo(APIView):
#     def get(self, request):
#         data = {}
#         user = request.user
#         try:
#             data["id"] = user.id
#             data["phone_number"] = user.phone_number
#             data["balance"] = user.balance
#             return Response(data, status=status.HTTP_200_OK) 
#         except:
#             pass
#         return Response(data, status=status.HTTP_404_NOT_FOUND) 

