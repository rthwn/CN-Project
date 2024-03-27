import socket
import tkinter as tk

def scan_ports():
    target_host = host_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())

    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target_host, port))
                s.sendall(b'GET / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(target_host).encode())
                response = s.recv(1024)
                if b'HTTP' in response:
                    open_ports.append(port)
        except:
            pass

    result_text.config(state=tk.NORMAL)
    if open_ports:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Open HTTP Ports: {open_ports}")
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No open HTTP ports found.")
    result_text.config(state=tk.DISABLED)

# Create GUI
root = tk.Tk()
root.title("HTTP Port Scanner")

frame = tk.Frame(root, bg="black", padx=20, pady=20)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Target Host:", bg="grey", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
tk.Label(frame, text="Start Port:", bg="grey", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
tk.Label(frame, text="End Port:", bg="grey", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")

host_entry = tk.Entry(frame, font=("Helvetica", 12))
host_entry.grid(row=0, column=1, padx=10, pady=5)
start_port_entry = tk.Entry(frame, font=("Helvetica", 12))
start_port_entry.grid(row=1, column=1, padx=10, pady=5)
end_port_entry = tk.Entry(frame, font=("Helvetica", 12))
end_port_entry.grid(row=2, column=1, padx=10, pady=5)

scan_button = tk.Button(frame, text="Scan Ports", command=scan_ports, bg="#4CAF50", fg="white", font=("Helvetica", 12), relief="raised")
scan_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

result_text = tk.Text(root, height=5, width=50)
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)

root.mainloop()
