import time
import os
import platform
import pyautogui
from pynput import mouse
from solver import move_mouse_to_quadrant
from ghost import GhostTyper

def play_sound(sound):
    if platform.system() == "Windows":
        import winsound
        # Map macOS sounds to Windows default sounds
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        except:
            pass
    else:
        os.system(f"afplay /System/Library/Sounds/{sound}.aiff &")
from ghost import GhostTyper

class StealthController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.corner_margin = 15 # 15 pixels leeway for the corner
        self.ghost = GhostTyper()
        
    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
            
        is_bottom = y >= (self.screen_height - self.corner_margin)
        is_left = x <= self.corner_margin
        is_right = x >= (self.screen_width - self.corner_margin)
        
        if is_bottom and is_left and button == mouse.Button.left:
            print(f"[Trigger] Bottom-Left Corner Clicked at ({x},{y}) -> MCQ Mode!")
            self.trigger_mcq()
            
        elif is_bottom and is_right and button == mouse.Button.left:
            # We use left click in the corners to be totally natural.
            if self.ghost.active:
                print(f"[Trigger] Bottom-Right Corner Clicked -> Turning OFF Code Ghost Mode.")
                self.ghost.stop_typing()
                play_sound("Submarine")
            else:
                print(f"[Trigger] Bottom-Right Corner Clicked at ({x},{y}) -> Code Mode!")
                self.trigger_coding()

    def run(self):
        print("Stealth Exam Solver Running (Drop-Box Edition)...")
        print(f"Screen Size: {self.screen_width}x{self.screen_height}")
        print(f"OS: {platform.system()}")
        print("- Click BOTTOM-LEFT corner -> Drop-Box MCQ Mode (Reads A/B/C/D from clipboard)")
        print("- Click BOTTOM-RIGHT corner -> Drop-Box Ghost Mode (reads answer.txt or clipboard)")
        
        # Keep process alive and listen to mouse
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
            
    def get_answer_text(self):
        answer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "answer.txt")
        answer_text = ""
        
        # 1. Try reading the text file dropped by your friend
        try:
            if os.path.exists(answer_path):
                with open(answer_path, "r", encoding="utf-8") as f:
                    answer_text = f.read().strip()
                # Empty the file to prevent accidental reuse
                open(answer_path, "w").close()
        except Exception as e:
            print(f"[Main] File read error: {e}")
            
        # 2. Try the Clipboard if the file was empty
        if not answer_text:
            try:
                import pyperclip
                answer_text = pyperclip.paste().strip()
            except Exception as e:
                pass
                
        return answer_text

    def trigger_mcq(self):
        play_sound("Pop")
        mcq_answer = self.get_answer_text()
        
        if mcq_answer and len(mcq_answer) <= 5: # Valid MCQ answer (A, B, C, D)
            print(f"[Main] Pulled MCQ Answer: {mcq_answer}")
            move_mouse_to_quadrant(mcq_answer)
        else:
            print("[Main] Failed to get valid MCQ answer from clipboard/file. Current clipboard might be code.")
            play_sound("Basso")
        
    def trigger_coding(self):
        play_sound("Pop")
        code_answer = self.get_answer_text()
        

        
        if code_answer:
            play_sound("Tink")
            print(f"[Main] Activating Key Substitution Ghost with {len(code_answer)} characters!")
            self.ghost.start_typing(code_answer)
        else:
            print("[Main] Failed to get code answer (answer.txt and clipboard are both empty).")
            play_sound("Basso")

if __name__ == "__main__":
    controller = StealthController()
    controller.run()
