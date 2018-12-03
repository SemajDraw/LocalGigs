import django.forms as forms
from django.forms import ModelForm
from app.models import Profile


# Adds the first name and last name to the django all-auth template defined in settings
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


# Form to upload profile pic
class ProfilePicForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture',)


# Form to update profile
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'bio', 'gender')


# Form to upload profile pic
class InterestedHTMLForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('interested_html',)
