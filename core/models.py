from django.db import models
from django.contrib.auth.models import User

class AstronautProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    astronaut_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default="Mission Specialist")
    
    # Personal Baseline Benchmarks
    baseline_rxn_ms = models.FloatField(default=280.0)  # Individual baseline latency
    baseline_memory_acc = models.FloatField(default=95.0)

    def __str__(self):
        return f"{self.full_name} ({self.astronaut_id})"


class DailyNeuroCheck(models.Model):
    astronaut = models.ForeignKey(AstronautProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Measured Metrics
    mean_rxn_ms = models.FloatField()
    rxn_deviation_pct = models.FloatField()  # Deviation from personal baseline
    eeg_condition = models.CharField(max_length=150)
    
    # Calculated Neuro Health
    neuro_health_score = models.IntegerField()
    mission_readiness = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.astronaut.astronaut_id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"