from django import forms
from .models import Availability, TA, Signup

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['ta', 'day', 'time_slot']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['ta'].queryset = TA.objects.filter(user=user)

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = [
            'username',
            'email',
            'grade',
            'subject',
        ]

