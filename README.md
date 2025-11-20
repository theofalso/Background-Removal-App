Background Removal App

A lightweight GUI utility that loads a pretrained image segmentation model to remove backgrounds from images in bulk. Drop images into the `input/` folder, run the GUI, press Start, and processed PNGs with transparent backgrounds are saved to the `output/` folder.

This project is a small front-end around the Hugging Face model `ZhengPeng7/BiRefNet` and uses PyTorch + Transformers for inference. The GUI is implemented with Tkinter and Pillow for image display and saving.

Key features
- Simple local GUI — no web server required.
- Batch processing of images in `input/`.
- Saves outputs as PNG files with alpha channel (filename_no_bg.png).

Contents
- `app.py` — main application (Tkinter GUI, model loading, processing loop).
- `requirements.txt` — required Python packages.
- `input/` — input images directory (create or put images here).
- `output/` — output images directory (generated PNGs with transparent backgrounds).

Prerequisites
- Python 3.8+ (3.10 recommended)
- Internet connection on first run (model is downloaded from Hugging Face)
- GPU is optional; the app will use CUDA if available, otherwise CPU.

Install
1. Create and activate a virtual environment (recommended):

```powershell
# Windows PowerShell (from project folder)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app
1. Place the images you want to process in the `input/` folder. Supported formats: PNG, JPG, JPEG, WEBP.
2. Start the GUI:

```powershell
python app.py
```

3. Wait for the model to load. On the first run the model files will be downloaded from Hugging Face — this can take several minutes depending on your connection.
4. When the GUI shows Ready, click the Start button to process all images found in `input/`.
5. Results will be saved to the `output/` folder with names like `originalname_no_bg.png`.


Contributing
- Small improvements, bug fixes and README/packaging updates are welcome. Please open issues or pull requests with a short description and steps to reproduce.
