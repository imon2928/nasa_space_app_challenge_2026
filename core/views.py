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
    if 'astronaut_id' not in request.session:
        return redirect('login')
        
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
        # 1. DELTA WAVE
        {
            "condition": "Delta Wave Dominance (Deep Restorative Sleep)",
            "image": "images/eeg1.png",
            "eeg_data": {
                "dominant_freq": "2.1 Hz (Range: 0.5 - 4.0 Hz Delta)",
                "amplitude": "110 µV (High Voltage)",
                "montage": "10-20 Standard (Occipital-Parietal Shift)",
                "alpha_power": "8%", "beta_power": "5%", "theta_power": "12%", "delta_power": "75%",
                "beta_theta_ratio": "0.41 (Deep Sleep Recovery)"
            },
            "brain_performance": "20% (Rest & Recovery Mode)",
            "attention": "Unconscious / Non-Responsive State",
            "focus": "Absent (No Active External Focus)",
            "memory": "Offline (Background Memory Consolidation Active)",
            "mood": "Complete Relaxation & Baseline Neural Recovery",
            "sleep_index": "Optimal Restorative Deep Sleep (Stage-3 NREM)",
            "sensory_motor": "Fully Relaxed & Inactive Motor Reflexes",
            "decision_speed": "Non-Functional (Zero Processing Capacity)",
            "concentration": "Absent (Unconscious State)",
            "guideline": """1. Operational Status: Off-Duty / Rest Period.
2. Maintain uninterrupted sleep in noise-shielded crew quarters.
3. Avoid abrupt wake-ups during high Delta phases to prevent sleep inertia."""
        },

        # 2. THETA WAVE
        {
            "condition": "Theta Wave Dominance (High Neuro-Fatigue Alert)",
            "image": "images/eeg2.png",
            "eeg_data": {
                "dominant_freq": "5.8 Hz (Range: 4.0 - 8.0 Hz Theta)",
                "amplitude": "82 µV (Elevated)",
                "montage": "10-20 Frontal-Central (Cz, Fz)",
                "alpha_power": "18%", "beta_power": "12%", "theta_power": "55%", "delta_power": "15%",
                "beta_theta_ratio": "0.21 (Critical Fatigue Alert)"
            },
            "brain_performance": "45% (Critical Fatigue)",
            "attention": "Internalized / Wandering Attention",
            "focus": "Diffuse / Daydreaming State",
            "memory": "Slow Active Processing (Intuitive Access)",
            "mood": "Mentally Detached / High Exhaustion",
            "sleep_index": "Light Sleep / Daytime Sleep Debt Alert",
            "sensory_motor": "Sluggish Proprioception & Delayed Reflexes",
            "decision_speed": "Delayed & Prone to Operational Errors (>400ms)",
            "concentration": "Low / High Microsleep Risk",
            "guideline": """1. SUSPEND CRITICAL DUTIES: Defer high-risk EVAs or robotic arm operations immediately.
2. MANDATORY NEURO-REST: Execute a 20 to 45-minute power nap or apply 15-min Binaural-Beat Neuro-Stimulation.
3. CIRCADIAN LIGHT THERAPY: Expose astronaut to blue-enriched light (460-480nm) to suppress Theta dominance.
4. PHYSIOLOGICAL REGULATION: Initiate 5-min autonomic breathing exercises and ensure hydration compliance."""
        },

        # 3. ALPHA WAVE
        {
            "condition": "Optimal Alpha Wave Dominance (Calm Alertness)",
            "image": "images/eeg3.png",
            "eeg_data": {
                "dominant_freq": "10.2 Hz (Range: 8.0 - 12.0 Hz Alpha)",
                "amplitude": "45 µV (Nominal)",
                "montage": "10-20 Standard (F3-C3, F4-C4)",
                "alpha_power": "60%", "beta_power": "20%", "theta_power": "12%", "delta_power": "8%",
                "beta_theta_ratio": "1.66 (Optimal Focus)"
            },
            "brain_performance": "94% (High Efficiency)",
            "attention": "Calm Alertness / Passive Readiness",
            "focus": "Smooth & Flexible Focus",
            "memory": "Optimal Working Memory (96% Efficiency)",
            "mood": "Positive, Emotionally Stable & Low Stress",
            "sleep_index": "Restful / Nominal Pre-Sleep Transition",
            "sensory_motor": "Normal Parietal Adaptation & Smooth Reflexes",
            "decision_speed": "Deliberate & Balanced Precision (240ms)",
            "concentration": "Sustainable & Fatigue-Free Concentration",
            "guideline": """1. Operational Status: Nominal / Mission Ready.
2. Action Plan: Ideal state for routine Intravehicular Activities (IVA).
3. Maintain baseline circadian hydration and standard lighting."""
        },

        # 4. BETA WAVE
        {
            "condition": "Beta Wave Dominance (Active Cognition & High Workload)",
            "image": "images/eeg1.png",
            "eeg_data": {
                "dominant_freq": "22.4 Hz (Range: 12.0 - 30.0 Hz Beta)",
                "amplitude": "55 µV (Active)",
                "montage": "10-20 Frontal Lead High Power",
                "alpha_power": "15%", "beta_power": "58%", "theta_power": "15%", "delta_power": "12%",
                "beta_theta_ratio": "3.86 (High Workload)"
            },
            "brain_performance": "82% (Active Processing)",
            "attention": "Active External / Highly Responsive Attention",
            "focus": "High Task-Oriented Analytical Focus",
            "memory": "Rapid Working Memory & Data Processing",
            "mood": "Alert (Risk of Acute Stress/Anxiety if prolonged)",
            "sleep_index": "Poor / Risk of Insomnia & High Cortisol",
            "sensory_motor": "Hyper-Reactive Motor Reflexes",
            "decision_speed": "Fast & Logical Problem-Solving",
            "concentration": "Intense & Sharp Concentration",
            "guideline": """1. Operational Status: Active High-Task Operations.
2. Action Plan: Excellent state for critical diagnostics and manual docking.
3. If hyper-arousal persists >2 hours, perform 5-min breathing exercise."""
        },

        # 5. GAMMA WAVE
        {
            "condition": "Gamma Wave Coherence (Peak Mental Performance)",
            "image": "images/eeg2.png",
            "eeg_data": {
                "dominant_freq": "42.5 Hz (Range: 30.0 - 100.0 Hz Gamma)",
                "amplitude": "35 µV (High Synchrony)",
                "montage": "10-20 Full Cortical Synchronization",
                "alpha_power": "20%", "beta_power": "25%", "theta_power": "5%", "delta_power": "5%",
                "beta_theta_ratio": "5.00 (Peak Cognition)"
            },
            "brain_performance": "99% (Peak Flow State)",
            "attention": "Ultra-Sharp / Hyper-Vigilant Attention",
            "focus": "Peak Flow State / Hyper-Concentration",
            "memory": "Maximum Working Memory Efficiency (99%)",
            "mood": "Heightened Awareness & High Cognitive Clarity",
            "sleep_index": "Fully Wakeful State (Non-Sleep Phase)",
            "sensory_motor": "Highly Synchronized Sensorimotor Integration",
            "decision_speed": "Ultra-Fast Complex Problem Solving",
            "concentration": "Maximum Cognitive Concentration",
            "guideline": """1. Operational Status: Peak Operational Clearance.
2. Action Plan: Prime window for high-risk operations (EVA, emergency protocol).
3. Log cognitive telemetry into NASA HRP dataset to track performance duration."""
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
        
    rxn = request.session.get('current_rxn', 290.0)
    sleep_hours = request.session.get('sleep_hours', 7.5)
    stress_level = request.session.get('stress_level', 3)
    eeg = request.session.get('current_eeg')
    
    profile = getattr(request.user, 'astronautprofile', None)
    baseline_rxn = profile.baseline_rxn_ms if profile else 280.0
    rxn_deviation = round(((rxn - baseline_rxn) / baseline_rxn) * 100, 1)
    
    neuro_score = 100
    if rxn_deviation > 25.0:
        neuro_score -= 30
    elif rxn_deviation > 10.0:
        neuro_score -= 15
        
    if sleep_hours < 6.0:
        neuro_score -= 20
    if stress_level > 6:
        neuro_score -= 15
        
    if "Theta" in eeg['condition'] or "Delta" in eeg['condition']:
        neuro_score -= 20
        
    neuro_score = max(neuro_score, 15)
    
    if neuro_score >= 80:
        readiness = "NOMINAL: CLEARED FOR HIGH-RISK IVA/EVA"
        readiness_class = "success"
    elif 55 <= neuro_score < 80:
        readiness = "CAUTION: COGNITIVE DEVIATION DETECTED"
        readiness_class = "warning"
    else:
        readiness = "CRITICAL: MANDATORY NEURO-REST PROTOCOL INITIATED"
        readiness_class = "danger"

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