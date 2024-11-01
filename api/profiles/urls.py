from django.urls import path

from .views import CreateUserView, GetUserIdByMatricNo, ProfileView

urlpatterns = [
    path("getuser/", ProfileView.as_view(), name="get_user"),
    path("createuser/", CreateUserView.as_view(), name="create_user"),
    path("getuseridbymatricno/", GetUserIdByMatricNo.as_view(), name="get_user_id_by_account_number"),
    # path("getcurrentusermoneyinfo/", GetCurrentUserMoneyInfo.as_view(), name="get_current_user_money_info"),

    ]
