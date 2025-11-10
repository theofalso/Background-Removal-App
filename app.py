import tkinter as tk
from tkinter import ttk, font, messagebox
from PIL import Image, ImageTk
import os
import threading


try:
    import torch
    from transformers import AutoModelForImageSegmentation
    from torchvision import transforms
except ImportError:
    messagebox.showerror(
        "Requeriments not installed",
        ""
        "pip install -r requirements_manual.txt"
    )
    exit()


INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
MAX_DISPLAY_WIDTH = 400
MAX_DISPLAY_HEIGHT = 400
MODEL_NAME = "ZhengPeng7/BiRefNet" 


BG_COLOR = "#F5F5F5"
CANVAS_BG = "#FFFFFF"
BORDER_COLOR = "#B0B0B0"
TEXT_COLOR = "#212121"
BTN_COLOR = "#007BFF"
BTN_HOVER = "#0056b3"
BTN_TEXT = "#FFFFFF"
STATUS_TEXT = "#424242"
BAR_COLOR = "#007BFF"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Background-removal-app)")
        self.root.geometry("500x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

    
        self.model = None
        self.transform = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Status.TLabel', font=('Helvetica', 10), foreground=STATUS_TEXT)
        

        self.style.configure('TButton', 
            background=BTN_COLOR, 
            foreground=BTN_TEXT, 
            borderwidth=0,
            font=('Helvetica', 10, 'bold')
        )
        self.style.map('TButton', 
            background=[('active', BTN_HOVER), ('disabled', BG_COLOR)]
        )
        

        self.style.configure('TProgressbar', 
            troughcolor=BG_COLOR, 
            background=BAR_COLOR, 
            bordercolor=BG_COLOR,
            lightcolor=BAR_COLOR,
            darkcolor=BAR_COLOR
        )

 
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        title_label = ttk.Label(main_frame, text="Background-removal-app", style="Header.TLabel")
        title_label.pack(pady=(0, 20))

        self.canvas = tk.Canvas(main_frame, 
            width=MAX_DISPLAY_WIDTH, 
            height=MAX_DISPLAY_HEIGHT, 
            bg=CANVAS_BG, 
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.canvas.pack(pady=10)
        self.canvas_text = self.canvas.create_text(
            MAX_DISPLAY_WIDTH/2, MAX_DISPLAY_HEIGHT/2, 
            text="Loading model...", 
            fill="#888", 
            font=('Helvetica', 10, 'italic')
        )

        self.status_label = ttk.Label(main_frame, text="Loading...", style="Status.TLabel")
        self.status_label.pack(pady=(10, 5))


        self.progress_bar = ttk.Progressbar(main_frame, 
            orient='horizontal', 
            mode='indeterminate',
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, padx=10)
        self.progress_bar.start(10)

        self.start_button = ttk.Button(main_frame, 
            text="Loading model...", 
            command=self.start_processing_thread
        )
        self.start_button.pack(pady=20, ipady=10, fill=tk.X, padx=10)
        self.start_button.config(state=tk.DISABLED)
    
        os.makedirs(INPUT_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        threading.Thread(target=self.load_model, daemon=True).start()

    def load_model(self):
        try:
            self.root.after(0, self.update_status, f"Loading model...: {MODEL_NAME} en {self.device}...")
            
            self.model = AutoModelForImageSegmentation.from_pretrained(
                MODEL_NAME, trust_remote_code=True
            )
            self.model.to(self.device)
            self.model.eval() 
            
            self.transform = transforms.Compose([
                transforms.Resize((1024, 1024)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])

            self.root.after(0, self.update_status, f"¡Model load in {self.device}!")
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL, text="Start"))
            
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, lambda: self.progress_bar.config(mode='determinate', value=0))
            
            self.root.after(0, self.canvas.delete, self.canvas_text)
            self.canvas_text = self.root.after(0, lambda: self.canvas.create_text(
                MAX_DISPLAY_WIDTH/2, MAX_DISPLAY_HEIGHT/2, 
                text="Ready to process", fill="#888"
            ))

        except Exception as e:
            messagebox.showerror("Error de Modelo", f"Load model fail \nDo you have internet conection?\a\nError: {e}")
            self.root.after(0, self.update_status, "Fatal error")
            self.root.after(0, self.progress_bar.stop)

    def update_status(self, text):
        self.status_label.config(text=text)
    
    def set_progress(self, value):
        self.progress_bar['value'] = value

    def update_image(self, pil_image):
        try:
            pil_image.thumbnail((MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(pil_image)
            self.canvas.delete("all")
            x = (MAX_DISPLAY_WIDTH - self.photo_image.width()) // 2
            y = (MAX_DISPLAY_HEIGHT - self.photo_image.height()) // 2
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)
        except Exception as e:
            print(f"Error: {e}")

    def start_processing_thread(self):
        self.start_button.config(state=tk.DISABLED, text="Processing...")
        self.update_status("loading...")
        self.progress_bar['value'] = 0
        
        processing_thread = threading.Thread(target=self.process_images)
        processing_thread.daemon = True
        processing_thread.start()

    def process_images(self):
        if not self.model:
            self.root.after(0, self.update_status, "Model not load yet")
            return
            
        try:
            image_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            if not image_files:
                self.root.after(0, self.update_status, "There is no images in input")
                return

            total = len(image_files)
            for i, filename in enumerate(image_files):
                status_msg = f"Working... {i+1}/{total}: {filename}"
                self.root.after(0, self.update_status, status_msg)
                
                progress_value = ((i + 1) / total) * 100
                self.root.after(0, self.set_progress, progress_value)
                
                input_path = os.path.join(INPUT_FOLDER, filename)
                output_filename = os.path.splitext(filename)[0] + "_no_bg.png"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                try: 
                    original_image = Image.open(input_path).convert("RGB")
                    image_size = original_image.size
                    self.root.after(0, self.update_image, original_image.copy())

                    input_tensor = self.transform(original_image).unsqueeze(0).to(self.device)

                    with torch.no_grad():
                        preds = self.model(input_tensor)[-1].sigmoid().cpu()
                    
                    pred = preds[0].squeeze()
                    pred_pil = transforms.ToPILImage()(pred)
                    mask = pred_pil.resize(image_size)

                    original_image.putalpha(mask)
                    original_image.save(output_path, "PNG")

                except Exception as e:
                    print(f"Processing Error {filename}: {e}")
                    self.root.after(0, self.update_status, f"Error in {filename}. Skiping...")
            
            self.root.after(0, self.update_status, f"¡Process completed! {total}")
            self.root.after(0, self.canvas.delete, "all")
            self.root.after(0, lambda: self.canvas.create_text(
                MAX_DISPLAY_WIDTH/2, MAX_DISPLAY_HEIGHT/2, 
                text="Finished", fill="green", font=('Helvetica', 12, 'bold')
            ))

        except Exception as e:
            print(f"General Error {e}")
            self.root.after(0, self.update_status, f"Error: {e}")
        finally:
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL, text="Start Process"))
            self.root.after(0, self.set_progress, 0)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()