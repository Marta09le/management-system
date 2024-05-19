from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserModel, GroupModel, NoteModel


# Форма реєстрації користувача
class UserRegisterForm(forms.ModelForm):
    # Поле для введення імені користувача
    first_name = forms.CharField(min_length=2, max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control py-4',
                                            'placeholder': 'Enter your first name'}))
    # Поле для введення прізвища користувача
    last_name = forms.CharField(min_length=2, max_length=30,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control py-4',
                                           'placeholder': 'Enter your last name'}))
    # Поле для введення пароля
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Enter your password'}))
    # Поле для вибору групи
    group = forms.ModelChoiceField(
        queryset=GroupModel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label="Select your group"
    )

    # Мета-клас для налаштувань форми
    class Meta:
        # Вказуємо модель, з якою буде працювати форма
        model = UserModel
        # Поля моделі, які будуть використовуватися у формі
        fields = ['first_name', 'last_name', 'email', 'password', 'group']
        # Поля, які будуть виключені з форми
        exclude = ['created']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control py-4',
                                             'placeholder': 'Enter your email'}),

        }

# Форма реєстрації менеджера
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

    # Мета-клас для налаштувань форми
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'password']
        exclude = ['created','group']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control py-4',
                                             'placeholder': 'Enter your email'}),

        }

# Форма для додавання групи
class GroupAddForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                         'placeholder': 'Enter event name'}))
    # Поле для введення опису групи
    description = forms.CharField(min_length=5, max_length=20,
                                  widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                                'placeholder': 'Enter a description'}))

    # Мета-клас для налаштувань форми
    class Meta:
        model = GroupModel
        fields = ['name', 'description']
        exclude = ['users_count']

# Форма для входу користувача
class UserLoginForm(AuthenticationForm):
    # Поле для введення електронної пошти
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True,
            'autocomplete': 'email'  # Add autocomplete attribute for username
        }
    ))
    # Поле для введення пароля
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
    # Поле для введення опису нотатки
    description = forms.CharField(min_length=5, max_length=50,
                                  widget=forms.TextInput(attrs={'class': 'form-control py-4',
                                                                'placeholder': 'Enter a description'}))

    # Мета-клас для налаштувань форми
    class Meta:
        model = NoteModel
        fields = ['name', 'description']
