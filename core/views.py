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
    # আপনার ডকুমেন্টের ৫টি ব্রেইন ওয়েভের নিখুঁত ডাটাবেজ
    eeg_database = [
        # 1. DELTA WAVE (0.5 – 4 Hz)
        {
            "condition": "Delta Dominance (Deep Sleep / Recovery)",
            "dominant_freq": "2.5 Hz (Delta)",
            "neuro_score": 90,
            "attention_score": 10, "attention_desc": "Unconscious / Non-responsive state",
            "memory_score": 30, "memory_desc": "Offline (Background Consolidation)",
            "sleep_score": 98, "sleep_desc": "Optimal Restorative Deep Sleep (Stage-3 NREM)",
            "decision_score": 0, "decision_desc": "Non-functional (Zero active processing capacity)",
            "focus_score": 0, "focus_desc": "Absent (No active external focus)",
            "mood_status": "Restful 😴", "mood_desc": "Complete physical relaxation & baseline recovery",
            "sensory_score": 10, "sensory_desc": "Fully relaxed with inactive motor reflexes",
            "concentration_score": 0, "concentration_desc": "Absent",
            "delta_uv": 65, "theta_uv": 15, "alpha_uv": 10, "beta_uv": 5, "gamma_uv": 2,
            "fatigue_risk": "Low", "cognitive_risk": "Low", "eva_readiness": "Off-Duty",
            "recommendation": "Off-Duty / Rest Period. Maintain uninterrupted sleep window. Avoid abrupt wake-ups during high Delta phase."
        },
        # 2. THETA WAVE (4 – 8 Hz)
        {
            "condition": "Theta Dominance (High Neuro-Fatigue)",
            "dominant_freq": "5.8 Hz (Theta)",
            "neuro_score": 48,
            "attention_score": 42, "attention_desc": "Internalized / Wandering attention",
            "memory_score": 60, "memory_desc": "Slow active processing; high intuitive neural access",
            "sleep_score": 40, "sleep_desc": "High daytime Theta indicates severe sleep debt",
            "decision_score": 52, "decision_desc": "Intuition-driven; prone to delayed operational errors",
            "focus_score": 45, "focus_desc": "Diffuse or dreamy focus (Daydreaming state)",
            "mood_status": "Fatigued 🥱", "mood_desc": "Deep tranquility or mental detachment / apathy",
            "sensory_score": 50, "sensory_desc": "Sluggish proprioception & delayed reflex coordination",
            "concentration_score": 41, "concentration_desc": "Low concentration; highly susceptible to microsleeps",
            "delta_uv": 20, "theta_uv": 58, "alpha_uv": 15, "beta_uv": 10, "gamma_uv": 4,
            "fatigue_risk": "High", "cognitive_risk": "Moderate", "eva_readiness": "Hold / Caution",
            "recommendation": "SUSPEND CRITICAL DUTIES: Suspend high-risk EVA or docking maneuvers. Execute a mandatory 20-min power nap or binaural-beat therapy."
        },
        # 3. ALPHA WAVE (8 – 12 Hz)
        {
            "condition": "Alpha Synchrony (Nominal / Calm Alertness)",
            "dominant_freq": "10.2 Hz (Alpha)",
            "neuro_score": 84,
            "attention_score": 82, "attention_desc": "Relaxed vigilance (Passive readiness)",
            "memory_score": 96, "memory_desc": "Balanced and stable baseline memory retention",
            "sleep_score": 78, "sleep_desc": "Optimal sleep-onset state (Transition phase)",
            "decision_score": 81, "decision_desc": "Calm, deliberate, and emotionally balanced decision-making",
            "focus_score": 79, "focus_desc": "Smooth, flexible focus (Task-transition friendly)",
            "mood_status": "Positive 😊", "mood_desc": "Emotionally stable and low-stress state",
            "sensory_score": 84, "sensory_desc": "Smooth, recalibrated sensorimotor coordination",
            "concentration_score": 88, "concentration_desc": "Sustainable, fatigue-free concentration over long duration",
            "delta_uv": 12, "theta_uv": 18, "alpha_uv": 38, "beta_uv": 20, "gamma_uv": 8,
            "fatigue_risk": "Low", "cognitive_risk": "Low", "eva_readiness": "Ready (Nominal)",
            "recommendation": "Mission Ready: Ideal for routine Intravehicular Activities (IVA), payload maintenance, and communication. Maintain hydration."
        },
        # 4. BETA WAVE (12 – 30 Hz)
        {
            "condition": "Beta Dominance (Active Cognition / High Task)",
            "dominant_freq": "22.5 Hz (Beta)",
            "neuro_score": 75,
            "attention_score": 88, "attention_desc": "Active, externally directed attention",
            "memory_score": 85, "memory_desc": "Fast, active working memory & data manipulation",
            "sleep_score": 45, "sleep_desc": "Poor (High nocturnal Beta causes insomnia)",
            "decision_score": 84, "decision_desc": "Fast logical problem-solving (Risk of impulsive choices)",
            "focus_score": 86, "focus_desc": "High task-oriented, analytical focus",
            "mood_status": "Alert / Hyper ⚡", "mood_desc": "Highly alert (Risk of acute stress or hyper-arousal)",
            "sensory_score": 89, "sensory_desc": "Rapid, hyper-reactive motor reflexes",
            "concentration_score": 90, "concentration_desc": "Intense, sharp concentration for task execution",
            "delta_uv": 8, "theta_uv": 12, "alpha_uv": 18, "beta_uv": 48, "gamma_uv": 15,
            "fatigue_risk": "Moderate", "cognitive_risk": "Low", "eva_readiness": "Active High-Task",
            "recommendation": "Active High-Task Operations: Excellent for critical diagnostics and manual alignment. If Beta persists >2 hrs, practice breathing exercises."
        },
        # 5. GAMMA WAVE (30 – 100 Hz)
        {
            "condition": "Gamma Peak Performance (Flow State)",
            "dominant_freq": "40.0 Hz (Gamma)",
            "neuro_score": 98,
            "attention_score": 98, "attention_desc": "Ultra-sharp, hyper-vigilant attention",
            "memory_score": 99, "memory_desc": "Maximum efficiency; multi-sensory complex data integration",
            "sleep_score": 0, "sleep_desc": "Fully awake state (Inapplicable to sleep)",
            "decision_score": 96, "decision_desc": "Complex executive problem-solving & rapid pattern recognition",
            "focus_score": 98, "focus_desc": "Peak Flow State / Hyper-concentration",
            "mood_status": "Peak Flow 🔥", "mood_desc": "Heightened awareness, peak mental clarity & confidence",
            "sensory_score": 97, "sensory_desc": "Highly precise, synchronized sensorimotor integration",
            "concentration_score": 99, "concentration_desc": "Maximum cognitive concentration",
            "delta_uv": 5, "theta_uv": 8, "alpha_uv": 12, "beta_uv": 25, "gamma_uv": 50,
            "fatigue_risk": "Low", "cognitive_risk": "Very Low", "eva_readiness": "Peak Clearance (EVA Ready)",
            "recommendation": "Peak Performance Clearance: Prime window for high-risk EVAs, orbital docking simulations, or emergency response maneuvers."
        }
    ]
    
    if request.method == "POST":
        selected_eeg = random.choice(eeg_database)
        request.session['current_eeg'] = selected_eeg
        return redirect('dashboard')
        
    return render(request, 'eeg_test.html')


