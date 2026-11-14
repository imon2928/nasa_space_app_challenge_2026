from django.db import models
from django.contrib.auth.models import User


class AstronautProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    astronaut_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default="Mission Specialist")

    # Personal Baseline Benchmarks (NASA WinSCAT / PVT Standard)
    baseline_rxn_ms = models.FloatField(default=280.0)  # Individual baseline latency
    baseline_memory_acc = models.FloatField(default=95.0)

    def __str__(self):
        return f"{self.full_name} ({self.astronaut_id})"


class DailyNeuroCheck(models.Model):
    astronaut = models.ForeignKey(AstronautProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    mission_environment = models.CharField(max_length=50, default="Space Station (ISS)")

    # Reaction & Behavioral Metrics
    mean_rxn_ms = models.FloatField()
    rxn_deviation_pct = models.FloatField()  # Deviation from personal baseline
    pvt_lapses = models.IntegerField(default=0)  # >500ms responses (NASA PVT standard)

    # EEG Spectral Band Powers (uV^2 / Hz)
    delta_uv = models.FloatField(default=12.0)
    theta_uv = models.FloatField(default=18.0)
    alpha_uv = models.FloatField(default=38.0)
    beta_uv = models.FloatField(default=20.0)
    gamma_uv = models.FloatField(default=8.0)
    alpha_peak_hz = models.FloatField(default=10.2)

    # 8 Core Cognitive Indicators (For Current, 7-Day & 30-Day Dynamic Charts)
    attention_score = models.IntegerField(default=80)
    memory_score = models.IntegerField(default=80)
    sleep_score = models.IntegerField(default=80)
    decision_score = models.IntegerField(default=80)
    focus_score = models.IntegerField(default=80)
    sensory_score = models.IntegerField(default=80)
    concentration_score = models.IntegerField(default=80)
    mood_status = models.CharField(max_length=50, default="Positive")

    # Measured & Calculated Neuro Health
    eeg_condition = models.CharField(max_length=150)
    neuro_health_score = models.IntegerField()
    overall_risk_pct = models.IntegerField(default=15)
    mission_readiness = models.CharField(max_length=100)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.astronaut.astronaut_id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"