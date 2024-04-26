from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"), # provided by scaffold
    path("logout", views.logout_view, name="logout"), # provided by scaffold
    path("register", views.register, name="register"), # provided by scaffold
    path('create_listing/', views.create_listing, name="create_listing"),
    path("listing/<int:pk>", views.listing_details, name="listing_details"),
    path('place_bid/<int:pk>/', views.place_bid, name='place_bid'),
    path("close_auction/<int:pk>/", views.close_auction, name="close_auction"),
    path("listing/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listings/category/<int:category_id>", views.listing_details, name="listings_by_category"),
    path('search/', views.search_results, name='search_results'),
    path('user/<str:username>/', views.user_listings, name='user_listings')
]
