from django import forms

from todolist.models import Account, Room


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', min_length=3, max_length=30, help_text='Required'
    )
    email = forms.EmailField(
        max_length=60, help_text='Required', error_messages={
            'required': 'Sorry, you will need an email'
        }
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        users = Account.objects.filter(username=username)
        if users.count():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that is already taken.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'}
        )

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'}
        )


class RoomUpdateForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = Room
        fields = ('name', 'info', 'password')


class RoomEnterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Room
        fields = ('password',)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
