from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TA, Availability
from .forms import AvailabilityForm, TACreationForm, SignupForm
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic import CreateView

def ta_dashboard(request):
    selected_grade = request.GET.get('grade', '')
    ta_index = int(request.GET.get('ta_index', 0))
    
    if selected_grade:
        ta_list = TA.objects.filter(grades__contains=selected_grade)
    else:
        ta_list = TA.objects.all()
        
    if ta_index < 0:
        ta_index = max(0, len(ta_list) - 1)
    elif ta_index >= len(ta_list) and len(ta_list) > 0:
        ta_index = 0

    current_ta = ta_list[ta_index] if ta_list.exists() else None
    
    schedule = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
    if current_ta:
        slots = current_ta.availabilities.all()
        for slot in slots:
            if slot.day in schedule:
                schedule[slot.day].append(slot)

    context = {
        'current_ta': current_ta,
        'schedule': schedule,
        'ta_index': ta_index,
        'prev_index': ta_index - 1,
        'next_index': ta_index + 1,
        'selected_grade': selected_grade,
        'grades_list': ['9', '10', '11', '12'],
    }
    return render(request, 'tutoring/home.html', context)

def ta_detail(request, pk):
    ta = get_object_or_404(TA, pk=pk)
    return render(request, 'tutoring/ta_detail.html', {'ta': ta})

@login_required
def edit_availability(request):
    is_master = request.user.is_superuser
    ta = getattr(request.user, 'ta', None)
    
    #if not is_master:
    #   messages.error(request, "You don't have a TA profile.")
    #    return redirect('ta_dashboard')

    ta_form = TACreationForm() if is_master else None
    slot_form = AvailabilityForm(user=request.user, initial={'ta': ta} if ta else None)

    if request.method == 'POST':
        if 'create_ta' in request.POST and is_master:
            ta_form = TACreationForm(request.POST)
            if ta_form.is_valid():
                ta_form.save()
                return redirect('edit_availability')
        elif 'add_availability' in request.POST:
            slot_form = AvailabilityForm(request.POST, user=request.user)
            if slot_form.is_valid():
                slot_form.save()
                return redirect('ta_dashboard')

    context = {
        'ta_form': ta_form,
        'slot_form': slot_form,
        'is_master': is_master,
    }
    return render(request, 'tutoring/edit_availability.html', context)

@login_required
def delete_availability(request, pk):
    slot = get_object_or_404(Availability, pk=pk)
    if request.user.is_superuser or (hasattr(request.user, 'ta') and slot.ta == request.user.ta):
        slot.delete()
    return redirect('ta_dashboard')

@login_required
def delete_ta(request, pk):
    if request.user.is_superuser:
        ta = get_object_or_404(TA, pk=pk)
        ta.delete()
    return redirect('ta_dashboard')

class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"