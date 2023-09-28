from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from .models import CustomUser, Review


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('username', css_class='col-md-6'),
            Div('password1', css_class='col-md-6'),
            Div('password2', css_class='col-md-6'),
            Submit('submit', 'Зарегистрироваться')
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
