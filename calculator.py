import tkinter as tk
import random
import os # Import os to construct file paths reliably

# Import the playsound function
try:
    # Using 1.3.0 as 1.2.2 often has issues, especially on Linux/Mac.
    # If 1.3.0 fails, try 1.2.2 again or look for platform-specific alternatives.
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    print("Warning: 'playsound' library not found or installation issue.")
    print("Install it using: pip install playsound") # Recommend latest unless specific issues
    # print("Or try specific version: pip install playsound==1.2.2") # If latest fails
    print("Sound effects will not play.")
    PLAYSOUND_AVAILABLE = False

# --- Configuration ---
# Make sure this sound file exists in the same directory as the script,
# or provide the full path to the sound file.
EMOJI_SOUND_FILE = "untitled.wav" # Sound for the emoji button

# --- NEW: Fanfare Sound Configuration ---
SOUND_DIR = "sounds" # Name of the subdirectory containing fanfare sounds
# IMPORTANT: Create a folder named "sounds" next to your script
# and place your 10 MP3 files inside it. List their names here:
FANFARE_SOUND_FILES = [
    "fanfare1.mp3", # Replace with your actual MP3 filenames
    "fanfare2.mp3",
    "fanfare3.mp3",
    "fanfare4.mp3",
    "fanfare5.mp3",
    "fanfare6.mp3",
    "fanfare7.mp3",
    "fanfare8.mp3",
    "fanfare9.mp3",
    "fanfare10.mp3",
]
# --- End NEW Fanfare Sound Configuration ---


