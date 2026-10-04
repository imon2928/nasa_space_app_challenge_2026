import base64
import logging
import random
import os
import sys
import cv2
import numpy as np
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .face_auth import REQUIRED_HITS, get_face_info, recognize_face
from .models import AstronautProfile, DailyNeuroCheck

logger = logging.getLogger(__name__)

def get_absolute_path(relative_path):
    """PyInstaller (.exe) এবং সাধারণ ডেভেলপমেন্ট দুই ক্ষেত্রেই সঠিক পাথ খুঁজে নেওয়ার ফাংশন"""
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def login_view(request):
    """লগইন ইন্টারফেস বন্ধ রাখা কিন্তু গেস্ট মোডের পেইজ রেন্ডার করা"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        return JsonResponse({
            'success': False,
            'fatal': True,
            'message': 'BIOMETRIC LOGIN IS CURRENTLY DISABLED'
        })

    return render(request, 'login.html')

def guest_login_view(request):
    """গেস্ট একাউন্ট দিয়ে লগইন করিয়ে সরাসরি ড্যাশবোর্ডে রিডাইরেক্ট করা"""
    guest_user, created = User.objects.get_or_create(username="Guest_Astronaut")
    if created:
        guest_user.set_unusable_password()
        guest_user.save()

    profile, _ = AstronautProfile.objects.get_or_create(
        user=guest_user,
        defaults={"astronaut_id": "Guest", "full_name": "Guest Astronaut", "role": "Visiting Specialist"}
    )

    login(request, guest_user)
    request.session['astronaut_id'] = profile.astronaut_id
    request.session['full_name'] = profile.full_name
    return redirect('dashboard')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

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
            full_name=full_name,
            role="Mission Specialist"
        )

        login(request, user)
        request.session['astronaut_id'] = astronaut_id
        request.session['full_name'] = full_name
        return redirect('dashboard')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    try:
        profile = request.user.astronautprofile
    except AstronautProfile.DoesNotExist:
        profile = None

    eeg = request.session.get('current_eeg', None)
    rxn = request.session.get('current_rxn', profile.baseline_rxn_ms if profile else 280.0)

    context = {
        'profile': profile,
        'eeg': eeg,
        'rxn': rxn,
        'has_tested': True if eeg else False
    }
    context['face_info'] = get_face_info(profile.astronaut_id) if profile else None
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
            "recommendation": "Off-Duty / Rest Period. Maintain uninterrupted sleep window."
        },
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
            "recommendation": "SUSPEND CRITICAL DUTIES: Execute a mandatory 20-min power nap or binaural-beat therapy."
        },
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
            "recommendation": "Mission Ready: Ideal for routine Intravehicular Activities (IVA) and payload maintenance."
        },
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
            "recommendation": "Active High-Task Operations: Excellent for critical diagnostics and manual alignment."
        },
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
            "recommendation": "Peak Performance Clearance: Prime window for high-risk EVAs and orbital docking simulations."
        }
    ]

    if request.method == "POST":
        selected_eeg = random.choice(eeg_database)
        request.session['current_eeg'] = selected_eeg

        try:
            profile = request.user.astronautprofile
            rxn = request.session.get('current_rxn', profile.baseline_rxn_ms)
            deviation = ((rxn - profile.baseline_rxn_ms) / profile.baseline_rxn_ms) * 100

            DailyNeuroCheck.objects.create(
                astronaut=profile,
                mean_rxn_ms=rxn,
                rxn_deviation_pct=round(deviation, 2),
                eeg_condition=selected_eeg['condition'],
                neuro_health_score=selected_eeg['neuro_score'],
                mission_readiness=selected_eeg['eva_readiness']
            )
        except Exception as e:
            print("DailyNeuroCheck Save Error:", e)

        return redirect('dashboard')

    return render(request, 'eeg_test.html')

@login_required(login_url='login')
def metrics_view(request):
    eeg = request.session.get('current_eeg', None)

    if eeg:
        high_beta = eeg.get('beta_uv', 24)
        heart_rate = 72 + int(high_beta * 0.5)
        spo2 = 98 if high_beta < 30 else 96
        body_temp = 36.8

        if high_beta > 35:
            stress_level = "HIGH"
        elif high_beta > 22:
            stress_level = "MODERATE"
        else:
            stress_level = "LOW"
    else:
        heart_rate = 84
        spo2 = 98
        body_temp = 36.6
        stress_level = "LOW"

    context = {
        'heart_rate': heart_rate,
        'spo2': spo2,
        'body_temp': body_temp,
        'stress_level': stress_level,
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