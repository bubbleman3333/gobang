from django.urls import path
from . import views

urlpatterns = [
    path("play/", views.show_board, name="play_gobang"),
    path("put_stone/", views.put_stone),
    path("observe/", views.observe),
    path("start/", views.reset),
    path("", views.index)
]