EQUALS_CLICK_THRESHOLD = 10 # How many '=' clicks trigger the fanfare
FANFARE_DURATION_MS = 2500 # How long the fanfare window stays open (milliseconds)
# --- End Configuration ---


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.expression = ""
        self.result_displayed = False
        self.equals_click_count = 0 # Counter for '=' clicks

        # Get the directory where the script is running
        self.script_dir = os.path.dirname(__file__)

        # Construct the full path to the *emoji* sound file
        self.emoji_sound_path = os.path.join(self.script_dir, EMOJI_SOUND_FILE)

        # --- NEW: Construct the path to the sounds directory ---
        self.fanfare_sound_dir = os.path.join(self.script_dir, SOUND_DIR)
        # --- End NEW ---

        self.entry = tk.Entry(master, width=25, borderwidth=5, font=('Arial', 16), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Define buttons (same as before)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3),
            ('=', 5, 0), ('C', 5, 1), ('Back', 5, 2), ('😎', 5, 3)
        ]

        # Create and place buttons (same logic as before)
        for (text, row, col) in buttons:
            if text == '=':
                button = tk.Button(master, text=text, padx=20, pady=20, command=self.calculate, font=('Arial', 14), bg=('#FA8072'))
            elif text == 'C':
                button = tk.Button(master, text=text, padx=20, pady=20, command=self.clear, font=('Arial', 14), bg=('#40E0D0'))
            elif text == 'Back':
                button = tk.Button(master, text=text, padx=20, pady=20, command=self.backspace, font=('Arial', 14), bg=('#40E0D0'))
            elif text == '😎':
                button = tk.Button(master, text=text, padx=0, pady=0, command=self.play_emoji_sound, font=('Arial', 30), bg=('yellow'))
            else:
                button = tk.Button(master, text=text, padx=20, pady=20, command=lambda t=text: self.press(t), font=('Arial', 14), bg=('#40E0D0'))

            button.grid(row=row, column=col, padx=5, pady=5)

    def press(self, key):
        # Same logic as before
        if self.result_displayed:
            if key in ['+', '-', '*', '/', '%']:
                pass
            else:
                self.clear()
        self.expression += str(key)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)

    def calculate(self):
        # --- Fanfare Trigger Logic ---
        self.equals_click_count += 1
        print(f"= clicked {self.equals_click_count} times.") # Optional debug print
        if self.equals_click_count >= EQUALS_CLICK_THRESHOLD:
            self.play_fanfare_animation() # Keep the animation
            self.play_random_fanfare_sound() # <--- ADDED: Play random sound
            self.equals_click_count = 0 # Reset the counter
        # --- End Fanfare Trigger Logic ---

        if not self.expression:
             return
        try:
            # Simple eval - Be cautious with eval in real applications
            eval_expr = self.expression.replace('%', '/100.0') # Ensure float division for %
            # More robust eval protection (optional but recommended)
            # result = eval(eval_expr, {"__builtins__": None}, {}) # Restrict eval scope
            result = eval(eval_expr) # Using standard eval as in original code
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
            self.expression = str(result)
            self.result_displayed = True
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Div by Zero Error")
            self.expression = ""
            self.result_displayed = True
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")
            print(f"Calculation Error: {e}")
            self.expression = ""
            self.result_displayed = True

    def clear(self):
        # Same as before
        self.entry.delete(0, tk.END)
        self.expression = ""
        self.result_displayed = False
        # self.equals_click_count = 0 # Optionally reset counter on Clear too

    def backspace(self):
        # Same as before
        if self.result_displayed:
            self.clear()
        else:
            current_text = self.entry.get()
            new_text = current_text[:-1]
            self.expression = new_text
            self.entry.delete(0, tk.END)
            self.entry.insert(0, new_text)
            self.result_displayed = False

    def play_emoji_sound(self):
        """Plays the sound effect for the emoji button."""
        if not PLAYSOUND_AVAILABLE:
            print("Cannot play sound: playsound library not available.")
            return

        try:
            print(f"Attempting to play emoji sound: {self.emoji_sound_path}") # Debug print
            if os.path.exists(self.emoji_sound_path):
                 playsound(self.emoji_sound_path, block=False) # block=False to avoid freezing GUI
            else:
                 print(f"Error: Emoji sound file not found at {self.emoji_sound_path}")
                 self._show_temp_error("Emoji Sound Missing")

        except Exception as e:
            print(f"Error playing emoji sound {self.emoji_sound_path}: {e}")
            self._show_temp_error("Sound Error")


    # --- NEW Fanfare Sound Method ---
    def play_random_fanfare_sound(self):
        """Plays a random sound from the FANFARE_SOUND_FILES list."""
        if not PLAYSOUND_AVAILABLE:
            print("Cannot play fanfare sound: playsound library not available.")
            return

        if not FANFARE_SOUND_FILES:
            print("Warning: No fanfare sound files listed in FANFARE_SOUND_FILES.")
            return

        try:
            # Choose a random sound file
            chosen_sound_file = random.choice(FANFARE_SOUND_FILES)
            full_sound_path = os.path.join(self.fanfare_sound_dir, chosen_sound_file)

            print(f"Attempting to play fanfare sound: {full_sound_path}") # Debug print

            if os.path.exists(full_sound_path):
                 playsound(full_sound_path, block=False) # block=False is crucial for GUI responsiveness
            else:
                 print(f"Error: Fanfare sound file not found at {full_sound_path}")
                 # Optionally show an error in the calculator display
                 self._show_temp_error("Fanfare Sound Missing")

        except Exception as e:
            # Catch potential errors from playsound itself (e.g., codec issues)
            print(f"Error playing fanfare sound {full_sound_path}: {e}")
            self._show_temp_error("Sound Play Error")
    # --- End NEW Fanfare Sound Method ---


    # --- New Fanfare Animation Method (same as before) ---
    def play_fanfare_animation(self):
        """Creates a temporary window with a fanfare message."""
        fanfare_window = tk.Toplevel(self.master)
        fanfare_window.title("🎉")
        fanfare_window.geometry("300x150")
        fanfare_window.resizable(False, False)
        fanfare_window.attributes('-topmost', True)

        # Center the fanfare window
        self.master.update_idletasks()
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_w = self.master.winfo_width()
        main_h = self.master.winfo_height()
        fanfare_w = 300
        fanfare_h = 150
        center_x = main_x + (main_w // 2) - (fanfare_w // 2)
        center_y = main_y + (main_h // 2) - (fanfare_h // 2)
        fanfare_window.geometry(f"{fanfare_w}x{fanfare_h}+{center_x}+{center_y}")

        fanfare_label = tk.Label(
            fanfare_window,
            text="✨✨ WOW! ✨✨\n10 Calculations!",
            font=('Arial', 20, 'bold'),
            pady=20,
            bg="gold",
            fg="darkblue"
        )
        fanfare_label.pack(expand=True, fill='both')
        fanfare_window.after(FANFARE_DURATION_MS, fanfare_window.destroy)

    # --- Helper method to show temporary errors in entry ---
    def _show_temp_error(self, message):
        """Displays an error message in the entry field temporarily."""
        try:
            prev_text = self.entry.get() # Store previous text if possible
            self.entry.delete(0, tk.END)
            self.entry.insert(0, message)
            # Schedule reverting back after 1.5 seconds
            self.master.after(1500, lambda: (self.entry.delete(0, tk.END), self.entry.insert(0, prev_text)))
        except Exception as e:
            print(f"Error displaying temporary message: {e}") # Avoid crashing if GUI is gone


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    # Ensure the main window gets focus initially if needed
    root.focus_force()
    calculator = Calculator(root)
    root.mainloop()