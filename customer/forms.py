from django import forms
from customer.models import Customer


class FormDangKy(forms.ModelForm):
    first_name = forms.CharField(max_length=264, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Họ",
    }))
    last_name = forms.CharField(max_length=264, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Tên",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu",
    }))
    confirm_password = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận Mật khẩu",
    }))
    phone = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Điện thoại",
    }))
    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Địa chỉ", "rows": "3",
    }))

    class Meta:
        model = Customer
        fields = '__all__'


