import os
import subprocess

import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self, text="Select Video", command=self.select_video)
        self.select_button.pack(side="top")

        self.volume_label = tk.Label(self, text="Increase Volume By (dB):")
        self.volume_label.pack(side="top")
        self.volume_entry = tk.Entry(self)
        self.volume_entry.pack(side="top")

        self.cut_label = tk.Label(self, text="Cut Start Duration (seconds):")
        self.cut_label.pack(side="top")
        self.cut_entry = tk.Entry(self)
        self.cut_entry.pack(side="top")
        self.cut_entry.insert(0, "0.9")  # Default value pre-filled

        self.test_run_var = tk.BooleanVar()
        self.test_run_check = tk.Checkbutton(self, text="Test Run (First 60 seconds)", variable=self.test_run_var)
        self.test_run_check.pack(side="top")

        self.process_button = tk.Button(self, text="Process Video", command=self.process_video)
        self.process_button.pack(side="top")

        self.quit_button = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def select_video(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi")])
        if self.filename:
            required_gain = self.analyze_sound()
            self.volume_entry.delete(0, tk.END)
            self.volume_entry.insert(0, str(required_gain))

    def analyze_sound(self):
        cmd = f"ffmpeg -i \"{self.filename}\" -af \"volumedetect, atrim=start=5\" -vn -sn -dn -f null -"
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        mean_volume = self.extract_mean_volume(result.stderr)
        if mean_volume is not None:
            target_volume = -25.7
            required_gain = target_volume - mean_volume
            return required_gain
        else:
            print("Could not determine mean volume.")
            return 0

    def extract_mean_volume(self, ffmpeg_output):
        import re
        match = re.search(r"mean_volume: ([-\d.]+) dB", ffmpeg_output)
        if match:
            return float(match.group(1))
        return None

    def process_video(self):
        volume = self.volume_entry.get()
        cut_time = self.cut_entry.get()
        test_run = self.test_run_var.get()

        output_name = f"{self.filename.rsplit('.', 1)[0]}-out.mp4"

        # Check if output file already exists and delete if it does
        if os.path.exists(output_name):
            os.remove(output_name)
            print(f"Deleted existing file: {output_name}")
            
        cmd = [
            'ffmpeg',
            '-ss', cut_time,
            '-i', self.filename,
            '-filter:a', f"volume={volume}dB",
            '-vcodec', 'copy',
            # '-acodec', 'copy',
        ]

        if test_run:
            cmd.extend(['-t', '60'])

        output_name = f"{self.filename.rsplit('.', 1)[0]}-out.mp4"
        cmd.extend([output_name])
        print('Executing:', ' '.join(cmd))
        subprocess.run(cmd, shell=True)
        print("Processing completed!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
