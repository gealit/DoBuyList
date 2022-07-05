from django import forms

from todolist.models import Room


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
