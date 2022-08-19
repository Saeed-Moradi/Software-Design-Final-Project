from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': '(ایمیل(این فیلد اجباری است','class':'form-control mt-2 text-right'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': '(نام(این فیلد اجباری است',
                                            'class': 'form-control mt-2 text-right'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': '(نام خانوادگی(این فیلد اجباری است',
                                           'class': 'form-control mt-1 text-right'}))
    phone = forms.CharField(max_length=11,
                            widget=forms.TextInput(
                                attrs={'placeholder': '(تلفن همراه(این فیلد اجباری است',
                                       'class': 'form-control mt-1 text-right'}))

    # image = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2',)


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'نام', 'class': 'form-control mt-2 text-right'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'نام خانوادگی', 'class': 'form-control mt-2 text-right'}))
    phone = forms.CharField(max_length=11,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'تلفن همراه', 'class': 'form-control mt-2 text-right'}))
    image = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone', 'image')
