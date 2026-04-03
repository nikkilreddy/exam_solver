import subprocess
import os

import pyautogui

def move_mouse_to_quadrant(response_text):
    """Move mouse to screen quadrant based on answer (A, B, C, D) using a human curve."""
    option = response_text.strip().upper()
    
    W, H = pyautogui.size()
    
    if "A" in option:
        target_x, target_y = W // 4, H // 4
    elif "B" in option:
        target_x, target_y = (3 * W) // 4, H // 4
    elif "C" in option:
        target_x, target_y = W // 4, (3 * H) // 4
    elif "D" in option:
        target_x, target_y = (3 * W) // 4, (3 * H) // 4
    else:
        print(f"[Solver] Could not map '{option}' to a quadrant.")
        return
        
    print(f"[Solver] Nudging mouse to Quadrant {option} (X:{target_x}, Y:{target_y})")
    pyautogui.moveTo(target_x, target_y, duration=1.2, tween=pyautogui.easeInOutQuad)


