import tkinter as tk
import customtkinter
import replicate
from PIL import ImageTk
from urllib.request import urlopen

# API tokenini sozlash
replicate_client = replicate.Client(api_token="r8_MdrmJD9bAgifP0VZWpInoMELG6QNx771ihr9I")

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asliddin AI Image Generator App")
        
        # UI elementlari
        self.heading = customtkinter.CTkLabel(root, text="Qanday rasm kerakligini Yozing")
        self.heading.pack(padx=10, pady=10)

        # Prompt kiritish
        self.promptVariable = tk.StringVar()
        self.prompt = customtkinter.CTkEntry(root, width=400, height=50, textvariable=self.promptVariable)
        self.prompt.pack(padx=10, pady=10)

        # Run tugmasi
        self.run = customtkinter.CTkButton(root, text="Run", command=self.generate_image)
        self.run.pack(padx=10, pady=10)

        # Tasvir
        self.image_label = customtkinter.CTkLabel(root, text="")
        self.image_label.pack()

    def generate_image(self):
        # Kirishni va tugmani ishlovchi holatga o'tkazish
        self.prompt.configure(state='disabled')
        self.run.configure(state='disabled')

        # Yuklanayotgan xabarni ko'rsatish
        self.run.configure(text="Running...")

        # Promptni olish
        prompt = self.promptVariable.get()

        try:
            # Tasvir yaratish
            image_url = self.generate_image_from_prompt(prompt)
            # Tasvirni ko'rsatish
            self.display_image(image_url)
        except Exception as e:
            # Xatolikni ko'rsatish
            self.image_label.configure(text=f"Error: {e}")
        finally:
            # Kirishni va tugmani ishlovchi holatga qaytarish
            self.prompt.configure(state='normal')
            self.run.configure(state='normal')
            self.run.configure(text="Run")

    def generate_image_from_prompt(self, prompt):
        output = replicate_client.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "width": 768,
                "height": 768,
                "prompt": prompt,
                "scheduler": "DPMSolverMultistep",
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50
            }
        )
        return output[0]

    def display_image(self, image_url):
        # Tasvirni olish
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()

        # Tasvirni ko'rsatish
        photo = ImageTk.PhotoImage(data=raw_data)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

if __name__ == "__main__":
    # Tizim sozlamalari
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # Ilova ramkasi
    root = customtkinter.CTk()
    root.geometry('1400x800')
    app = ImageGeneratorApp(root)
    root.mainloop()
