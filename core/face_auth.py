"""
face_auth.py — ফেস লগইনের জন্য OpenCV (YuNet ডিটেক্টর + SFace রিকগনাইজার) মডিউল।
"""
import os
import sys
import threading
import cv2
from django.conf import settings

# ─────────────────────────────────────────────────────────────
# ১. PyInstaller (.exe) ও ডেভেলপমেন্ট উভয় ক্ষেত্রে সঠিক পাথ রিড করার ফাংশন
# ─────────────────────────────────────────────────────────────
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = str(settings.BASE_DIR)
    return os.path.join(base_path, relative_path)

# ─────────────────────────────────────────────────────────────
# CUSTOMIZE: নিবন্ধিত ছবিসমূহ
# ─────────────────────────────────────────────────────────────
KNOWN_FACES = {
    "Imon": {"name": "Imon", "file": "images/imon.jpg"},
    "Dipu": {"name": "Dipu", "file": "images/dipu.png"},
    "Akram": {"name": "Akram", "file": "images/akram.jpeg"},
    "Jannat": {"name": "Jannat", "file": "images/jannat.jpeg"},
    "Maria": {"name": "Maria", "file": "images/maria.jpeg"},
}

# মডেল ফাইলসমূহের ডায়নামিক পাথ
DETECTOR_MODEL = get_resource_path("face_models/face_detection_yunet_2023mar.onnx")
RECOGNIZER_MODEL = get_resource_path("face_models/face_recognition_sface_2021dec.onnx")

# কোসাইন সিমিলারিটি ও ডিটেকশন থ্রেশহোল্ড (ওয়েবক্যাম এবং ঘরের আলোর জন্য কিছুটা সহনশীল করা হয়েছে)
MATCH_THRESHOLD = 0.30
DETECT_SCORE = 0.50
REQUIRED_HITS = 2

_engine_lock = threading.Lock()
_detector = None
_recognizer = None
_known_features = None  # {astronaut_id: feature_vector}


def _resolve_path(rel):
    """ছবির আসল পাথ খোঁজে: PyInstaller Temp path -> Django staticfiles -> BASE_DIR/static"""
    # ১. PyInstaller bundling-এর ভেতরে থাকলে
    pyi_candidate = get_resource_path(os.path.join("core", "static", rel))
    if os.path.exists(pyi_candidate):
        return pyi_candidate
        
    pyi_candidate_direct = get_resource_path(os.path.join("static", rel))
    if os.path.exists(pyi_candidate_direct):
        return pyi_candidate_direct

    # ২. Django Staticfinders
    try:
        from django.contrib.staticfiles import finders
        found = finders.find(rel)
        if isinstance(found, (list, tuple)):
            found = found[0] if found else None
        if found and os.path.exists(found):
            return str(found)
    except Exception:
        pass

    # ৩. ম্যানুয়াল ফলব্যাক
    bases = []
    for d in getattr(settings, "STATICFILES_DIRS", []):
        bases.append(str(d[1] if isinstance(d, (list, tuple)) else d))
    bases.append(os.path.join(str(settings.BASE_DIR), "static"))
    
    for base in bases:
        candidate = os.path.join(base, rel)
        if os.path.exists(candidate):
            return candidate
            
    return os.path.join(bases[0], rel)


def get_face_info(astronaut_id):
    info = KNOWN_FACES.get(astronaut_id)
    if not info:
        return None
    filename = os.path.basename(info["file"])
    return {
        "id": astronaut_id,
        "name": info.get("name") or os.path.splitext(filename)[0],
        "file": info["file"],
        "filename": filename,
    }


def _load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    h, w = img.shape[:2]
    if max(h, w) > 1024:
        scale = 1024 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return img


def _detect_largest_face(img):
    h, w = img.shape[:2]
    _detector.setInputSize((w, h))
    _, faces = _detector.detect(img)
    if faces is None or len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])


def _detect_enrollment_face(img):
    h, w = img.shape[:2]
    small = img
    if max(h, w) > 640:
        scale = 640 / max(h, w)
        small = cv2.resize(img, (int(w * scale), int(h * scale)))

    face, used = None, img
    for candidate in (img, small):
        for thr in (DETECT_SCORE, 0.4, 0.25):
            _detector.setScoreThreshold(thr)
            face = _detect_largest_face(candidate)
            if face is not None:
                used = candidate
                break
        if face is not None:
            break
    _detector.setScoreThreshold(DETECT_SCORE)
    return face, used


def _ensure_ready():
    global _detector, _recognizer, _known_features
    if _known_features is not None:
        return

    if not hasattr(cv2, "FaceDetectorYN") or not hasattr(cv2, "FaceRecognizerSF"):
        raise RuntimeError(f"OPENCV TOO OLD ({cv2.__version__})")

    # মডেল ফাইল দুটি চেক করা
    for model_path, min_size in ((DETECTOR_MODEL, 100_000), (RECOGNIZER_MODEL, 10_000_000)):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"MODEL FILE MISSING: {os.path.basename(model_path)}")
        if os.path.getsize(model_path) < min_size:
            raise RuntimeError(f"MODEL FILE CORRUPT: {os.path.basename(model_path)}")

    _detector = cv2.FaceDetectorYN.create(str(DETECTOR_MODEL), "", (320, 320), DETECT_SCORE, 0.3, 5000)
    _recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZER_MODEL), "")

    features = {}
    for astro_id, info in KNOWN_FACES.items():
        path = _resolve_path(info["file"])
        img = _load_image(path) if os.path.isfile(path) else None
        if img is None:
            print(f"[face_auth] {astro_id}: Image not found -> {path}")
            continue
        face, used = _detect_enrollment_face(img)
        if face is None:
            print(f"[face_auth] {astro_id}: No face found in image -> {path}")
            continue
        features[astro_id] = _recognizer.feature(_recognizer.alignCrop(used, face))
        print(f"[face_auth] {astro_id}: Successfully enrolled -> {path}")

    if not features:
        raise RuntimeError("NO ENROLLED FACE LOADED — Please check images in static/images/")
    _known_features = features


def reload_known_faces():
    global _known_features
    with _engine_lock:
        _known_features = None


def recognize_face(frame):
    with _engine_lock:
        _ensure_ready()
        face = _detect_largest_face(frame)
        if face is None:
            return "no_face", None, 0.0

        live_feature = _recognizer.feature(_recognizer.alignCrop(frame, face))

        best_id, best_score = None, -1.0
        for astro_id, known_feature in _known_features.items():
            score = float(_recognizer.match(live_feature, known_feature, cv2.FaceRecognizerSF_FR_COSINE))
            if score > best_score:
                best_id, best_score = astro_id, score

    if best_id is not None and best_score >= MATCH_THRESHOLD:
        return "ok", best_id, best_score
    return "unknown", None, best_score