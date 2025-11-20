
# BiRefNet Background Remover (Enhanced GUI)

A modern, lightweight desktop utility that uses Artificial Intelligence to remove image backgrounds in bulk. Simply place your images in the `input/` folder, run the application, click "Start", and get transparent PNGs in the `output/` folder.

This project is a Graphical User Interface (GUI) built around the Hugging Face **ZhengPeng7/BiRefNet** model, utilizing **PyTorch** and **Transformers** for inference. The interface is built with **Tkinter** (using a modern theme) and uses **Pillow** for image manipulation.


## Prerequisites

The only requirement you need installed is **[uv](https://github.com/astral-sh/uv)**. `uv` will handle installing Python and the necessary libraries.

This project uses `uv` to avoid manual virtual environment (`venv`) or `pip` management.

1.  **Run the application:**
    Simply run this command. `uv` will detect dependencies (`torch`, `transformers`, etc.), automatically create the isolated environment, and launch the app:

    ```bash
    uv run app.py
    ```

    *(Note: The first time you run it, `uv` will take a few seconds to install libraries, and then the App will take a few minutes to download the AI model from Hugging Face).*

## How to Use

1.  Place the images you want to process in the `input/` folder.
2.  Launch the GUI with the command above (`uv run app_birefnet_v2.py`).
3.  Wait for the loading bar to finish preparing the model.
4.  Click the **"Start Processing"** button.
5.  The progress bar will show the status. Once finished, check the `output/` folder.


## Credits

* **AI Model:** [ZhengPeng7/BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet)
