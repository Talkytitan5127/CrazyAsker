from django import forms

from asker.models import Profile


class ProfileForm(forms.Form):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'id': 'customFile'
                }
        )
    )

    class Meta:
        model = Profile
        fields = ('avatar')


    def __init__(self, client, *args, **kwargs):
        self._user = client
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        profile = self._user.profile
        picture = self.cleaned_data['avatar']
        profile.avatar = picture
        profile.save()
