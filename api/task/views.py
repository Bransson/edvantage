from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.db.models import Q


from tasks.models import*
from .serializers import CalenderSerializer, TaskSerializer


User = get_user_model()


# class MessageView(APIView):
#     permission_classes = (IsAuthenticated,)

#     # get Transactions that have a relation with the current logged in user (user_to or user_from)
#     def get(self, request):
#         p = request.user
#         # transactions = Transaction.objects.filter(Q(user_to=p) |Q( user_from=p))
#         dic = {}
#         lst = []

#         for obj in Message.objects.filter(chat = request.data.get("chat")):
            
#             dic[obj.id]= [obj.user, obj.text, obj.datetime]

#             lst.append(dic)
#             dic = {}
#         return Response(lst)
    
        
#     def post(self, request):
#         serializer = MessageSerializer(data=request.data,)
#         data = []
#         if serializer.is_valid(raise_exception=True):
#             prof = User.objects.get(id=request.user.id)

#             for key in serializer.data:
#                 key = dict(key)
#                 key['user'] = prof.id
#                 data.append(key)
            
#             serializer = MessageSerializer(data=data,)
#             if serializer.is_valid(raise_exception=True):   
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      


class CalenderView(APIView):
    permission_classes = (IsAuthenticated,)

    # get Transactions that have a relation with the current logged in user (user_to or user_from)
    def get(self, request):
        pk = request.data.get(id)
        # transactions = Transaction.objects.filter(Q(user_to=p) |Q( user_from=p))
        dic = {}
        lst = []
        if pk:
            for obj in Calender.objects.filter(id = pk):
                
                dic[obj.id]= [{'name': obj.name, 'user': obj.user, 'datetime': obj.datetime}]

                lst.append(dic)
                dic = {}
        else:
            for obj in Calender.objects.filter(user = request.user):
                
                dic[obj.id]= [{'name': obj.name, 'user': obj.user, 'datetime': obj.datetime}]
                lst.append(dic)
                dic = {}

        return Response(lst)
    
        
    def post(self, request):
        serializer = CalenderSerializer(data=request.data,)
    
        if serializer.is_valid(raise_exception=True):
            prof = User.objects.get(id=request.user.id)

            serializer.save(creator =prof)

            serializer = CalenderSerializer(data=serializer.data,)
            if serializer.is_valid(raise_exception=True):   
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pk = request.data.get(id)
        dic = {}
        lst = []

        if pk:
            for obj in Task.objects.filter(id = pk):
                
                dic[obj.id]= [obj.user, obj.title, obj.course_code, obj.due_date, obj.datetime, obj.additional_notes, obj.type_type, ]

                lst.append(dic)
                dic = {}
        else:
            for obj in Task.objects.filter(user = request.user):
                
                dic[obj.id]= [obj.user, obj.title, obj.course_code, obj.due_date, obj.datetime, obj.additional_notes, obj.type_type]

                lst.append(dic)
                dic = {}

        return Response(lst)
    
        
    def post(self, request):
        serializer = TaskSerializer(data=request.data,)
    
        if serializer.is_valid(raise_exception=True):
            prof = User.objects.get(id=request.user.id)

            serializer.save(creator =prof)

            serializer = TaskSerializer(data=serializer.data,)
            if serializer.is_valid(raise_exception=True):   
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         


# class TransferView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data, many=True)
#         data = {}.
#         if serializer.is_valid(raise_exception=True):
#             prof = User.objects.get(id=request.user)
#             transaction = serializer.save(commit=False)
#             transaction.user_from = prof
#             transaction.save()
#             try:
#                 data['user_from'] = transaction.user_from.id
#             except:
#                 pass
#             finally:
#                 data['user_to'] = transaction.user_to.id
#                 data['amount'] = transaction.amount
#                 data["transaction_type"] = transaction.transaction_type
#                 data['payment_method'] = transaction.payment_method
#                 data["transaction_id_number"] = transaction.transaction_id_number
#                 data["status"] = transaction.status
#                 data["narration"] = transaction.narration
#                 data['date_time'] = transaction.date_time
#             return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      



