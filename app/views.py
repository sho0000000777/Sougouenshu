from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from app.models import User, Category, Item, Category, Itemincart
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
    if request.session.get("is_login"):
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

        item = Item.objects.filter(item_id=item_id).first()

        login_user_id = request.session.get("login_user_id")
        
        user = User.objects.filter(user_id=login_user_id).first()

        cart_item = Itemincart.objects.filter(user=user, item=item).first()

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

    return render(request, "app/cart.html", {
        "itemsincart": itemsincart,
    })