@login_required(login_url='login')
def metrics_view(request):
    context = {
        'heart_rate': 74,
        'spo2': 98,
        'body_temp': 36.8,
        'stress_level': 'Low',
    }
    return render(request, 'metrics.html', context)


@login_required(login_url='login')
def risk_view(request):
    eeg = request.session.get('current_eeg', None)
    
    context = {
        'has_tested': True if eeg else False,
        'eeg': eeg,
    }
    return render(request, 'risk.html', context)


@login_required(login_url='login')
def settings_view(request):
    return render(request, 'settings.html')

@login_required(login_url='login')
def recommendations_view(request):
    eeg = request.session.get('current_eeg', None)
    
    # টেস্ট দেওয়া না থাকলে ডিফল্ট একটা আলফা প্রোটোকল সেট থাকবে
    if not eeg:
        eeg = {
            "condition": "Alpha Synchrony (Nominal State)",
            "dominant_freq": "10.2 Hz (Alpha)",
            "neuro_score": 84,
            "fatigue_risk": "Low",
            "recommendation": "Continue current routine. Maintain hydration, regular breaks and light exposure as per schedule."
        }
        
    context = {
        'eeg': eeg,
        'has_tested': True if request.session.get('current_eeg') else False
    }
    return render(request, 'recommendations.html', context)