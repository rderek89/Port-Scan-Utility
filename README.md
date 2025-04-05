Port Scan Utility
Overview

The Port Scan Utility is a lightweight and easy-to-use tool designed to help users scan a given host for open ports. Built using Python and the Tkinter GUI library, it allows users to scan IP addresses or domain names to identify which ports are open and accessible. This tool is useful for network administrators, security professionals, or anyone interested in analyzing the availability of services on a network.
Features

    Scan Hosts: Enter an IP address or domain name to scan for open ports within a specified range.

    Real-time Results: View real-time results in the application window, showing which ports are open and available.

    Progress Bar: A progress bar displays the scan's progress, updating as it scans each port.

    Scan Log: The results of the scan are written to a log file (Port-Scanner.txt), which can be downloaded for later analysis.

    Intuitive Interface: The application features a simple, user-friendly interface built with Tkinter.

    Cross-Platform: The tool works on both Windows and Linux systems, offering a versatile scanning solution for various environments.

How to Use

    Enter Host: Provide an IP address or domain name in the "Enter Host to Scan" field.

    Set Port Range: Define the start and end ports to scan within the "Start Port" and "End Port" fields.

    Start Scan: Click the "Start Scan" button to begin scanning the provided host.

    Download Log: Once the scan is complete, you can download the results by clicking the "Download Log" button.

Technologies Used

    Python: The core language for this utility.

    Tkinter: Python's built-in GUI library for creating the graphical interface.

    Socket Library: Used for network communication to check the availability of ports.

    Threading: Allows the program to perform the scan without freezing the user interface.

Installation

    Clone the repository:

git clone https://github.com/yourusername/port-scan-utility.git

Install the required libraries:

pip install tkinter

Run the program:

    python port_scan_utility.py



Contributing

Feel free to open issues or submit pull requests if you have suggestions, bug fixes, or improvements. Contributions are welcome!
