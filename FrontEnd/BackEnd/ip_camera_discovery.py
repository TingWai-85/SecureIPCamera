#built-in library
import socket
import psutil # type: ignore
import nmap

# Self-created libraries
try:
    from .general_function import choice  # Relative import for package
    from .general_function import validate_ip
except ImportError:
    import sys
    from os.path import dirname, abspath
    sys.path.append(dirname(abspath(__file__)))
    from general_function import choice  # Absolute import fallback
    from general_function import validate_ip

#Being imported to be used in front end as well (start)========================================================================================================================================================

def get_network_detail():
    wireless_adapter_names = ['wlan0', 'Wi-Fi', 'wlp']  # Common wireless adapter names
    all_interface = psutil.net_if_addrs() #this will give us all the network interface detail in dictionary


    # Iterate through network interfaces
    for interface, addrs in all_interface.items(): #loop through all_interface dictionary in tuple format
        # Check if the interface is a wireless adapter
        for name in wireless_adapter_names:
            if name in interface:
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # check for IPv4 address
                        ip_address = addr.address
                        hostname = interface
                        subnet = ".".join(ip_address.split(".")[:-1])
                        network_detail = [hostname,ip_address,subnet]
                        return network_detail
    
    return "Wireless adapter not found or not connected."

def subnet_calculation(subnet,mask):
    if mask == 24:
        return subnet + ".0/24"
    elif mask == 16:
        return ".".join(subnet.split(".")[:2]) + ".0.0/16"
    elif mask == 8:
        return subnet.split(".")[0] + ".0.0.0/8"
    else:
        return "Unsupported subnet mask. Use 8, 16, or 24."

def scan_for_cameras(ip_range):
    # Initialize the Nmap scanner
    scanner = nmap.PortScanner()

    # Scan for commonly used IP camera ports
    print(f"Scanning IP range: {ip_range} for IP cameras...")
    scanner.scan(hosts=ip_range, arguments='-p 80,443,554,8000-9000 --open -sV')
    
    # Disctonary to store detected cameras
    ip_cameras = {}
    print(scanner.all_hosts())
    # Loop through scanned hosts
    for host in scanner.all_hosts():
        print(f"\nHost: {host} - Status: {scanner[host].state()}")  #scanner[host] return a dictionary
        if 'tcp' in scanner[host]:  # Check for open ports
            for port in scanner[host]['tcp']:                   #there are multiple inner dictionary inside this 'tcp' values
                service = scanner[host]['tcp'][port].get('name', 'unknown')
                product = scanner[host]['tcp'][port].get('product', '')
                version = scanner[host]['tcp'][port].get('version', '')

                # Basic filter for camera-related services
                if service in ['http', 'https', 'rtsp'] or 'camera' in product.lower():
                    print(f"  Port: {port}, Service: {service}, Product: {product} {version}")
                    if host not in ip_cameras:
                        ip_cameras[host] = {}  #for this first attempt, create a new key 'host' and the value is a list
                        ip_cameras[host]['services'] = []
                    ip_cameras[host]['services'].append({ #save the detected host inside the list in a form of dictionary format
                        'port': port,
                        'service': service,
                        'product': product,
                        'version': version
                    })
    if ip_cameras:
        print("\nDetected IP Cameras:")
        for ip, data in ip_cameras.items():
            print(f"- IP: {ip}")
            for definition, service in data.items():
                if definition == 'services':
                    for detail in service:
                        print(f"  Port: {detail['port']}, Service: {detail['service']}, Device: {detail['product']} {detail['version']}")
    else:
        print("\nNo IP cameras found in the specified range.")
    
    return ip_cameras

#Being imported to be used in front end as well (end)========================================================================================================================================================

#for use only in running the application in command line based (start)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def network_range_confirmation():
    network_detail = get_network_detail()
    hostname = network_detail[0]
    local_ip = network_detail[1]
    default_subnet = network_detail[2]
    
    # Display basic details
    print(f"Detected Hostname: {hostname}")
    print(f"Detected Wireless IP: {local_ip}")
    print(f"Detected Default Subnet Base: {default_subnet}.x")
    
    # Ask for a subnet mask

    print("\nOptional Subnet Mask Options:")
    print("[1] Use Default Mask (/24)\n[2] Specify Custom Mask\n[3] Specify a Specific IP Address")
    print("Enter your choice (1 , 2 or 3): ")
    choosen = choice(3)
    
    if choosen == "1":
        mask = 24  # Default
        subnet = subnet_calculation(default_subnet, mask)
        print(f"\nCalculated Subnet: {subnet}")
    elif choosen == "2":
        print("[1] (/24)\n[2] (/16)\n[3] (/8)")
        print("Enter your desired CIDR subnet mask (1 , 2 or 3): ")
        s_mask = choice(3)

        if s_mask == '1':
            mask = 24
        elif s_mask == '2':
            mask = 16
        else:
            mask = 8
        
        subnet = subnet_calculation(default_subnet, mask)
        print(f"\nCalculated Subnet: {subnet}")
    else:
        ip_op = True
        while ip_op:
            ip = input("\nPlease enter a valid IP address: ")
            if validate_ip(ip):
                print(f"\nThe IP address '{ip}' is valid!")
                ip_op = False
                break
            else:
                print("\nInvalid IP address format. Please try again.")
                continue
        subnet = ip + "/32"

    return subnet
    
def ip_camera_discovering_main():
    subnet = network_range_confirmation() #return a string
    ip_cam = scan_for_cameras(subnet)      #return a dictionary

    return ip_cam

#for use only in running the application in command line based (end)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    camera = ip_camera_discovering_main()
   #print(camera)
   #{'192.168.212.37': {'services': [{'port': 8554, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}, {'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}]}}