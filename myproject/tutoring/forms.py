from django import forms
from .models import Availability, TA, User
from django.contrib.auth.forms import UserCreationForm

class TACreationForm(forms.ModelForm):
    class Meta:
        model = TA
        fields = ['name', 'bio', 'grades']
        widgets = {
            'grades': forms.TextInput(attrs={'placeholder': 'e.g., 9,10,11'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['ta', 'day', 'time_slot']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['ta'].queryset = TA.objects.filter(user=user)

class SignupForm(UserCreationForm):
    grade_choices = [
        ('', ''),
        ('9th', '9th'),
        ('10th', '10th'),
        ('11th', '11th'),
        ('12th', '12th'),
    ]
    grade = forms.ChoiceField(choices=grade_choices, required=True, label="Grade")
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "grade",
        )