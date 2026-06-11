from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from app.models import User, Category
from django.urls import reverse_lazy
from .forms import UserCreateForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def index(request):
    categories = Category.objects.all()
    login_user = None
    if request.session.get("is_login"):
        login_user = User.objects.filter(user_id=request.session['login_user_id']).first()
    return render(request, "app/base.html", {"categories": categories,'login_user': login_user})


class UserCreate(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "app/signup.html"
    success_url = reverse_lazy("app:login")

    def form_valid(self, form):
        # パスワードをハッシュ化して保存
        form.instance.password = make_password(form.cleaned_data["password"])
        return super().form_valid(form)


def login_view(request):
    form = LoginForm()
    print("aaa")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]

            # ① DBからユーザーを探す
            user = User.objects.filter(name=name).first()

            # ② パスワードが一致するか確認
            if user and check_password(password, user.password):
                # ③ セッションに保存（＝ログイン状態にする）
                request.session["is_login"] = True
                request.session["login_user_id"] = user.user_id
                request.session["login_user_name"] = user.name
                return redirect("app:index")
                # return render(request, "app/login.html", {"form": form})

            # ④ 失敗
            form.add_error(None, "ユーザー名またはパスワードが違います")

    return render(request, "app/login.html", {"form": form})


def logout_view(request):
    request.session.flush()  # セッション全削除
    return redirect("app:login")


def user_list_view(request):
    # ログインチェック
    if not request.session.get("is_login"):
        return redirect("app:login")

    users = User.objects.all()
    return render(request, "app/snsuser_list.html", {
        "users": users,
        "login_user_name": request.session.get("login_user_name"),
    })

def search_view(request):
    return redirect("app:")