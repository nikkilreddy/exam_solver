import time
import random
import pyautogui
from pynput import keyboard

class GhostTyper:
    def __init__(self):
        self.active = False
        self.paused = False
        self.listener = None
        
    def on_press(self, key):
        # We listen passively (suppress=False) so there are no Mac infinite loop bugs
        if not self.active:
            return
            
        # If the user presses the 'Right Shift' key, we toggle the pause state.
        # Browsers CANNOT block the Shift key or else users wouldn't be able to type capital letters!
        if key == keyboard.Key.shift_r:
            self.paused = not self.paused
            if self.paused:
                print("[Ghost] ⏸️ PAUSED. Press 'Right Shift' again to resume.")
            else:
                print("[Ghost] ▶️ RESUMED typing!")

    def start_typing(self, solution_code):
        print(f"[Ghost] Ghost mode activated. Code length: {len(solution_code)}")
        self.active = True
        
        # Give user 2 seconds to click inside the code editor before we start typing
        print("[Ghost] You have 3 seconds to click inside the exam text editor...")
        time.sleep(3)
        
        print("[Ghost] Auto-typing started! You can press the 'Right Shift' key at any time to Pause/Resume.")
        
        self.paused = False
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
        for char in solution_code:
            if not self.active:
                break # Allows stopping mid-way if right corner is clicked again
                
            # Block while paused
            while self.paused and self.active:
                time.sleep(0.1)
                
            if char == '\n':
                pyautogui.press('enter')
                # Wait a bit longer after newlines to simulate thinking
                time.sleep(random.uniform(0.1, 0.4))
            elif char == '\t':
                pyautogui.press('tab')
            else:
                pyautogui.typewrite(char)
                
            # Human typing speed delay (approx 60-80 WPM)
            time.sleep(random.uniform(0.02, 0.08))
            
        print("[Ghost] Finished typing code.")
        self.stop_typing()

    def stop_typing(self):
        self.active = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        print("[Ghost] Ghost mode halted.")
