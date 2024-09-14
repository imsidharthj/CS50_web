from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("create", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist.remove", views.remove_from_watchlist, name="remove_from_watchlist")
]