# class GetTransactionById(APIView):
#     def get(self, request):
#         data = {}
#         transaction_id_number = request.data.get("transaction_id_number")
#         transaction = Transaction.objects.get(transaction_id_number = transaction_id_number)
        
#         try:
#             data['user_from'] = transaction.user_from.id
#         except:
#             pass
#         finally:
#             data["id"] = transaction.id
#             data["user_to"] = transaction.user_to.id
#             data["amount"] = transaction.amount
#             data["transaction_type"] = transaction.transaction_type
#             data["payment_method"] = transaction.payment_method
#             data["transaction_id_number"] = transaction.transaction_id_number
#             data["status"] = transaction.status
#             data["narration"] = transaction.narration
#             data["date_time"] = transaction.date_time
#         return Response(data, status=status.HTTP_201_CREATED) 


# class GetPersonalTransactionById(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         data = {}
#         transaction_id_number = request.data.get("transaction_id_number")
#         try:
#             transaction = Transaction.objects.get(transaction_id_number = transaction_id_number)
#             if transaction.user_to == request.user or transaction.user_from == request.user:
#                 data["id"] = transaction.id
#                 try:
#                     data["user_from"] = transaction.user_from.id
#                     data["transaction_balance"] = transaction.user_from_balance

#                 except:
#                     data["user_to"] = transaction.user_to.id
#                     data["transaction_balance"] = transaction.user_to_balance

#                 finally:
#                     data["amount"] = transaction.amount
#                     data["transaction_type"] = transaction.transaction_type
#                     data["payment_method"] = transaction.payment_method
#                     data["transaction_id_number"] = transaction.transaction_id_number
#                     data["status"] = transaction.status
#                     data["narration"] = transaction.narration

#                     data["date_time"] = transaction.date_time
        
#                 return Response(data, status=status.HTTP_200_OK)
#             return Response(data, status=status.HTTP_403_FORBIDDEN)
#         except:
#             return Response(data, status=status.HTTP_404_NOT_FOUND)














# class TransferView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid(raise_exception=True):
#             prof = User.objects.get(id=request.user.id)
#             print(type(serializer.validated_data['user_from']))
#             if serializer.validated_data['user_from'] == prof:
#                 transaction = serializer.save()
#                 try:
#                     data['user_from'] = transaction.user_from.id
#                 except:
#                     pass
#                 finally:
#                     data['user_to'] = transaction.user_to.id
#                     data['amount'] = transaction.amount
#                     data["transaction_type"] = transaction.transaction_type
#                     data['payment_method'] = transaction.payment_method
#                     data["transaction_id_number"] = transaction.transaction_id_number
#                     data["status"] = transaction.status
#                     data["narration"] = transaction.narration
#                     data['date_time'] = transaction.date_time
#                 return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

"""
class TransactionView(APIView):
    permission_classes = (IsAuthenticated,)

    # get Transactions that have a relation with the current logged in user (user_to or user_from)
    def get(self, request):
        p = request.user
        # transactions = Transaction.objects.filter(Q(user_to=p) |Q( user_from=p))
        transactions1 = Transaction.objects.filter(user_to=p)
        transactions2 = Transaction.objects.filter(user_from=p)
        # transactions1 = [t.user_from_balance = None) for t in transactions1]

        serializer1 = TransactionSerializer(transactions1, many=True)
        serializer2 = TransactionSerializer(transactions2, many=True)
        serializer1_data = serializer1.data
        # print(type(serializer1_data))
        serializer1_data.user_from_balance = None
        serializer2_data = serializer2.data
        serializer2_data.user_to_balance = None
        print(serializer2_data)
        serializer_data = serializer1_data + serializer2_data
        
        

        return Response(serializer_data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            prof = User.objects.get(user=request.user).id
            if serializer.validated_data['user_from'].id == prof:
                transaction = serializer.save()
                data['user_from'] = transaction.user_from.id
                data['user_to'] = transaction.user_to.id
                data['amount'] = transaction.amount
                data['payment_method'] = transaction.payment_method
                return Response(data, status=status.HTTP_201_CREATED)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""