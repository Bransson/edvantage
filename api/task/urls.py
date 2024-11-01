from django.urls import path

from .views import CalenderView, TaskView


urlpatterns = [
   path("create-task",  TaskView.as_view(), name="create_get_task"),
   path("create-calender",  CalenderView.as_view(), name="create_get_calender"),
    # path("getpersonaltransactionbyid/", GetPersonalTransactionById.as_view(), name="get_personal_transaction_by_id"),

    ]
