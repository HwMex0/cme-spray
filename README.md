# CME-Spray

## Overview
This script automates the process of password spraying against a list of IP addresses using CrackMapExec. It is designed to test multiple services like SMB, SSH, WinRM, MSSQL, and LDAP with the option to control output verbosity and leverage threading for efficiency.

## Features
- Supports multiple services (SMB, SSH, WinRM, MSSQL, LDAP).
- Option to print only successful login attempts.
- Threading support for faster execution.
- Colored output for better readability.

## Prerequisites
- Python 3.6 or higher.
- CrackMapExec installed and accessible in the system's PATH.

## Installation

1. Clone the repository or download the script:
``` git clone https://github.com/HwMex0/cme-spray.git```

2. Install the required Python packages:
``` pip install -r requirements.txt ```

## Usage

Run the script with the necessary arguments:
``` python3 cme-spray.py --ips <IPs file or IP> --users <users file or user> --passwords <passwords file or password> [--services smb ssh winrm mssql ldap] [--print-success] [--threads <number>] ```

### Arguments
- `--ips`: Path to the file containing IP addresses or a single IP address.
- `--users`: Path to the file containing usernames or a single username.
- `--passwords`: Path to the file containing passwords or a single password.
- `--services`: (Optional) List of services to spray. Default is all supported services (smb, ssh, winrm, mssql, ldap).
- `--print-success`: (Optional) Flag to print only successful connections.
- `--threads`: (Optional) Number of threads to use for password spraying. Default is 10.

## Disclaimer
This tool is intended for security research and penetration testing activities. Use it responsibly and always with permission from the target network owner.
