from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/create/", views.create, name="create"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("wiki/rand/", views.random_entry, name="random_e")
]
