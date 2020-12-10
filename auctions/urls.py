from django.urls import path

from . import views

# app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/end_bid", views.end_bid, name="end_bid"),
    path("wishlist/<int:user_id>/", views.wishlist, name="wishlist"),
    path("<int:listing_id>/wishitem", views.wishitem, name="wishitem"),
    path("getlisting", views.getlisting, name="getlisting"),
    path("removeWishitem", views.removeWishitem, name="removeWishitem"),
    path("removeWish", views.removeWish, name="removeWish"),
    path("<int:listing_id>/comment", views.comment, name="add_comment"),
    path("add_category", views.add_cat, name="add_category"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cats>/", views.category, name="category"),
    path("closed_bid", views.closed_bid, name="closed_bid"),
    path("verdict/<str:bid>/", views.verdict, name="verdict"),
]
