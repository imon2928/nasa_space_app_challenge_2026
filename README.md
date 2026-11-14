# 🚀 Neuro-Health: Astronaut Neuro-Cognitive & Sensorimotor Health Monitoring System

[![NASA Space Apps Challenge 2026](https://img.shields.io/badge/NASA%20Space%20Apps-2026-blue?style=for-the-badge&logo=nasa)](https://github.com/imon2928/nasa_space_app_challenge_2026)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MNE-Python](https://img.shields.io/badge/MNE--Python-Signal%20Processing-000000?style=for-the-badge)](https://mne.tools/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://neuro-health.onrender.com)

> **"When humanity steps into deep space, the ultimate survival technology isn't built of metal — it's the human brain inside the helmet."**

## 🌐 Live Demo

**👉 [https://neuro-health.onrender.com](https://neuro-health.onrender.com)**

> **Note:** The biometric (face) login portal is currently offline. Click **"Continue with Guest Mode"** on the login page to explore the full dashboard. The app is hosted on Render's free tier, so the first load may take 30–60 seconds while the server wakes up.

| Page | Link |
| --- | --- |
| Dashboard | [/](https://neuro-health.onrender.com/) |
| EEG Test | [/eeg-test/](https://neuro-health.onrender.com/eeg-test/) |
| Reaction Test | [/reaction-test/](https://neuro-health.onrender.com/reaction-test/) |
| Metrics | [/metrics/](https://neuro-health.onrender.com/metrics/) |
| Risk | [/risk/](https://neuro-health.onrender.com/risk/) |
| Recommendations | [/recommendations/](https://neuro-health.onrender.com/recommendations/) |
| Settings | [/settings/](https://neuro-health.onrender.com/settings/) |

---

## 📝 Description

**Neuro-Health** is a web-based, real-time neuro-cognitive monitoring platform built for astronauts on long-duration, deep-space missions. It simulates 8-channel EEG streams, measures reaction time, and turns them into a Cognitive Fatigue Index, lobe-specific brain health maps, and a live neural risk status. It then recommends NASA-style countermeasures (neuro-stimulation breaks, guided breathing, EVA holds) so the crew can **monitor, predict, prevent and perform** — even when Mission Control is minutes away.

---

## 📌 Executive Summary

During deep-space missions, astronauts endure long-term isolation, cosmic radiation (HZE particles), and microgravity ($0g$). Microgravity eliminates the $1g$ vector, shutting down otolith organ signaling in the inner ear and proprioceptive feedback from foot pressure. This induces a severe **Sensory Conflict (Neuro-Vestibular Mismatch)** in the *Vestibular Nuclei*, triggering **Space Motion Sickness (SMS)** via the evolutionary *Poison Hypothesis* (*Area Postrema* activation). Furthermore, long-term exposure causes cephalad fluid shifts, ventriculomegaly ($12–25\%$ expansion), **Spaceflight-Associated Neuro-ocular Syndrome (SANS)**, and disrupts the internal neural clock in the *Posterior Parietal Cortex* and *Basal Ganglia*, leading to critical **Cognitive Time Distortion**.

With communication delays with Earth exceeding **20 minutes** on Mars missions, real-time intervention from Ground Control is impossible. A split-second error during extravehicular activity (EVA) or docking maneuvers can prove fatal.

**Neuro-Health** by **Team NeuroNauts** is an autonomous, edge-computing predictive software platform. Anchored on NASA Open Science Data Repository (OSDR) datasets and EEG metrics, Neuro-Health delivers real-time synthetic EEG stream processing, lobe-specific neuro-health mapping, gamified cognitive time-perception recalibration, and predictive risk alerts to transition space medicine from reactive treatment to real-time neural protection.

---

## 🎯 Key Features & Core Innovations

### 1. Authentication & Instant Baseline

- **Facial Recognition Authentication**: Designed to give instant, hands-free sign-in for astronauts, fetching personalized neuro-cognitive baselines and historical mission logs. *(Currently disabled in the live demo — use Guest Mode.)*

### 2. Live Synthetic EEG & Biometric Assessment

- **Real-time Signal Stream**: Leverages `MNE-Python` to simulate live 8-channel EEG streams grounded in **PhysioNet** and **NASA OSDR** datasets.
- **Frequency Analysis & Wave Interpretation**:
  - **Alpha (8–12 Hz)**: Optimal resting state; balanced memory and baseline cognitive load.
  - **Beta (13–30 Hz)**: High focus and active executive function. Protracted elevation indicates severe cognitive fatigue and stress.
  - **Theta (4–7 Hz)**: Drowsiness and neuro-fatigue. Elevated theta during awake states flags high error vulnerability and reaction latency.
  - **Gamma (>30 Hz)**: Complex information integration and intense cognitive processing.
- **Feature Extraction**: Computes the **Beta/Theta Ratio** dynamically to estimate a **Cognitive Fatigue Index (0–100)**.

### 3. Reaction Time Test

- Interactive reaction-time test benchmarked against NASA HRP / WinSCAT-style thresholds (Normal ≤ 350 ms, Fatigue Alert > 350 ms).

### 4. Dynamic Neural Risk Bar & Biometrics Sync

- **Color-Coded Status Bar**:
  - 🟢 **Green (Normal)**: Baseline active state.
  - 🔵 **Blue (Moderate Risk)**: Early fatigue / sensorimotor mismatch detected.
  - 🔴 **Red Alert (High Risk)**: Critical neuro-fatigue or parietal lobe degradation.
- **Cardiovascular Sync**: Heart-pulse visualization mapping live HR and HRV against stress markers (*Sympathetic Overdrive*).

### 5. Lobe-Specific Health Mapping

Dynamic visual heatmaps tracking structural and functional load across dedicated brain structures:

- **Frontal Lobe**: Executive function, decision latency, and working memory.
- **Parietal Lobe**: Sensorimotor integration and spatial orientation.
- **Occipital Lobe**: Visual processing speed and SANS-related degradation tracking.
- **Temporal Lobe / Insula**: Sensorimotor-temporal alignment and auditory cue processing.

### 6. Time Perception Recalibration & Neuro-Pacing (CPT)

- **Time Distortion Coefficient**: Calculates real-time temporal perception drift caused by microgravity-induced loss of proprioceptive feedback.
- **Cognitive Pacing Training (CPT)**: 3-to-5 minute interactive visual and **Rhythmic Auditory Stimulation (RAS)** exercises. Uses time-estimation tasks to exploit neuroplasticity and re-align the brain's internal neural clock (*Posterior Parietal Cortex & Basal Ganglia*).

### 7. Actionable NASA-Backed Protocols

- **Automated Intervention Logic**:
  - **High Theta / Slow Reaction (>350 ms)**: Triggers **20–30 min neuro-stimulation breaks** (binaural beats / light therapy) and crew rotation alerts.
  - **High Beta/Gamma (Stress Overload)**: Initiates **5-min guided breathing** and cognitive load reduction.
  - **Sensorimotor Decline**: Temporarily halts EVA operations and prompts sensorimotor retargeting exercises.

---

## 🏗️ System Architecture & Workflow

```text
+-----------------------------------------------------------------------+
|                         NASA Open Data Sources                        |
|   (NASA OSDR, HRP Cognition Battery, LSDA Twins Study, WinSCAT)       |
+----------------------------------+------------------------------------+
                                   |
                                   v
+----------------------------------+------------------------------------+
|                    Synthetic Signal & Data Engine                     |
|   - MNE-Python (EEG filtering, Alpha/Beta/Theta/Gamma bands)          |
|   - NumPy / SciPy / Scikit-Learn (fatigue & distortion classifiers)   |
+----------------------------------+------------------------------------+
                                   |
                                   v
+----------------------------------+------------------------------------+
|                       Django Application Core                         |
|   (offline-capable design for a local spacecraft server)              |
+----------------------------------+------------------------------------+
                                   |
                                   v
+----------------------------------+------------------------------------+
|                          Web Interface                                |
|   - Dashboard & Dynamic Risk Status Bar   - EEG & Reaction Tests     |
|   - Lobe-Specific Heatmaps                - CPT Neuro-Pacing Training |
|   - Metrics, Risk & Recommendations      - NASA Safety Protocols      |
+-----------------------------------------------------------------------+
```

---

## 🛠️ Tech Stack

| Domain | Technology / Library | Description |
| --- | --- | --- |
| **Backend** | Python, Django, Gunicorn, WhiteNoise | Web app, routing, static file serving and production server |
| **Frontend** | Django Templates, HTML/CSS/JavaScript | Astronaut dashboard with minimal HCI to reduce cognitive load |
| **Signal Processing** | MNE-Python, SciPy, NumPy | Synthetic EEG frequency bands and power spectral density (PSD) |
| **Machine Learning** | Scikit-Learn | Fatigue prediction, reaction-time latency scoring, risk classification |
| **Computer Vision** | OpenCV (headless) | Camera / face-verification engine (currently disabled) |
| **Data Baselines** | NASA OSDR, HRP, WinSCAT | Medical thresholds, cognition metrics, baseline reaction parameters |
| **Deployment** | Render | Live hosting via `Procfile` |

---

## 📂 Project Structure

```text
nasa_space_app_challenge_2026/
├── core/                  # Main Django app (views, templates, logic)
├── neurohealth_project/   # Django project settings & URL config
├── manage.py
├── requirements.txt
├── Procfile               # Render / Gunicorn start command
└── README.md
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/imon2928/nasa_space_app_challenge_2026.git
cd nasa_space_app_challenge_2026

# 2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations & start the server
python manage.py migrate
python manage.py runserver
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 📊 NASA Data Sources & Grounding

The algorithmic thresholds and health models in **Neuro-Health** are constructed from NASA and spaceflight datasets:

1. **NASA Open Science Data Repository (OSDR)**: Used to derive baseline weights for lobe-specific neuro-structural changes under cosmic radiation and microgravity.
2. **NASA Human Research Program (HRP) / WinSCAT & Cognition Battery**: Standardized reaction-time thresholds (Normal ≤ 350 ms, Fatigue Alert > 350 ms) and spatial memory decay curves.
3. **NASA Twins Study & LSDA**: Empirical decay rates for mission-duration vs. cognitive performance used in long-term predictive modeling.

> *"The baseline thresholds for Neuro-Health's cognitive fatigue prediction models are informed by standard metrics from the NASA Human Research Program (HRP) Cognition Battery and NASA Open Science Data Repository (OSDR) spaceflight datasets."*

---

## 👥 Team NeuroNauts

We are a multidisciplinary team bridging space neuroscience, software engineering, and visual design:

- **Md. Imon Hossain** — Lead Researcher, Software Engineer & UI/UX Designer
- **Jannat** — Presenter & Scientific Advocate
- **Maria** — Core Neuro-Research Specialist
- **Akram** — Scientific Communication & Documentation
- **Dipu** — Visual Designer & Graphic Assets
- **Sinha** — Narrative & Content Specialist

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

**Monitor Your Brain. Predict the Risk. Protect the Mission.**
Team NeuroNauts • NASA Space Apps Challenge 2026 • [Live Demo](https://neuro-health.onrender.com)
