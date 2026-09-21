from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        astronaut_id = request.POST.get("astronaut_id")
        password = request.POST.get("password")
        user = authenticate(request, username=astronaut_id, password=password)
        if user is not None:
            login(request, user)
            request.session['astronaut_id'] = astronaut_id
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Astronaut ID or Key!")

    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        astronaut_id = request.POST.get("astronaut_id")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        if User.objects.filter(username=astronaut_id).exists():
            messages.error(request, "Astronaut ID already registered!")
            return render(request, 'register.html')

        user = User.objects.create_user(username=astronaut_id, password=password)
        login(request, user)
        request.session['astronaut_id'] = astronaut_id
        return redirect('dashboard')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    # সেশনে ইইজি টেস্টের ডাটা আছে কিনা চেক করা
    eeg = request.session.get('current_eeg', None)
    rxn = request.session.get('current_rxn', 280.0)
    
    context = {
        'eeg': eeg,
        'rxn': rxn,
        'has_tested': True if eeg else False
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def reaction_test(request):
    if request.method == "POST":
        rxn_time = float(request.POST.get("avg_rxn_time", 280.0))
        sleep_hours = float(request.POST.get("sleep_hours", 7.5))
        stress_level = int(request.POST.get("stress_level", 3))
        
        request.session['current_rxn'] = rxn_time
        request.session['sleep_hours'] = sleep_hours
        request.session['stress_level'] = stress_level
        return redirect('eeg_test')
        
    return render(request, 'reaction_test.html')

@login_required(login_url='login')
def eeg_test(request):
    eeg_database = [
        # ALPHA WAVE (OPTIMAL)
        {
            "condition": "Alpha Synchrony (Nominal State)",
            "dominant_freq": "10.2 Hz (Alpha)",
            "neuro_score": 84,
            "attention_score": 82, "attention_desc": "Calm Alertness / Passive Readiness",
            "memory_score": 96, "memory_desc": "Optimal Working Memory Efficiency",
            "sleep_score": 78, "sleep_desc": "Restful / Normal Pre-Sleep Transition",
            "decision_score": 81, "decision_desc": "Deliberate & Balanced Precision (240ms)",
            "focus_score": 79, "focus_desc": "Smooth & Flexible Focus",
            "mood_status": "Positive 😊", "mood_desc": "Emotionally Stable & Low Stress",
            "sensory_score": 84, "sensory_desc": "Normal Parietal Adaptation & Reflexes",
            "concentration_score": 88, "concentration_desc": "Sustainable & Fatigue-Free Concentration",
            "delta_uv": 12, "theta_uv": 18, "alpha_uv": 32, "beta_uv": 24, "gamma_uv": 10,
            "fatigue_risk": "Low", "cognitive_risk": "Low", "eva_readiness": "Ready",
            "recommendation": "Continue current routine. Maintain hydration, regular breaks and light exposure as per schedule."
        },
        # THETA WAVE (HIGH FATIGUE)
        {
            "condition": "Theta Dominance (High Neuro-Fatigue)",
            "dominant_freq": "5.8 Hz (Theta)",
            "neuro_score": 48,
            "attention_score": 42, "attention_desc": "Internalized / Wandering Attention",
            "memory_score": 60, "memory_desc": "Slow Active Working Memory Processing",
            "sleep_score": 40, "sleep_desc": "High Daytime Sleep Debt Detected",
            "decision_score": 52, "decision_desc": "Delayed Latency / Error Prone (>400ms)",
            "focus_score": 45, "focus_desc": "Diffuse / Daydreaming State",
            "mood_status": "Fatigued 🥱", "mood_desc": "High Cognitive Exhaustion Risk",
            "sensory_score": 50, "sensory_desc": "Sluggish Proprioception & Motor Reflexes",
            "concentration_score": 41, "concentration_desc": "High Microsleep & Lapse Susceptibility",
            "delta_uv": 25, "theta_uv": 65, "alpha_uv": 18, "beta_uv": 12, "gamma_uv": 5,
            "fatigue_risk": "High", "cognitive_risk": "Moderate", "eva_readiness": "Hold",
            "recommendation": "SUSPEND CRITICAL DUTIES: Execute a mandatory 20-45 min power nap or 15-min Binaural-Beat therapy immediately."
        }
    ]
    
    if request.method == "POST":
        selected_eeg = random.choice(eeg_database)
        request.session['current_eeg'] = selected_eeg
        return redirect('dashboard')
        
    return render(request, 'eeg_test.html')