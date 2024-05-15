from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserModel, GroupModel, NoteModel


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2, max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control py-4',
                                            'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(min_length=2, max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control py-4',
                                           'placeholder': 'Enter your last name'}))

    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Enter your password'}))

    group = forms.ModelChoiceField(
        queryset=GroupModel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label="Select your group"
    )

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'password', 'group']
        exclude = ['created']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control py-4',
                                             'placeholder': 'Enter your email'}),

        }


class ManagerRegisterForm(forms.ModelForm):
    first_name = forms.CharField(min_length=2, max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control py-4',
                                            'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(min_length=2, max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control py-4',
                                           'placeholder': 'Enter your last name'}))

    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Enter your password'}))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'password']
        exclude = ['created','group']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control py-4',
                                             'placeholder': 'Enter your email'}),

        }


class GroupAddForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                         'placeholder': 'Enter event name'}))
    description = forms.CharField(min_length=5, max_length=20,
                                  widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                                'placeholder': 'Enter a description'}))

    class Meta:
        model = GroupModel
        fields = ['name', 'description']
        exclude = ['users_count']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True,
            'autocomplete': 'email'  # Add autocomplete attribute for username
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password'  # Add autocomplete attribute for password
        }
    ))

    class Meta:
        model = UserModel
        fields = ['email', 'password']


class NoteAddForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                         'placeholder': 'Enter note name'}))
    description = forms.CharField(min_length=5, max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                                'placeholder': 'Enter a description'}))

    class Meta:
        model = NoteModel
        fields = ['name', 'description']
