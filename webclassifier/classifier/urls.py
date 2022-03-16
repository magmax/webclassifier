
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("spam/<int:pk>/", views.spam, name="spam"),
    path("jam/<int:pk>/", views.jam, name="jam"),
    path("process/<int:pk>/", views.process, name="process"),
    path("processall/", views.processall, name="processall"),
]
