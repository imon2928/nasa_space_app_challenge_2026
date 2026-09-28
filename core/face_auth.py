"""
face_auth.py — ফেস লগইনের জন্য OpenCV (YuNet ডিটেক্টর + SFace রিকগনাইজার) মডিউল।

এই ফাইলটি আপনার অ্যাপ ফোল্ডারে (views.py এর পাশে) রাখুন।

প্রয়োজন:
    pip install "opencv-python>=4.8" numpy
    face_models/ ফোল্ডারে দুটি ONNX মডেল (নিচে README-স্টাইল নোটে কমান্ড দেওয়া আছে)
"""
import os
import threading
from pathlib import Path

import cv2
from django.conf import settings

# ─────────────────────────────────────────────────────────────
# CUSTOMIZE: এখানে আগে থেকে ছবি যোগ করুন
#   key   = AstronautProfile.astronaut_id
#   name  = প্রোফাইলে যে নাম দেখাবেন (না দিলে ফাইলের নাম থেকে নেবে)
#   file  = static ফোল্ডারের ভেতরের রিলেটিভ পাথ
# ─────────────────────────────────────────────────────────────
KNOWN_FACES = {
    "Imon": {"name": "Imon", "file": "images/imon.jpg"},
    "Dipu": {"name": "Dipu", "file": "images/dipu.png"},
    "Akram": {"name": "Akram", "file": "images/akram.jpeg"},
    "Jannat": {"name": "Jannat", "file": "images/jannat.jpeg"},
    "Maria": {"name": "Maria", "file": "images/maria.jpeg"},
}

# CUSTOMIZE: মডেল ফাইলের অবস্থান
MODELS_DIR = Path(settings.BASE_DIR) / "face_models"
DETECTOR_MODEL = MODELS_DIR / "face_detection_yunet_2023mar.onnx"
RECOGNIZER_MODEL = MODELS_DIR / "face_recognition_sface_2021dec.onnx"

# CUSTOMIZE: কোসাইন সিমিলারিটি থ্রেশহোল্ড (OpenCV-এর ডিফল্ট সুপারিশ ≈ 0.363)
# বাড়ালে কঠোর (ভুল লগইন কমে, কিন্তু নিজের মুখও মাঝে মাঝে রিজেক্ট হতে পারে)
MATCH_THRESHOLD = 0.40

# CUSTOMIZE: মুখ "ডিটেক্ট" করার ন্যূনতম কনফিডেন্স। আলো কম/ওয়েবক্যাম খারাপ হলে ০.৬ পর্যন্ত নামান
DETECT_SCORE = 0.7

# CUSTOMIZE: টানা কতবার একই ব্যক্তি মিললে লগইন হবে
REQUIRED_HITS = 3

_engine_lock = threading.Lock()
_detector = None
_recognizer = None
_known_features = None  # {astronaut_id: feature_vector}


def _static_dir():
    dirs = getattr(settings, "STATICFILES_DIRS", [])
    return str(dirs[0]) if dirs else os.path.join(str(settings.BASE_DIR), "static")


def _resolve_path(rel):
    """ছবির আসল পাথ খোঁজে: Django staticfiles finder → STATICFILES_DIRS → BASE_DIR/static"""
    from django.contrib.staticfiles import finders
    found = finders.find(rel)
    if isinstance(found, (list, tuple)):
        found = found[0] if found else None
    if found:
        return str(found)

    bases = []
    for d in getattr(settings, "STATICFILES_DIRS", []):
        bases.append(str(d[1] if isinstance(d, (list, tuple)) else d))
    bases.append(os.path.join(str(settings.BASE_DIR), "static"))
    for base in bases:
        candidate = os.path.join(base, rel)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(bases[0], rel)  # পাওয়া যায়নি — এরর মেসেজে দেখানোর জন্য


def get_face_info(astronaut_id):
    """প্রোফাইল/ড্যাশবোর্ডে দেখানোর জন্য ছবির তথ্য। না থাকলে None।"""
    info = KNOWN_FACES.get(astronaut_id)
    if not info:
        return None
    filename = os.path.basename(info["file"])
    return {
        "id": astronaut_id,
        "name": info.get("name") or os.path.splitext(filename)[0],
        "file": info["file"],      # {% static face_info.file %} এর জন্য
        "filename": filename,      # যেমন: imon.jpg
    }


def _load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    h, w = img.shape[:2]
    if max(h, w) > 1024:  # বড় ছবি ছোট করলে দ্রুত হয়
        scale = 1024 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return img


def _detect_largest_face(img):
    h, w = img.shape[:2]
    _detector.setInputSize((w, h))
    _, faces = _detector.detect(img)
    if faces is None or len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])  # সবচেয়ে বড় মুখ


