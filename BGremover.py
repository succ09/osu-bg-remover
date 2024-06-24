import os
import shutil
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import keyboard
import pygetwindow as gw

def remove_image_files(directory):
    image_files_removed = []
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    total_image_files = sum(1 for _, _, files in os.walk(directory) for file in files if file.endswith('.jpg') or file.endswith('.png'))
    files_deleted = 0

    with tqdm(total=total_image_files, unit='file') as pbar:
        pbar.set_postfix(total_files=total_files, total_image_files=total_image_files)
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    image_files_removed.append(root)
                    files_deleted += 1
                    pbar.update(1)

    return set(image_files_removed)

def start_process(event=None):
    directory = directory_entry.get()
    if not directory:
        return
    folders_with_deleted_files = remove_image_files(directory)
    print("Folders where bg's were deleted:")
    for folder in folders_with_deleted_files:
        print(folder)

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def set_keybind(event=None):
    global keybind, terminate_keybind
    keybind = keybind_entry.get()
    terminate_keybind = terminate_keybind_entry.get()
    keyboard.add_hotkey(keybind, start_process)
    keyboard.add_hotkey(terminate_keybind, terminate_active_window)

def terminate_active_window():
    active_window = gw.getActiveWindow()
    if active_window:
        active_window.close()

root = tk.Tk()
root.title("Background Remover")

directory_label = tk.Label(root, text="Directory:")
directory_label.pack()

directory_entry = tk.Entry(root, width=50)
directory_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack()

keybind_label = tk.Label(root, text="Keybind:")
keybind_label.pack()

keybind_entry = tk.Entry(root, width=10)
keybind_entry.pack()

terminate_keybind_label = tk.Label(root, text="Terminate Keybind:")
terminate_keybind_label.pack()

terminate_keybind_entry = tk.Entry(root, width=10)
terminate_keybind_entry.pack()

set_keybind_button = tk.Button(root, text="Set Keybinds", command=set_keybind)
set_keybind_button.pack()

start_button = tk.Button(root, text="Start", command=start_process)
start_button.pack()

root.mainloop()