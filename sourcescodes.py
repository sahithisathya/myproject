import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
import os

def select_image(image_list):
    def on_image_select(image_path, is_accident=False):
        selected_image.set(image_path)
        selected_image.is_accident = is_accident
        selected_image.img = Image.open(image_path)
        selected_image.img = selected_image.img.resize((600, 400))  # Resize the image for display
        selected_image.img_tk = ImageTk.PhotoImage(selected_image.img)
        show_image()
        top.destroy()

    random.shuffle(image_list)  # Shuffle the list of images

    top = tk.Toplevel(root)
    top.title("Select Image")
    top.geometry("800x600")  # Original size of the pop-up window

    for i, image_path in enumerate(image_list):
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        is_accident = "non_accident" not in os.path.basename(image_path).lower()  # Check if filename contains "non_accident"
        btn_text = "Accident" if is_accident else "No Accident Found"
        btn = ttk.Button(top, image=img_tk, compound=tk.BOTTOM, command=lambda image_path=image_path, is_accident=is_accident: on_image_select(image_path, is_accident))
        btn.image = img_tk
        btn.grid(row=i//2, column=i%2, padx=5, pady=5)

def show_image():
    user_input = selected_image.get()
    if user_input:
        img_tk = selected_image.img_tk
        if selected_image.is_accident:
            accident_image_label.configure(image=img_tk, text="Accident", compound=tk.BOTTOM)
            accident_image_label.image = img_tk
            accident_image_label.pack()
            non_accident_image_label.pack_forget()  # Hide non-accident image label
        else:
            accident_image_label.configure(image=img_tk, text="No Accident Found", compound=tk.BOTTOM)
            accident_image_label.image = img_tk
            accident_image_label.pack()
            non_accident_image_label.pack_forget()  # Hide accident image label
    else:
        accident_image_label.pack_forget()
        non_accident_image_label.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Accident Detection")
root.geometry("400x400")  # Set window size to accommodate the image

# Create image label but don't pack it initially
accident_image_label = tk.Label(root)
non_accident_image_label = tk.Label(root)

# Create heading label
heading_label = tk.Label(root, text="Accident Detection", font=("Helvetica", 16))
heading_label.pack(pady=10)

# Create entry widget for user input
selected_image = tk.StringVar()

# Button to select the image folder
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        images = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.jpg')]
        select_image(images)

select_button = tk.Button(root, text="Select Image Folder", command=browse_folder)
select_button.pack()

root.mainloop()
