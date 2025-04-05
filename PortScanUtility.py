import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import threading
from datetime import datetime
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Port Scan Utility")
root.geometry("700x600")  # Adjusted window size for better fit
root.resizable(True, True)  # Allow resizing

# Set the background color for the main window to dark gray
root.configure(bg='#1a1a1a')

# Banner Text
ascii_banner = "Port Scan Utility"

# Add footer text (including today's date)
today_date = datetime.today().strftime('%B %Y')  # Get month and year only
footer_text = f"Created by Derek Robinson - {today_date}"

# Banner Label using Text widget to handle large text with black background and green text
banner_label = tk.Text(root, height=2, width=60, wrap=tk.WORD, font=("Courier", 24), bg='#1a1a1a', fg='#32CD32', bd=0,
                       relief="solid")
banner_label.insert(tk.END, ascii_banner)  # Insert banner text
banner_label.configure(state=tk.DISABLED)  # Make the banner uneditable
banner_label.pack(pady=10, padx=10, fill="x")  # Reduced padding to lift the banner higher

# Center the banner text by adding a tag for centering
banner_label.tag_add("center", "1.0", "end")
banner_label.tag_configure("center", justify='center')  # Center text horizontally

# Footer text in Label with light gray color on dark background
footer_label = tk.Label(root, text=footer_text, font=("Courier", 12), anchor="w", fg="#888888", bg="#1a1a1a")
footer_label.pack(side="bottom", pady=10)

# Result text box for displaying scan results with dark background
result_text = tk.Text(root, height=15, width=80, bg='#333333', fg='#ffffff', insertbackground="black", bd=0,
                      relief="solid", font=("Courier", 10))
result_text.pack(pady=10, padx=10, fill="both", expand=True)

# Scrollbar for the result text widget
scrollbar = tk.Scrollbar(result_text)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=result_text.yview)

# Entry for host IP with dark background and white text
host_label = tk.Label(root, text="Enter Host to Scan:", font=("Courier", 10), fg="white", bg="#1a1a1a")
host_label.pack(pady=5)
host_entry = tk.Entry(root, width=60, bg="#2d2d2d", fg="white", insertbackground="black", bd=2)
host_entry.pack(pady=5)

# Entry for start and end ports with dark background and white text
start_port_label = tk.Label(root, text="Start Port:", font=("Courier", 10), fg="white", bg="#1a1a1a")
start_port_label.pack(pady=5)
start_port_entry = tk.Entry(root, width=20, bg="#2d2d2d", fg="white", insertbackground="black", bd=2)
start_port_entry.pack(pady=5)

end_port_label = tk.Label(root, text="End Port:", font=("Courier", 10), fg="white", bg="#1a1a1a")
end_port_label.pack(pady=5)
end_port_entry = tk.Entry(root, width=20, bg="#2d2d2d", fg="white", insertbackground="black", bd=2)
end_port_entry.pack(pady=5)

# Function to start the scan (run in a separate thread)
def scan_ports():
    # Disable the scan button during the scan
    scan_button.config(state=tk.DISABLED)

    # Clear previous results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Scanning in progress...\n")

    host = host_entry.get()
    if not host:
        messagebox.showerror("Input Error", "Please enter a valid host.")
        scan_button.config(state=tk.NORMAL)
        return

    try:
        # Validate the IP format
        socket.inet_aton(host)  # This raises an exception if the IP is invalid
        host_ip = host
    except socket.error:
        # If it's not a valid IP, try to resolve it as a domain name
        try:
            host_ip = socket.gethostbyname(host)
        except socket.gaierror:
            messagebox.showerror("Host Error", "Host name you entered is invalid.")
            scan_button.config(state=tk.NORMAL)
            return

    result_text.insert(tk.END, f"Scanning Host: {host_ip}\n")

    # Get port range
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")
        scan_button.config(state=tk.NORMAL)
        return

    # Record the start time
    t1 = datetime.now()
    result_text.insert(tk.END, f"Start time: {t1}\n")

    # Track if any open ports are found
    open_ports_found = False

    # Scan for open ports in the specified range
    def scan():
        nonlocal open_ports_found
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a more reasonable timeout for real scans
            result = sock.connect_ex((host_ip, port))

            if result == 0:
                result_text.insert(tk.END, f"Port {port} is Open\n")
                open_ports_found = True  # Mark that an open port was found

            sock.close()

            # Update progress bar periodically
            if (port - start_port) % 10 == 0:  # Update every 10 ports
                progress_bar['value'] = (port - start_port + 1) / (end_port - start_port + 1) * 100
                root.update_idletasks()

        # If no open ports were found, display the message
        if not open_ports_found:
            result_text.insert(tk.END, "No open ports were found.\n")

        # Record the end time
        t2 = datetime.now()
        result_text.insert(tk.END, f"End time: {t2}\n")

        # Calculate and display total time
        total_time = t2 - t1
        result_text.insert(tk.END, f"Total time: {total_time}\n")

        # Re-enable the scan button after completion
        scan_button.config(state=tk.NORMAL)

    # Start the scan in a separate thread to avoid freezing the UI
    threading.Thread(target=scan, daemon=True).start()


# Function to download the results
def download_log():
    with open("Port-Scanner.txt", "r") as file:
        log_data = file.read()

    # Save the content to the user's default download location (cross-platform)
    with open("Port-Scan-Log.txt", "w") as download_file:
        download_file.write(log_data)

    messagebox.showinfo("Download", "The scan log has been downloaded as Port-Scan-Log.txt")


# Function to display About Me section
def show_about():
    about_text = "Port Scan Utility\nCreated by Derek Robinson\n\nThis tool helps you scan a given host for open ports."
    messagebox.showinfo("About Me", about_text)


# Function to display How to Use section
def show_how_to_use():
    instructions_text = ("How to Use the Port Scan Utility:\n\n"
                         "1. Enter the host (IP or domain name) in the 'Enter Host to Scan' field.\n"
                         "2. Set the start and end ports for the scan.\n"
                         "3. Click 'Start Scan' to begin scanning.\n"
                         "4. Open ports will be listed in the results area.\n"
                         "5. After the scan, you can download the scan log using 'Download Log' button.")
    messagebox.showinfo("How to Use", instructions_text)


# Menu Bar
menu_bar = tk.Menu(root)

# Add "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="About Me", command=show_about)
file_menu.add_command(label="How to Use", command=show_how_to_use)
menu_bar.add_cascade(label="Help", menu=file_menu)

# Configuring the window to use the menu
root.config(menu=menu_bar)

# Frame to hold both buttons side by side
button_frame = tk.Frame(root, bg="#1a1a1a")
button_frame.pack(pady=20)

# Start Scan Button
scan_button = tk.Button(button_frame, text="Start Scan", command=scan_ports, height=2, width=20, bg="#32CD32",
                        fg="white", font=("Courier", 12), bd=0, relief="flat")
scan_button.pack(side="left", padx=10)

# Download Button (to the right of the Start Scan button)
download_button = tk.Button(button_frame, text="Download Log", command=download_log, height=2, width=20, bg="#32CD32",
                            fg="white", font=("Courier", 12), bd=0, relief="flat")
download_button.pack(side="left", padx=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Run the GUI event loop
root.mainloop()
