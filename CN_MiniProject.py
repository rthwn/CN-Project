import socket
import threading
from queue import Queue
import tkinter as tk
import ssl
import os
import tempfile

# Define the number of threads to use
thread_count = 3000


def generate_certificate():
    cert_file = tempfile.NamedTemporaryFile(delete=False)
    key_file = tempfile.NamedTemporaryFile(delete=False)
    cert_file.close()
    key_file.close()

    cert_path = cert_file.name
    key_path = key_file.name

    # Generate certificate
    os.system(f"openssl req -new -x509 -keyout {key_path} -out {cert_path} -days 365 -subj /CN=localhost -nodes")

    return cert_path, key_path


# Function to perform TCP port scanning
def tcp_portscan(target, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

# Copy elements in port_list to queue
def fill_queue(start_port, end_port, queue):
    port_list = range(start_port, end_port + 1)
    for port in port_list:
        queue.put(port)
    # Add a sentinel value to indicate the end of the queue
    for _ in range(thread_count):
        queue.put(None)

# Worker thread function
def worker(queue, open_ports):
    while True:
        port = queue.get()
        if port is None:  # Check for sentinel value
            break
        if tcp_portscan(target_ip, port, timeout):
            open_ports.append(port)
        queue.task_done()

# Function to start port scanning
def start_scan():
    global target_ip, start_port, end_port, timeout
    target_ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    timeout = int(timeout_entry.get())

    queue = Queue()
    open_ports = []

    fill_queue(start_port, end_port, queue)

    thread_list = []
    for _ in range(thread_count):
        thread = threading.Thread(target=worker, args=(queue, open_ports))
        thread.start()
        thread_list.append(thread)

    # Wait for all worker threads to complete
    for thread in thread_list:
        thread.join()

    # Update result text area
    if open_ports:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Open ports are: " + str(open_ports))
        result_text.config(state=tk.DISABLED)
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No open ports found.")
        result_text.config(state=tk.DISABLED)

# Create GUI
root = tk.Tk()
root.title("Port Scanner")
root.configure(bg="#f0f0f0")

# Frame
frame = tk.Frame(root, bg="black", padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Labels
tk.Label(frame, text="Target IP:", bg="grey", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
tk.Label(frame, text="Start Port:", bg="grey", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
tk.Label(frame, text="End Port:", bg="grey", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
tk.Label(frame, text="Timeout:", bg="grey", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")

# Entry fields
ip_entry = tk.Entry(frame, font=("Helvetica", 12))
ip_entry.grid(row=0, column=1, padx=10, pady=5)
start_port_entry = tk.Entry(frame, font=("Helvetica", 12))
start_port_entry.grid(row=1, column=1, padx=10, pady=5)
end_port_entry = tk.Entry(frame, font=("Helvetica", 12))
end_port_entry.grid(row=2, column=1, padx=10, pady=5)
timeout_entry = tk.Entry(frame, font=("Helvetica", 12))
timeout_entry.grid(row=3, column=1, padx=10, pady=5)

# Scan button
scan_button = tk.Button(frame, text="Scan Ports", command=start_scan, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="raised")
scan_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Result text area
result_text = tk.Text(root, height=50, width=80)
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)

root.mainloop()
