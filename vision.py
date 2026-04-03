import os
import time
import platform

# Only import pyautogui on Windows as it causes Pillow bugs on macOS Python 3.14
if platform.system() == "Windows":
    import pyautogui

def get_user():
    if platform.system() == "Windows":
        return os.getlogin()
    return os.environ.get("SUDO_USER") or os.getlogin()

def get_paths():
    user = get_user()
    if platform.system() == "Windows":
        return f"C:\\Users\\{user}"
    return f"/Users/{user}"

def capture_mcq_image():
    user = get_user()
    if platform.system() == "Windows":
        save_path = "screen.png"
        print("[Vision] Capturing single screenshot for MCQ (Windows)...")
        pyautogui.screenshot(save_path)
    else:
        save_path = f"/Users/{user}/screen.png"
        print(f"[Vision] Capturing single screenshot for MCQ (as {user})...")
        os.system(f"sudo -u {user} screencapture -x {save_path}")
    return [save_path]

def capture_coding_images():
    user = get_user()
    
    if platform.system() == "Windows":
        s1_path = "s1.png"
        s2_path = "s2.png"
        print("[Vision] Capturing first screen (Windows)...")
        pyautogui.screenshot(s1_path)
        
        # Windows beep
        import winsound
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        
        print("[Vision] Pausing 2 seconds for you to scroll down...")
        time.sleep(2)
        
        print("[Vision] Capturing second screen (Windows)...")
        pyautogui.screenshot(s2_path)
    else:
        s1_path = f"/Users/{user}/s1.png"
        s2_path = f"/Users/{user}/s2.png"
        print(f"[Vision] Capturing first screen (as {user})...")
        os.system(f"sudo -u {user} screencapture -x {s1_path}")
        
        os.system("afplay /System/Library/Sounds/Ping.aiff &")
        print("[Vision] Pausing 2 seconds for you to scroll down...")
        time.sleep(2)
        
        print(f"[Vision] Capturing second screen (as {user})...")
        os.system(f"sudo -u {user} screencapture -x {s2_path}")
    
    return [s1_path, s2_path]
    
    return [s1_path, s2_path]
