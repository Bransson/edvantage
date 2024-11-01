from django.urls import path

from .views import ChatView, MessageView


urlpatterns = [
    path("create-chat/", ChatView.as_view(), name="create_get_transaction"),
    path("create-message/", MessageView.as_view(), name="create_get_message"),
    # path("getpersonaltransactionbyid/", GetPersonalTransactionById.as_view(), name="get_personal_transaction_by_id"),

    ]