def _detect_enrollment_face(img):
    """রেজিস্টার করা ছবিতে মুখ খোঁজে — না পেলে ধাপে ধাপে থ্রেশহোল্ড কমিয়ে ও ছবি ছোট করে চেষ্টা করে।"""
    h, w = img.shape[:2]
    small = img
    if max(h, w) > 640:
        scale = 640 / max(h, w)
        small = cv2.resize(img, (int(w * scale), int(h * scale)))

    face, used = None, img
    for candidate in (img, small):
        for thr in (DETECT_SCORE, 0.5, 0.3):
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
    """প্রথমবার কল হলে মডেল লোড করে আর পরিচিত ছবিগুলোর ফিচার একবারই বের করে রাখে।"""
    global _detector, _recognizer, _known_features
    if _known_features is not None:
        return

    if not hasattr(cv2, "FaceDetectorYN") or not hasattr(cv2, "FaceRecognizerSF"):
        raise RuntimeError(f"OPENCV TOO OLD ({cv2.__version__}) — pip install -U opencv-python")

    # (ফাইল, ন্যূনতম সাইজ) — ছোট হলে ডাউনলোড নষ্ট (LFS পয়েন্টার/HTML পেজ) হয়েছে
    for model, min_size in ((DETECTOR_MODEL, 100_000), (RECOGNIZER_MODEL, 10_000_000)):
        if not model.exists():
            raise FileNotFoundError(f"MODEL FILE MISSING: {model.name} (face_models/ ফোল্ডারে রাখুন)")
        if model.stat().st_size < min_size:
            raise RuntimeError(f"MODEL FILE CORRUPT: {model.name} ({model.stat().st_size} bytes) — আবার ডাউনলোড করুন")

    _detector = cv2.FaceDetectorYN.create(str(DETECTOR_MODEL), "", (320, 320), DETECT_SCORE, 0.3, 5000)
    _recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZER_MODEL), "")

    features = {}
    for astro_id, info in KNOWN_FACES.items():
        path = _resolve_path(info["file"])
        img = _load_image(path) if os.path.isfile(path) else None
        if img is None:
            folder = os.path.dirname(path)
            listing = os.listdir(folder) if os.path.isdir(folder) else "ফোল্ডারটাই নেই"
            print(f"[face_auth] {astro_id}: ছবি পাওয়া/পড়া যায়নি -> {path}")
            print(f"[face_auth]   ওই ফোল্ডারে আছে: {listing}")
            continue
        face, used = _detect_enrollment_face(img)
        if face is None:
            print(f"[face_auth] {astro_id}: ছবিতে মুখ পাওয়া যায়নি -> {path} ({img.shape[1]}x{img.shape[0]})")
            continue
        features[astro_id] = _recognizer.feature(_recognizer.alignCrop(used, face))
        print(f"[face_auth] {astro_id}: রেজিস্টার হয়েছে -> {path}")

    if not features:
        # ক্যাশ করছি না, যাতে ছবি ঠিক করে আবার চেষ্টা করা যায়
        raise RuntimeError("NO ENROLLED FACE LOADED — KNOWN_FACES-এর ছবি/পাথ বা ছবির মুখ চেক করুন (সার্ভার কনসোল দেখুন)")
    _known_features = features


def reload_known_faces():
    """নতুন ছবি যোগ করলে সার্ভার রিস্টার্ট ছাড়া রিলোড করতে চাইলে কল করুন।"""
    global _known_features
    with _engine_lock:
        _known_features = None


def recognize_face(frame):
    """
    ক্যামেরা ফ্রেম (BGR numpy array) নিয়ে ফেরত দেয়: (status, astronaut_id, score)
      status = "ok" | "no_face" | "unknown"
    """
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


def diagnose(test_image=None):
    """
    সমস্যা খুঁজতে চালান:
        python manage.py shell -c "from YOURAPP.face_auth import diagnose; diagnose()"
    ওয়েবক্যামের একটা ছবি সেভ করে পাথ দিলে সেটাও টেস্ট করে:
        diagnose('/path/to/snapshot.jpg')
    """
    print("OpenCV version:", cv2.__version__)
    print("FaceDetectorYN:", hasattr(cv2, "FaceDetectorYN"), "| FaceRecognizerSF:", hasattr(cv2, "FaceRecognizerSF"))
    for m in (DETECTOR_MODEL, RECOGNIZER_MODEL):
        print(m.name, "->", f"{m.stat().st_size} bytes" if m.exists() else "MISSING")
    for astro_id, info in KNOWN_FACES.items():
        path = _resolve_path(info["file"])
        img = _load_image(path) if os.path.isfile(path) else None
        print(astro_id, path, "->", "NOT FOUND/UNREADABLE" if img is None else f"loaded {img.shape[1]}x{img.shape[0]}")

    reload_known_faces()
    try:
        with _engine_lock:
            _ensure_ready()
        print("Enrolled faces:", list(_known_features.keys()))
    except Exception as exc:
        print("ENGINE ERROR:", exc)
        return

    if test_image:
        frame = _load_image(test_image)
        print("Test image:", "unreadable" if frame is None else recognize_face(frame))