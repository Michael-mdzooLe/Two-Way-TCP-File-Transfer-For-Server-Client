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

def download_file(server_ip, port, filename, log_box):
    if not filename.strip():
        messagebox.showerror("Error", "Please enter a file name to download.")
        return

    client_socket = socket.socket()
    try:
        client_socket.connect((server_ip, port))
        client_socket.send("DOWNLOAD".encode())
        client_socket.recv(BUFFER_SIZE)  # Wait for ACK
        client_socket.send(filename.encode())

        response = client_socket.recv(BUFFER_SIZE).decode()
        if response.startswith("NOTFOUND"):
            log_box.insert(tk.END, f"[✗] File not found: {filename}")
            client_socket.close()
            return

        fname, fsize = response.split(SEPARATOR)
        fsize = int(fsize)

        with open(f"downloaded_{fname}", "wb") as f:
            total = 0
            while total < fsize:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                total += len(bytes_read)

        log_box.insert(tk.END, f"[✓] Downloaded: downloaded_{fname}")
    except Exception as e:
        messagebox.showerror("Download Error", str(e))
    finally:
        client_socket.close()

def browse_file(file_label):
    filepath = filedialog.askopenfilename()
    file_label.config(text=filepath)

def start_client_gui():
    window = tk.Tk()
    window.title("TCP File Client")
    window.geometry("550x400")

    tk.Label(window, text="Server IP:").pack()
    ip_entry = tk.Entry(window)
    ip_entry.insert(0, "127.0.0.1")
    ip_entry.pack()

    file_label = tk.Label(window, text="No file selected")
    file_label.pack()

    browse_button = ttk.Button(window, text="Browse File", command=lambda: browse_file(file_label))
    browse_button.pack(pady=5)

    send_button = ttk.Button(window, text="Upload File", command=lambda: send_file(ip_entry.get(), 5001, file_label.cget("text"), log_box))
    send_button.pack(pady=5)

