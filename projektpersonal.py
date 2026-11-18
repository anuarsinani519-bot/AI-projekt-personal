
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from weather_classifier import predict_weather


# ============================================================
# SETTINGS
# ============================================================

APP_TITLE = "Weather AI Classifier"

UPLOAD_BUTTON_TEXT = "Choose Weather Image"

EMPTY_IMAGE_TEXT = "Upload a weather image"

RESULT_EMPTY_TEXT = "Weather prediction will appear here"

PREVIEW_SIZE = (320, 240)


# ============================================================
# WEATHER APP
# ============================================================

class WeatherApp:

    def __init__(self, root):

        self.root = root

        self.root.title(APP_TITLE)
        self.root.geometry("560x600")
        self.root.resizable(False, False)

        self.root.configure(bg="#101827")

        self.preview_image = None

        # TITLE

        self.title_label = tk.Label(
            root,
            text="WEATHER AI",
            font=("Segoe UI", 24, "bold"),
            fg="#60A5FA",
            bg="#101827"
        )

        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = tk.Label(
            root,
            text="Artificial Intelligence Weather Detection",
            font=("Segoe UI", 10),
            fg="#94A3B8",
            bg="#101827"
        )

        self.subtitle_label.pack(pady=(0, 15))

        # IMAGE PREVIEW

        self.image_label = tk.Label(
            root,
            text=EMPTY_IMAGE_TEXT,
            width=42,
            height=12,
            relief="solid",
            borderwidth=1,
            bg="#1E293B",
            fg="#CBD5E1",
            font=("Segoe UI", 11)
        )

        self.image_label.pack(pady=10)

        # UPLOAD BUTTON

        self.choose_button = tk.Button(
            root,
            text=UPLOAD_BUTTON_TEXT,
            command=self.choose_image,
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )

        self.choose_button.pack(pady=12)

        # WEATHER RESULT

        self.result_label = tk.Label(
            root,
            text=RESULT_EMPTY_TEXT,
            font=("Segoe UI", 18, "bold"),
            fg="#F8FAFC",
            bg="#101827"
        )

        self.result_label.pack(pady=(20, 8))

        # CONFIDENCE

        self.confidence_label = tk.Label(
            root,
            text="Confidence: -",
            font=("Segoe UI", 12),
            fg="#38BDF8",
            bg="#101827"
        )

        self.confidence_label.pack()

        # IMAGE PATH

        self.path_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 9),
            wraplength=480,
            fg="#94A3B8",
            bg="#101827"
        )

        self.path_label.pack(pady=15)

        # FOOTER

        self.footer_label = tk.Label(
            root,
            text="POWERED BY TENSORFLOW",
            font=("Segoe UI", 9, "bold"),
            fg="#64748B",
            bg="#101827"
        )

        self.footer_label.pack(side="bottom", pady=15)


    # ========================================================
    # IMAGE UPLOAD
    # ========================================================

    def choose_image(self):

        image_path = filedialog.askopenfilename(

            title="Choose Weather Image",

            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All files", "*.*"),
            ],

        )

        if not image_path:
            return

        self.show_preview(image_path)

        self.predict(image_path)


    # ========================================================
    # IMAGE PREVIEW
    # ========================================================

    def show_preview(self, image_path):

        image = Image.open(image_path).convert("RGB")

        image.thumbnail(PREVIEW_SIZE)

        self.preview_image = ImageTk.PhotoImage(image)

        self.image_label.configure(
            image=self.preview_image,
            text="",
            width=320,
            height=240
        )

        self.path_label.configure(
            text=str(Path(image_path))
        )


    # ========================================================
    # WEATHER PREDICTION
    # ========================================================

    def predict(self, image_path):

        try:

            result = predict_weather(image_path)

        except Exception as error:

            messagebox.showerror(
                "Weather AI Error",
                str(error)
            )

            return

        weather = result["weather"]

        confidence = result["confidence"]

        self.result_label.configure(
            text=f"Weather: {weather.upper()}"
        )

        self.confidence_label.configure(
            text=f"Confidence: {confidence:.2f}%"
        )


# ============================================================
# START APPLICATION
# ============================================================

def main():

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()


if __name__ == "__main__":

    main()
