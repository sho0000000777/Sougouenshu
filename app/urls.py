from django.urls import path
from . import views

app_name = "app"
    
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("signup/complete/", views.UserCreateCompleteView.as_view(), name="signup_complete"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("search/", views.search_view, name="search"),
    path('item/<int:item_id>/', views.itemdetail_view, name='item_detail'),
    path('cart/insert/', views.cart_insert_view, name='cart_insert'),
    path("cart/", views.cart_view, name="cart"),
    path("userinfo/",views.userinfo_view, name="userinfo"),
    path("user/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("user/update/complete/", views.UserUpdateCompleteView.as_view(), name="user_update_complete"),
    path("user/update/done/", views.UserUpdateDoneView.as_view(), name="user_update_done"),
    path("user/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path("user/delete/done/", views.UserDeleteDoneView.as_view(), name="user_delete_done"),
]