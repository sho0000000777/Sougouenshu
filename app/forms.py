from django import forms
from app.models import User


class UserCreateForm(forms.ModelForm):
    """会員登録フォーム"""

    class Meta:
        model = User
        fields = ["user_id", "password", "name", "address"]
        widgets = {
            "password": forms.PasswordInput(),
        }
        labels = {
            "user_id": "会員ID",
            "password": "パスワード",
            "name": "お名前",
            "address": "ご住所",
        }


class LoginForm(forms.Form):
    """ログインフォーム（DBと連動しないのでforms.Form）"""

    name = forms.CharField(label="ユーザー名", max_length=100)
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(),
    )

