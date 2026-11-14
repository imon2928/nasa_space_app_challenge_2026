# nasa_space_app_challenge_2026
# 🚀 Neuro-Health: Astronaut Neuro-Cognitive & Sensorimotor Health Monitoring System

![NASA Space Apps Challenge 2026](https://img.shields.io/badge/NASA%20Space%20Apps-2026-blue?style=for-the-badge&logo=nasa)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![MNE-Python](https://img.shields.io/badge/MNE--Python-Signal%20Processing-000000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

> **"When humanity steps into deep space, the ultimate survival technology isn't built of metal — it's the human brain inside the helmet."**

---

## 📌 Executive Summary

During deep-space missions, astronauts endure long-term isolation, cosmic radiation (HZE particles), and microgravity ($0g$). Microgravity eliminates the $1g$ vector, shutting down otolith organ signaling in the inner ear and proprioceptive feedback from foot pressure. This induces a severe **Sensory Conflict (Neuro-Vestibular Mismatch)** in the *Vestibular Nuclei*, triggering **Space Motion Sickness (SMS)** via the evolutionary *Poison Hypothesis* (*Area Postrema* activation). Furthermore, long-term exposure causes cephalad fluid shifts, ventriculomegaly ($12–25\%$ expansion), **Spaceflight-Associated Neuro-ocular Syndrome (SANS)**, and disrupts the internal neural clock in the *Posterior Parietal Cortex* and *Basal Ganglia*, leading to critical **Cognitive Time Distortion**.

With communication delays with Earth exceeding **20 minutes** on Mars missions, real-time intervention from Ground Control is impossible. A split-second error during extravehicular activity (EVA) or docking maneuvers can prove fatal.

**Neuro-Health** by **Team NeuroNauts** is an autonomous, edge-computing predictive software platform. Anchored on NASA Open Science Data Repository (OSDR) datasets and EEG metrics, Neuro-Health delivers real-time synthetic EEG stream processing, lobe-specific neuro-health mapping, gamified cognitive time-perception recalibration, and predictive risk alerts to transition space medicine from reactive treatment to real-time neural protection.

---

## 🎯 Key Features & Core Innovations

### 1. Secure Authentication & Instant Baseline
* **Facial Recognition Authentication**: Provides instant, hands-free authentication for astronauts, fetching personalized neuro-cognitive baselines and historical mission logs.

### 2. Live Synthetic EEG & Biometric Assessment
* **Real-time Signal Stream**: Leverages `MNE-Python` to simulate live $8$-channel EEG streams grounded in **PhysioNet** and **NASA OSDR** datasets.
* **Frequency Analysis & Wave Interpretation**:
  * **Alpha ($\mathbf{8-12\text{ Hz}}$)**: Optimal Resting State; balanced memory and baseline cognitive load.
  * **Beta ($\mathbf{13-30\text{ Hz}}$)**: High focus and active executive function. Protracted elevation indicates severe cognitive fatigue and stress.
  * **Theta ($\mathbf{4-7\text{ Hz}}$)**: Drowsiness and Neuro-Fatigue. Elevated theta during awake states flags high error vulnerability and reaction latency.
  * **Gamma ($\mathbf{>30\text{ Hz}}$)**: Complex information integration and intense cognitive processing.
* **Feature Extraction**: Computes the **Beta/Theta Ratio** dynamically to estimate a **Cognitive Fatigue Index ($0-100$)**.

### 3. Dynamic Neural Risk Bar & Biometrics Sync
* **Color-Coded Status Bar**:
  * 🟢 **Green (Normal)**: Baseline active state.
  * 🔵 **Blue (Moderate Risk)**: Early fatigue/sensorimotor mismatch detected.
  * 🔴 **Red Alert (High Risk)**: Critical neuro-fatigue or parietal lobe degradation.
* **Cardiovascular Sync**: Integrated 3D Heart Pulse visualization mapping live HR and HRV against stress markers (*Sympathetic Overdrive*).

### 4. Lobe-Specific Health Mapping
Generates dynamic visual heatmaps tracking structural and functional load across dedicated brain structures:
* **Frontal Lobe**: Executive function, decision latency, and working memory.
* **Parietal Lobe**: Sensorimotor integration and spatial orientation.
* **Occipital Lobe**: Visual processing speed and SANS-related degradation tracking.
* **Temporal Lobe / Insula**: Sensorimotor-temporal alignment and auditory cues processing.

### 5. Time Perception Recalibration & Neuro-Pacing (CPT)
* **Time Distortion Coefficient**: Calculates real-time temporal perception drift caused by microgravity-induced loss of proprioceptive feedback.
* **Cognitive Pacing Training (CPT)**: 3-to-5 minute interactive visual and **Rhythmic Auditory Stimulation (RAS)** exercises. Employs time estimation tasks to exploit neuroplasticity and re-align the brain's internal neural clock (*Posterior Parietal Cortex & Basal Ganglia*).

### 6. Actionable NASA-Backed Protocols
* **Automated Intervention Logic**:
  * **High Theta / Slow Reaction (>350ms)**: Triggers **20-30 min Neuro-stimulation Breaks** (Binaural Beats / Light Therapy) and crew rotation alerts.
  * **High Beta/Gamma (Stress Overload)**: Initiates **5-min Guided Breathing** and cognitive load reduction.
  * **Sensorimotor Decline**: Temporarily halts EVA operations and prompts sensorimotor retargeting exercises.

---

## 🏗️ System Architecture & Workflow
+-----------------------------------------------------------------------+
|                         NASA Open Data Sources                        |
|   (NASA OSDR, HRP Cognition Battery, LSDA Twins Study, WinSCAT)       |
+----------------------------------+------------------------------------+
|
v
+----------------------------------+------------------------------------+
|                    Synthetic Signal & Data Engine                     |
|        - MNE-Python (EEG Filtering, Alpha/Beta/Theta/Gamma)           |
|        - NumPy / Scikit-Learn (Fatigue & Distortion Classifiers)      |
+----------------------------------+------------------------------------+
|
v
+----------------------------------+------------------------------------+
|                      Edge-Computing Core                      |
|         (100% Offline Capable - Local Spacecraft Server)              |
+----------------------------------+------------------------------------+
|
v
+----------------------------------+------------------------------------+
|                     React.js / Web Interface                          |
|   - Facial Recognition Sign-in    - Lobe-Specific Heatmaps            |
|   - Dynamic Risk Status Bar       - 3D Heart Sync (Three.js)          |
|   - CPT Neuro-Pacing Training     - NASA Safety Action Protocols      |
+-----------------------------------------------------------------------+
---

## 🛠️ Tech Stack

| Domain | Technology / Library | Description |
| :--- | :--- | :--- |
| **Frontend UI/UX** | React.js, TailwindCSS, Three.js | High-performance astronaut dashboard, minimal HCI to reduce cognitive load |
| **Backend & Analytics** | Python 3.10+, FastAPI / Streamlit | High-throughput data orchestration and edge analytics |
| **Signal Processing** | MNE-Python, SciPy, NumPy | Processing synthetic EEG frequency bands and power spectral density (PSD) |
| **Machine Learning** | Scikit-Learn | Fatigue prediction, reaction time latency scoring, and risk classification |
| **Data Baselines** | NASA OSDR, HRP, WinSCAT | Medical thresholds, cognition metrics, and baseline reaction parameters |

---

## 📊 NASA Data Sources & Grounding

The algorithmic thresholds and health models in **Neuro-Health** are constructed directly from NASA and spaceflight datasets:

1. **NASA Open Science Data Repository (OSDR)**: Used to derive baseline weights for lobe-specific neuro-structural changes under cosmic radiation and microgravity.
2. **NASA Human Research Program (HRP) / WinSCAT & Cognition Battery**: Standardized reaction time thresholds (e.g., $Normal \le 350\text{ ms}$, $Fatigue Alert > 350\text{ ms}$) and spatial memory decay curves.
3. **NASA Twins Study & LSDA**: Empirical decay rates for mission-duration vs. cognitive performance used in long-term mission predictive modeling.

> *"The baseline thresholds for Neuro-Health's cognitive fatigue prediction models are informed by standard metrics from the NASA Human Research Program (HRP) Cognition Battery and NASA Open Science Data Repository (OSDR) spaceflight datasets."*

---

## 👥 Team NeuroNauts

We are a multidisciplinary team bridging space neuroscience, software engineering, and visual design:

* **Md. Imon Hossain** — Lead Researcher, Software Engineer & UI/UX Designer
* **Jannat** — Presenter & Scientific Advocate
* **Maria** — Core Neuro-Research Specialist
* **Akram** — Scientific Communication & Documentation
* **Dipu** — Visual Designer & Graphic Assets
* **Sinha** — Narrative & Content Specialist

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<p align="center">
  <b>Monitor Your Brain. Predict the Risk. Protect the Mission.</b><br>
  <sub>Team NeuroNauts • NASA Space Apps Challenge 2026</sub>
</p>
