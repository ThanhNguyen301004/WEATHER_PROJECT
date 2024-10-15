# forms.py
from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Nhập lại mật khẩu")

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Mật khẩu không khớp!")
