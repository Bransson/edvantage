from django.urls import path, include



urlpatterns = [
    path("message-chat/", include("api.message_chat.urls"), name="message_chat"),
    path("profiles/", include("api.profiles.urls"), name="profile"),
    path("tasks/", include("api.tasks.urls"), name="tasks"),
    ]
