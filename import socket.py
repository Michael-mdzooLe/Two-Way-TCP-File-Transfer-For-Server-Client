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
    try:
        client_socket.connect((server_ip, port))
        client_socket.send("UPLOAD".encode())
        client_socket.recv(BUFFER_SIZE)  # Wait for ACK

        client_socket.send(f"{os.path.basename(filepath)}{SEPARATOR}{filesize}".encode())

        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

        log_box.insert(tk.END, f"[✓] File uploaded: {os.path.basename(filepath)}")
    except Exception as e:
        messagebox.showerror("Upload Error", str(e))
    finally:
        client_socket.close()

