# Simple Port Scanner

[![License: Educational](https://img.shields.io/badge/License-Educational%20Only-yellow.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

A lightweight, multi-threaded port scanner written in Python for educational purposes. This tool helps cybersecurity students understand TCP/IP concepts, socket programming, and how network scanning tools like `nmap` work under the hood.

> **⚠️ ETHICAL DISCLAIMER:** This tool is intended for **educational purposes only**. Only scan systems you own or have explicit written permission to test. Unauthorized port scanning may violate laws and regulations in your jurisdiction. The author assumes no liability for misuse of this software.

##Features

- ✅ Multi-threaded scanning for improved performance
- ✅ Support for hostname resolution
- ✅ Configurable port ranges (1-65535)
- ✅ Adjustable timeout settings
- ✅ Color-coded terminal output (Windows/Linux/macOS)
- ✅ Common service name identification
- ✅ Results export to text file
- ✅ Keyboard interrupt handling (Ctrl+C)


- Understanding TCP handshake and socket connections
- Learning about common port numbers and associated services
- Practicing Python threading and network programming
- Developing responsible disclosure and ethical testing habits
- Building foundational skills for network security roles


### Prerequisites

- **Python 3.6** or higher installed on your system
- No external packages required (uses only Python standard library)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/nyam0si/port-scanner.git
cd port-scanner
