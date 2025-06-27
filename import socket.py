import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def send_file(server_ip, port, filepath, log_box):
    if not os.path.exists(filepath):
        messagebox.showerror("Error", "No file selected.")
        return

    filesize = os.path.getsize(filepath)
    client_socket = socket.socket()
