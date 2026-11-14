import os
import sys
import time
import socket
import threading
import webview
from waitress import serve

# PyInstaller ডাইনামিক রুট পাথ হ্যান্ডেল করা
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)
os.chdir(base_dir)

# উইন্ডোজ টাস্কবারে নিজস্ব আইকন সাপোর্ট দেওয়া
try:
    import ctypes
    myappid = 'neurohealth.biometric.app.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# Django সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neurohealth_project.settings')

import django
django.setup()

from django.core.handlers.wsgi import WSGIHandler

def start_server():
    """Waitress WSGI সার্ভার দিয়ে জ্যাঙ্গো প্রজেক্ট চালু করা"""
    try:
        application = WSGIHandler()
        serve(application, host='127.0.0.1', port=8000, threads=6)
    except Exception as e:
        print("Waitress Server Error:", e)

def wait_for_server(host='127.0.0.1', port=8000, timeout=12):
    """সার্ভার ৮০০০ পোর্টে চালু হওয়া পর্যন্ত অপেক্ষা করা"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.5)
    return False

if __name__ == '__main__':
    # ১. থ্রেডে জ্যাঙ্গো সার্ভার চালুকরণ
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # ২. ৮০০০ পোর্ট চালু হওয়া পর্যন্ত ওয়েট করা
    if wait_for_server():
        # ৩. পোর্ট রেডি হলেই সফটওয়্যার উইন্ডো ওপেন হবে
        window = webview.create_window(
            title='Neuro-Health — Biometric Authentication & Cognitive Monitor',
            url='http://127.0.0.1:8000/login/',
            width=1100,
            height=750,
            resizable=True,
            min_size=(900, 600)
        )
        webview.start()
    else:
        print("Error: Django server failed to start within timeout.")