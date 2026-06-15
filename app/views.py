from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from app.models import User, Category, Item, Category, Itemincart
from django.urls import reverse_lazy
from .forms import UserCreateForm, LoginForm, UserUpdateForm
from django.contrib.auth.hashers import make_password, check_password
from django.views import View

# Create your views here.
def index(request):
    categories = Category.objects.all()
    login_user = None
    if request.session.get("is_login"):
        login_user = User.objects.filter(user_id=request.session['login_user_id']).first()
    return render(request, "app/base.html", {"categories": categories,'login_user': login_user})


class UserCreateView(View):
    template_name = "app/signup.html"
    confirm_template_name = "app/registerUserConfirm.html"

    def get(self, request):
        form = UserCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            request.session["signup_data"] = {
                "user_id": form.cleaned_data["user_id"],
                "password": form.cleaned_data["password"],
                "name": form.cleaned_data["name"],
                "address": form.cleaned_data["address"],
            }

            return render(request, self.confirm_template_name, {
                "data": request.session["signup_data"]
            })

        return render(request, self.template_name, {"form": form})


class UserCreateCompleteView(View):
    def post(self, request):
        signup_data = request.session.get("signup_data")

        if not signup_data:
            return redirect("app:signup")

        user = User(
            user_id=signup_data["user_id"],
            password=make_password(signup_data["password"]),
            name=signup_data["name"],
            address=signup_data["address"],
        )

        user.save()

        # 登録後はセッションを消す
        del request.session["signup_data"]

        return render(request, "app/registerUserCommit.html", {
            "name": user.name,
        })


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            password = form.cleaned_data["password"]

            # ① DBからユーザーを探す
            user = User.objects.filter(user_id=user_id).first()

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
    request.session.flush()  
    return redirect("app:login")

def search_view(request):
    category_id = request.GET.get('category', "")
    keyword = request.GET.get('keyword', "")

    items = Item.objects.all()
    category_name = 'すべて'

    if category_id:
        items = items.filter(category_id=category_id)
        category = Category.objects.filter(category_id=category_id).first()
        category_name = category.name if category else ''

    if keyword:
        items = items.filter(name__icontains=keyword)
    
    return render(request, 'app/searchResult.html', {
        'items': items,
        'keyword':keyword,
        'category_name':category_name
    })

def itemdetail_view(request, item_id):
    item = Item.objects.filter(item_id=item_id).first()
    login_user = None
    if request.session.get("is_login"):#ログイン中かどうかで処理が分岐
        login_user = User.objects.filter(user_id=request.session['login_user_id']).first()

    if not item:
        return render(request, 'app/itemDetail.html', {
            'error': '商品が見つかりません',
        })

    return render(request, 'app/itemDetail.html', {
        'item': item,
        'login_user': login_user,
        "amount_range": range(1, item.stock + 1),
    })

def cart_insert_view(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        amount = request.POST.get("amount")
        amount = int(amount)

        item = Item.objects.filter(item_id=item_id).first()#挿入する商品を検索

        login_user_id = request.session.get("login_user_id")#ログイン中のユーザID取得
        
        user = User.objects.filter(user_id=login_user_id).first()#ユーザを調べる

        cart_item = Itemincart.objects.filter(user=user, item=item).first()#ユーザとアイテムから現在のカートに該当商品があるか検索

        if cart_item:
            cart_item.amount += amount
            cart_item.save()
        else:
            Itemincart.objects.create(
                user=user,
                item=item,
                amount=amount
            )
        return redirect("app:cart")

    return redirect("app:index")

def cart_view(request):
    login_user_id = request.session.get("login_user_id")
    user = User.objects.filter(user_id=login_user_id).first()

    itemsincart = Itemincart.objects.filter(user=user)
    sum_price = 0
    for item in itemsincart:
        sum_price += item.item.price * item.amount

    return render(request, "app/cart.html", {
        "itemsincart": itemsincart,
        "sum_price": sum_price,
    })

def userinfo_view(request):
    if request.session.get("is_login"):#ログイン中かどうか
        login_user = User.objects.filter(user_id=request.session['login_user_id']).first()
    return render(request, "app/userInfo.html", {
        "login_user":login_user
    })


class UserUpdateView(View):
    template_name = "app/updateUser.html"
    confirm_template_name = "app/updateUserConfirm.html"

    def get(self, request):
        login_user_id = request.session.get("login_user_id")
        user = User.objects.filter(user_id=login_user_id).first()
        form = UserUpdateForm(instance=user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        login_user_id = request.session.get("login_user_id")
        user = User.objects.filter(user_id=login_user_id).first()
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            request.session["user_update_data"] = {
                "user_id": form.cleaned_data["user_id"],
                "name": form.cleaned_data["name"],
                "address": form.cleaned_data["address"],
                "new_password": form.cleaned_data["new_password"],
            }

            return render(request, self.confirm_template_name, {
                "data": request.session["user_update_data"]
            })

        return render(request, self.template_name, {"form": form})


class UserUpdateCompleteView(View):
    def post(self, request):
        login_user_id = request.session.get("login_user_id")
        update_data = request.session.get("user_update_data")
        user = User.objects.filter(user_id=login_user_id).first()
        user.name = update_data["name"]
        user.address = update_data["address"]

        if update_data["new_password"]:
            user.password = make_password(update_data["new_password"])

        user.save()

        # セッションの表示用情報も更新
        request.session["login_user_name"] = user.name

        # 使い終わった一時データは消す
        del request.session["user_update_data"]

        return redirect("app:user_update_done")


class UserUpdateDoneView(View):
    def get(self, request):
        login_user = User.objects.filter(user_id=request.session['login_user_id']).first()
        return render(request, "app/updateUserCommit.html",{
            "login_user": login_user,
        })


class UserDeleteView(View):
    template_name = "app/withdrawConfirm.html"

    def get(self, request):
        login_user_id = request.session.get("login_user_id")

        user = User.objects.filter(user_id=login_user_id).first()

        return render(request, self.template_name, {
            "login_user": user,
        })

    def post(self, request):
        login_user_id = request.session.get("login_user_id")

        user = User.objects.filter(user_id=login_user_id).first()

        user.delete()

        request.session.flush()

        return redirect("app:user_delete_done")


class UserDeleteDoneView(View):
    def get(self, request):
        return render(request, "app/withdrawCommit.html")