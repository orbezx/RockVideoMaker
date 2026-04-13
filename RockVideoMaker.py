import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import subprocess
import os
import sys

class RockvideoMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Rockvideo Maker")
        self.root.geometry("500x600")
        
        # Default Variables
        self.bg_color = "#000000"  # Default Black
        self.text_color = "#FFFFFF" # Default White
        self.is_transparent = tk.BooleanVar(value=False)
        
        ttk.Label(root, text="🎸 Rockvideo Maker", font=("Arial", 20, "bold")).pack(pady=15)
        
        # 1. Text Input
        ttk.Label(root, text="Text Content:").pack()
        self.text_entry = ttk.Entry(root, width=40)
        self.text_entry.insert(0, "ROCK ON")
        self.text_entry.pack(pady=5)

        # 2. Color Selection Frame
        color_frame = ttk.LabelFrame(root, text="Colors & Background", padding=10)
        color_frame.pack(pady=10, fill="x", padx=20)

        ttk.Button(color_frame, text="Set Text Color", command=self.pick_text_color).grid(row=0, column=0, padx=5, pady=5)
        self.text_sample = tk.Label(color_frame, text="Aa", bg="white", width=4)
        self.text_sample.grid(row=0, column=1)

        ttk.Button(color_frame, text="Set BG Color", command=self.pick_bg_color).grid(row=1, column=0, padx=5, pady=5)
        self.bg_sample = tk.Label(color_frame, text="  ", bg="black", width=4)
        self.bg_sample.grid(row=1, column=1)

        ttk.Checkbutton(color_frame, text="Transparent Background (Export as .mov)", variable=self.is_transparent).grid(row=2, column=0, columnspan=2, pady=5)

        # 3. Quality & FPS
        settings_frame = ttk.Frame(root)
        settings_frame.pack(pady=10)

        ttk.Label(settings_frame, text="Quality:").grid(row=0, column=0, padx=5)
        self.res_var = tk.StringVar(value="1080p")
        self.res_dropdown = ttk.Combobox(settings_frame, textvariable=self.res_var, width=10, state="readonly")
        self.res_dropdown['values'] = ("4k", "1080p", "720p", "480p")
        self.res_dropdown.grid(row=0, column=1, padx=5)

        ttk.Label(settings_frame, text="FPS:").grid(row=0, column=2, padx=5)
        self.fps_var = tk.StringVar(value="30")
        ttk.Entry(settings_frame, textvariable=self.fps_var, width=5).grid(row=0, column=3, padx=5)

        # 4. Render Button
        self.render_btn = ttk.Button(root, text="🔥 GENERATE VIDEO", command=self.generate_animation)
        self.render_btn.pack(pady=30)

        self.status = ttk.Label(root, text="Status: Ready", foreground="gray")
        self.status.pack(side="bottom", pady=10)

    def pick_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_color = color
            self.text_sample.config(fg=color)

    def pick_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color = color
            self.bg_sample.config(bg=color)

    def generate_animation(self):
        text_val = self.text_entry.get().strip()
        fps_val = self.fps_var.get()
        res_choice = self.res_var.get()
        
        # Map quality
        res_map = {"4k": "-qk", "1080p": "-qh", "720p": "-qm", "480p": "-ql"}
        res_flag = res_map.get(res_choice, "-qm")
        
        # Transparency flag
        trans_flag = "-t" if self.is_transparent.get() else ""

        self.status.config(text="Status: Rendering...", foreground="blue")
        self.root.update()

        script_content = f"""
from manim import *
config.frame_rate = {fps_val}
config.background_color = "{self.bg_color}"

class CustomAnim(Scene):
    def construct(self):
        txt = Text("{text_val}", font_size=72)
        txt.set_color("{self.text_color}")
        self.play(Write(txt))
        self.wait()
        self.play(FadeOut(txt))
"""
        with open("ui_anim.py", "w", encoding="utf-8") as f:
            f.write(script_content)

        try:
            # Added {trans_flag} to the command
            command = f'"{sys.executable}" -m manim {res_flag} {trans_flag} -p --flush_cache ui_anim.py CustomAnim'
            os.system(command)
            self.status.config(text="Status: Rock on! Video Done.", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RockvideoMaker(root)
    root.mainloop()