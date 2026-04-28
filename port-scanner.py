#!/usr/bin/env python3
"""
Simple Port Scanner
A lightweight Python tool for scanning open ports on a target host.
For educational purposes only.
"""

import socket
import sys
import threading
import time
from datetime import datetime

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def scan_port(target, port, timeout=1):
    """
    Scan a single port on the target host.
    
    Args:
        target (str): IP address or hostname
        port (int): Port number to scan
        timeout (int): Connection timeout in seconds
    
    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Attempt to connect
        result = sock.connect_ex((target, port))
        
        # Close the socket
        sock.close()
        
        # connect_ex returns 0 on success
        return result == 0
        
    except socket.gaierror:
        print(f"{RED}[!] Hostname could not be resolved{RESET}")
        sys.exit(1)
    except socket.error:
        return False

def scan_ports(target, start_port, end_port, max_threads=100):
    """
    Scan a range of ports using threading for efficiency.
    
    Args:
        target (str): IP address or hostname
        start_port (int): Starting port number
        end_port (int): Ending port number
        max_threads (int): Maximum number of concurrent threads
    """
    open_ports = []
    threads = []
    
    print(f"{BLUE}[*] Starting scan on {target}{RESET}")
    print(f"{BLUE}[*] Scanning ports {start_port}-{end_port}{RESET}")
    print(f"{BLUE}[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print("-" * 50)
    
    # Create and start threads
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_and_record, args=(target, port, open_ports))
        threads.append(thread)
        thread.start()
        
        # Limit concurrent threads
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
    
    # Wait for remaining threads
    for thread in threads:
        thread.join()
    
    # Display results
    print("-" * 50)
    print(f"{YELLOW}[+] Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{GREEN}[+] Open ports found: {len(open_ports)}{RESET}")
    
    if open_ports:
        print(f"\n{GREEN}Open Ports:{RESET}")
        for port in sorted(open_ports):
            service = get_service_name(port)
            print(f"  {GREEN}{port}/tcp{RESET} - {service}")
    else:
        print(f"{RED}[!] No open ports found in the specified range.{RESET}")
    
    return open_ports

def scan_and_record(target, port, open_ports_list):
    """Helper function for threading to record open ports"""
    if scan_port(target, port):
        open_ports_list.append(port)
        service = get_service_name(port)
        print(f"  {GREEN}[+] Port {port}/tcp is OPEN - {service}{RESET}")

def get_service_name(port):
    """
    Return common service name for a given port number.
    
    Args:
        port (int): Port number
    
    Returns:
        str: Service name or 'Unknown'
    """
    common_ports = {
        20: "FTP (Data)",
        21: "FTP (Control)",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        111: "RPC",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
    }
    return common_ports.get(port, "Unknown")

def validate_ip(ip):
    """Basic IP address validation"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or int(part) < 0 or int(part) > 255:
            return False
    return True

def main():
    """Main function to handle user input and orchestrate the scan"""
    
    # Display banner
    print(f"""
    {BLUE}╔══════════════════════════════════════════╗
    ║      Simple Port Scanner v1.0             ║
    ║      Educational Use Only                  ║
    ╚══════════════════════════════════════════╝{RESET}
    """)
    
    # Get target
    target = input(f"{YELLOW}[?] Enter target IP or hostname: {RESET}").strip()
    
    # Resolve hostname if needed
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{GREEN}[+] Resolved {target} to {target_ip}{RESET}")
    except socket.gaierror:
        print(f"{RED}[!] Could not resolve hostname. Exiting.{RESET}")
        sys.exit(1)
    
    # Get port range
    try:
        start_port = int(input(f"{YELLOW}[?] Enter starting port (1-65535): {RESET}").strip())
        end_port = int(input(f"{YELLOW}[?] Enter ending port (1-65535): {RESET}").strip())
        
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            print(f"{RED}[!] Invalid port range. Exiting.{RESET}")
            sys.exit(1)
    except ValueError:
        print(f"{RED}[!] Invalid input. Please enter numbers. Exiting.{RESET}")
        sys.exit(1)
    
    # Get timeout
    try:
        timeout_input = input(f"{YELLOW}[?] Enter timeout in seconds (default 1): {RESET}").strip()
        timeout = float(timeout_input) if timeout_input else 1.0
    except ValueError:
        timeout = 1.0
    
    # Update global timeout for scan_port function
    global SCAN_TIMEOUT
    SCAN_TIMEOUT = timeout
    
    # Confirm with user
    print(f"\n{BLUE}[*] Target: {target_ip}{RESET}")
    print(f"{BLUE}[*] Port Range: {start_port}-{end_port}{RESET}")
    print(f"{BLUE}[*] Timeout: {timeout} seconds{RESET}")
    
    confirm = input(f"\n{YELLOW}[?] Start scan? (y/n): {RESET}").strip().lower()
    if confirm != 'y':
        print(f"{RED}[!] Scan cancelled.{RESET}")
        sys.exit(0)
    
    # Perform the scan
    try:
        open_ports = scan_ports(target_ip, start_port, end_port)
        
        # Save results if any open ports found
        if open_ports:
            save = input(f"\n{YELLOW}[?] Save results to file? (y/n): {RESET}").strip().lower()
            if save == 'y':
                filename = f"scan_results_{target_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Port Scan Results for {target_ip}\n")
                    f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Port Range: {start_port}-{end_port}\n")
                    f.write("-" * 50 + "\n")
                    for port in sorted(open_ports):
                        service = get_service_name(port)
                        f.write(f"Port {port}/tcp - {service}\n")
                print(f"{GREEN}[+] Results saved to {filename}{RESET}")
    
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Scan interrupted by user. Exiting.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[!] An error occurred: {e}{RESET}")
        sys.exit(1)

# Allow timeout to be modified globally
SCAN_TIMEOUT = 1.0

# Override scan_port to use the global timeout
def scan_port(target, port, timeout=None):
    """Scan a single port with configurable timeout"""
    timeout = timeout or SCAN_TIMEOUT
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except:
        return False

# Re-bind the function
import types
scan_port.__code__ = types.FunctionType(
    scan_port.__code__,
    globals(),
    'scan_port',
    argdefs=(None,)
)

if __name__ == "__main__":
    main()
