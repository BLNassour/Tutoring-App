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
    days = forms.MultipleChoiceField(
        choices=Availability.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label="Days",
    )

    field_order = ['ta', 'days', 'time_slot']
    class Meta:
        model = Availability
        fields = ['ta', 'time_slot']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['ta'].queryset = TA.objects.filter(user=user)

    def save(self):
        ta = self.cleaned_data['ta']
        time_slot = self.cleaned_data['time_slot']
        slots = []
        for day in self.cleaned_data['days']:
            slot, _ = Availability.objects.get_or_create(
                ta=ta, day=day, time_slot=time_slot
            )
            slots.append(slot)
        return slots

class SignupForm(UserCreationForm):
    grade_choices = [
        ('9', '9th'),
        ('10', '10th'),
        ('11', '11th'),
        ('12', '12th'),
    ]
    grade = forms.MultipleChoiceField(choices=grade_choices, widget=forms.CheckboxSelectMultiple, required=True, label="Grades")
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell students about the subjects you study and how they can contact you.'}),
        required=False,
        label="Bio",
    )
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            TA.objects.update_or_create(
                user=user,
                defaults={
                    "name": user.username,
                    "grades": ",".join(self.cleaned_data["grade"]),
                    "bio": self.cleaned_data["bio"],
                },
            )
        return user