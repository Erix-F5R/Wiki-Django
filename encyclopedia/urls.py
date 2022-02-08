from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("new-page/", views.new_page, name="new-page"),
    path("wiki/<str:title>/edit-page", views.edit_page, name="edit-page"),
    path("random/", views.random, name="random")

    
]
