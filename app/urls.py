from django.urls import path
from . import views

app_name = "app"
    
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.UserCreate.as_view(), name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("timeline/", views.timeline_view, name="timeline"),
    path("users/", views.user_list_view, name="snsuser_list"),
    path("search/", views.search_view, name="search"),
    # path("like/<int:post_id>/", views.like_view, name="like"),
]