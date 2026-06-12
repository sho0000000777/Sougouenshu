from django.urls import path
from . import views

app_name = "app"
    
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.UserCreate.as_view(), name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("search/", views.search_view, name="search"),
    path('item/<int:item_id>/', views.itemdetail_view, name='item_detail'),
    path('cart/insert/', views.cart_insert_view, name='cart_insert'),
    path("cart/", views.cart_view, name="cart"),
]