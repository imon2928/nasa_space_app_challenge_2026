from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AstronautProfile, DailyNeuroCheck
import random
import time

def login_view(request):
    if request.user.is_authenticated:
        return redirect('reaction_test')

    if request.method == "POST":
        astronaut_id = request.POST.get("astronaut_id")
        password = request.POST.get("password")

        # ১. Django User Authenticate checking
        user = authenticate(request, username=astronaut_id, password=password)
        
        if user is not None:
            login(request, user)
            request.session['astronaut_id'] = astronaut_id
            return redirect('reaction_test')
        else:
            messages.error(request, "Invalid Astronaut ID or Security Key! Please check credentials or Sign Up.")

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('reaction_test')

    if request.method == "POST":
        astronaut_id = request.POST.get("astronaut_id")
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        if User.objects.filter(username=astronaut_id).exists():
            messages.error(request, "Astronaut ID already registered!")
            return render(request, 'register.html')

        # নতুন অ্যাকাউন্ট ও প্রোফাইল তৈরি
        user = User.objects.create_user(username=astronaut_id, password=password)
        AstronautProfile.objects.create(
            user=user,
            astronaut_id=astronaut_id,
            full_name=full_name
        )
        
        login(request, user)
        request.session['astronaut_id'] = astronaut_id
        messages.success(request, "Registration successful! Welcome to Mission Control.")
        return redirect('reaction_test')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')


@login_required(login_url='login')
def reaction_test(request):
    if request.method == "POST":
        rxn_time = float(request.POST.get("avg_rxn_time", 280))
        request.session['current_rxn'] = rxn_time
        return redirect('eeg_test')
        
    return render(request, 'reaction_test.html')


@login_required(login_url='login')
def eeg_test(request):
    eeg_database = [
        {
            "condition": "Optimal Alpha-Dominant Cortical Synchrony",
            "eeg_data": {
                "dominant_freq": "10.2 Hz (Alpha)",
                "amplitude": "45 µV (Nominal)",
                "montage": "10-20 Standard (F3-C3, F4-C4)",
                "alpha_power": "48%",
                "beta_power": "22%",
                "theta_power": "18%",
                "delta_power": "12%",
                "beta_theta_ratio": "1.22 (Optimal Focus)"
            },
            "brain_performance": "94% (High Efficiency)",
            "sleep_index": "Restful / Nominal REM Cycles",
            "attention": "Sustained Stable Focus",
            "sensory_motor": "Normal Parietal Adaptation",
            "memory": "Optimal Working Memory (96% Efficiency)",
            "decision_speed": "Optimal Precision (240ms)",
            "mood": "Calm State & Balanced Affective Index",
            "guideline": "1. Continue scheduled intra-vehicular activities (IVA).\n2. Maintain standard hydration schedule."
        },
        {
            "condition": "High Beta & Gamma Hyper-Arousal Surge",
            "eeg_data": {
                "dominant_freq": "24.5 Hz (High Beta)",
                "amplitude": "68 µV (Elevated)",
                "montage": "10-20 Frontal Surge",
                "alpha_power": "15%",
                "beta_power": "54%",
                "theta_power": "16%",
                "delta_power": "15%",
                "beta_theta_ratio": "3.37 (Acute Stress Surge)"
            },
            "brain_performance": "68% (Elevated Strain)",
            "sleep_index": "Disrupted REM / High Cortisol",
            "attention": "Fragmented Hyper-Attention",
            "sensory_motor": "Hypersensitive Reflexes",
            "memory": "Moderate Working Memory (76% Efficiency)",
            "decision_speed": "Hyper-vigilant Speed",
            "mood": "Elevated Acute Stress & Overload",
            "guideline": "1. Initiate 5-minute guided breathing exercise.\n2. Dim cabin lighting by 20%."
        }
    ]
    
    if request.method == "POST":
        selected_outcome = random.choice(eeg_database)
        request.session['current_eeg'] = selected_outcome
        return redirect('final_report')
        
    return render(request, 'eeg_test.html')


@login_required(login_url='login')
def final_report(request):
    if 'current_eeg' not in request.session:
        return redirect('reaction_test')
        
    rxn = request.session.get('current_rxn', 280.0)
    eeg = request.session.get('current_eeg')
    
    profile = getattr(request.user, 'astronautprofile', None)
    baseline_rxn = profile.baseline_rxn_ms if profile else 280.0
    rxn_deviation = round(((rxn - baseline_rxn) / baseline_rxn) * 100, 1)
    
    neuro_score = 100
    if rxn_deviation > 25.0:
        neuro_score -= 35
    elif rxn_deviation > 10.0:
        neuro_score -= 15
        
    if "Hyper-Arousal" in eeg['condition']:
        neuro_score -= 20
        
    neuro_score = max(neuro_score, 15)
    
    if neuro_score >= 80:
        readiness = "MISSION READY (NOMINAL OPERATIONAL CLEARANCE)"
        readiness_class = "success"
    else:
        readiness = "CAUTION: COGNITIVE DEVIATION"
        readiness_class = "warning"

    context = {
        'astronaut_id': request.user.username,
        'rxn': rxn,
        'baseline_rxn': baseline_rxn,
        'rxn_deviation': rxn_deviation,
        'neuro_score': neuro_score,
        'readiness': readiness,
        'readiness_class': readiness_class,
        'eeg': eeg
    }
    return render(request, 'final_report.html', context)