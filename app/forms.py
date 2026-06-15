from django import forms
from app.models import User


from django import forms
from app.models import User

class UserCreateForm(forms.ModelForm):
    password_confirm = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["user_id", "password", "password_confirm", "name", "address"]
        widgets = {
            "password": forms.PasswordInput(),
        }
        labels = {
            "user_id": "会員ID",
            "password": "パスワード",
            "name": "お名前",
            "address": "ご住所",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("パスワードが一致しません")
        return cleaned_data


class LoginForm(forms.Form):
    """ログインフォーム（DBと連動しないのでforms.Form）"""

    user_id = forms.CharField(label="会員ID", max_length=100)
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(),
    )


class UserUpdateForm(forms.ModelForm):
    user_id = forms.CharField(
        label="会員ID",
        disabled=True
    )

    new_password = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput(),
        required=False
    )

    new_password_confirm = forms.CharField(
        label="新しいパスワード（確認）",
        widget=forms.PasswordInput(),
        required=False
    )

    class Meta:
        model = User
        fields = ["user_id", "name", "address"]
        labels = {
            "name": "お名前",
            "address": "ご住所",
        }

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if (new_password and not new_password_confirm) or (not new_password and new_password_confirm):
            raise forms.ValidationError("新しいパスワードと確認用パスワードを両方入力してください。")

        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError("新しいパスワードが一致しません。")

        return cleaned_data