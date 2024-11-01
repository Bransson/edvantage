from telnetlib import SE
from typing import OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.db.models import Q


from chat.models import *
from tasks.models import*
from .serializers import MessageSerializer, ChatSerializer


User = get_user_model()


class MessageView(APIView):
    permission_classes = (IsAuthenticated,)

    # get Transactions that have a relation with the current logged in user (user_to or user_from)
    def get(self, request):
        p = request.user
        # transactions = Transaction.objects.filter(Q(user_to=p) |Q( user_from=p))
        dic = {}
        lst = []

        for obj in Message.objects.filter(chat = request.data.get("chat")):
            
            dic[obj.id]= [obj.user, obj.text, obj.tasks, obj.calender, obj.datetime]

            lst.append(dic)
            dic = {}
        return Response(lst)
    
        
    def post(self, request):
        serializer = MessageSerializer(data=request.data,)
        data = []
        if serializer.is_valid(raise_exception=True):
            prof = User.objects.get(id=request.user.id)

            for key in serializer.data:
                key = dict(key)
                key['user'] = prof.id
                data.append(key)
            
            serializer = MessageSerializer(data=data,)
            if serializer.is_valid(raise_exception=True):   
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      


class ChatView(APIView):
    permission_classes = (IsAuthenticated,)

    # get Transactions that have a relation with the current logged in user (user_to or user_from)
    def get(self, request):
        pk = request.data.get(id)
        # transactions = Transaction.objects.filter(Q(user_to=p) |Q( user_from=p))
        dic = {}
        lst = []
        if pk:
            for obj in Chat.objects.filter(id = pk):
                
                dic[obj.id]= [obj.name, obj.members, obj.admin, obj.picture, obj.description, obj.datetime]

                lst.append(dic)
                dic = {}
        else:
            for obj in Chat.objects.filter(user = request.user):
                
                dic[obj.id]= [obj.name, obj.members, obj.admin, obj.picture, obj.description, obj.datetime]

                lst.append(dic)
                dic = {}

        return Response(lst)
    
        
    def post(self, request):
        serializer = ChatSerializer(data=request.data,)
    
        if serializer.is_valid(raise_exception=True):
            prof = User.objects.get(id=request.user.id)

            serializer.save(creator =prof)

            serializer = ChatSerializer(data=serializer.data,)
            if serializer.is_valid(raise_exception=True):   
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

# class TaskView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         pk = request.data.get(id)
#         dic = {}
#         lst = []

#         if pk:
#             for obj in Task.objects.filter(id = pk):
                
#                 dic[obj.id]= [obj.user, obj.title, obj.course_code, obj.due_date, obj.datetime, obj.additional_notes, obj.type_type]

#                 lst.append(dic)
#                 dic = {}
#         else:
#             for obj in Task.objects.filter(user = request.user):
                
#                 dic[obj.id]= [obj.user, obj.title, obj.course_code, obj.due_date, obj.datetime, obj.additional_notes, obj.type_type]

#                 lst.append(dic)
#                 dic = {}

#         return Response(lst)
    
        
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data,)
    
#         if serializer.is_valid(raise_exception=True):
#             prof = User.objects.get(id=request.user.id)

#             serializer.save(creator =prof)

#             serializer = TaskSerializer(data=serializer.data,)
#             if serializer.is_valid(raise_exception=True):   
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

