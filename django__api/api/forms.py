from django.forms import ModelForm
from app.models import Profile


# Form for updating the users profile
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'gender', 'bio')

