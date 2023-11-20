from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'autofocus': True,
            'type': 'email',
            'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Email'
        })
        self.fields['password'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Пароль'
        })


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'autofocus': True,
            'type': 'email',
            'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Пароль'
        })

        self.fields['password2'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Подтверждение пароля'
        })
