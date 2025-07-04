import scapy.all as scapy # type: ignore
import joblib
import pandas as pd
from scapy.layers.inet import IP, TCP # type: ignore
from scapy.sendrecv import sniff # type: ignore
from datetime import datetime
import os
from contextlib import redirect_stdout
# Suppress the pygame welcome message
with open(os.devnull, "w") as f, redirect_stdout(f): # once import pygame module, there is an welcoming message being output by default.
                                                     # Here is to avoid this welcoming message keep coming out 
    import pygame # type: ignore


#Being imported to be used in front end as well (start)========================================================================================================================================================

def extract_features(packet, ip_categories, reverse_ip_categories):
    """Extracts relevant network traffic features"""
    if packet.haslayer(IP) and packet.haslayer(TCP): # check the packet is having IP layer and TCP layer
        # extract the necessary information
        dst_ip = packet[IP].dst # destination IP address
        dst_port = packet[TCP].dport # destination port
        packet_size = len(packet) # get the length of the packet in bytes to represent its size
        syn_flag = int(packet[TCP].flags & 0x02 != 0) # Get the TCP flags field and check if the SYN flag is not zero, then convert the Boolean into integer
                                                        # (0x02 or 00000010 corresponds to the SYN flag)
        ack_flag = int(packet[TCP].flags & 0x10 != 0) # Get the TCP flags field and check if the ACK flag is not zero, then convert the Boolean into integer
                                                        # (0x10 or 00010000 corresponds to the ACK flag)

        # Convert IP to numerical category
        dst_ip_numeric = get_ip_numeric(dst_ip, ip_categories, reverse_ip_categories)

        # Create DataFrame
        df = pd.DataFrame([[dst_ip_numeric, dst_port, packet_size, syn_flag, ack_flag]],
                        columns=["dst_ip", "dst_port", "packet_size", "syn_flag", "ack_flag"])
        return df
    return None

def log_attack(ip, port):
    """Log attack details to a file."""
    # Ensure the directory exists
    log_directory = "ids_log" # define a directory (or aka folder) name
    os.makedirs(log_directory, exist_ok=True) # If the directory (or folder) does not exist, crete it; else pass

    # Define the log file path
    log_file_path = os.path.join(log_directory, "network_alerts.log") # define the specific file to store the log

    # Append log details to the file
    with open(log_file_path, "a") as log_file: # "a" --> append mode, which add new line to the log file without overwrite the entire file
        log_file.write(f"[{datetime.now()}] ALERT: Potential DoS attack detected on {ip}:{port}\n")
    print("📜 Alert logged.")


def play_alert_sound(sound_file):
    """Play a sound alert using pygame."""
    try:
        pygame.mixer.init() # initialize the pygame.mixer module, it is used to handle playing the audio
        pygame.mixer.music.load(sound_file)  # load the sound track
        pygame.mixer.music.set_volume(1.0) # the volume value is between 0.0 - 1.0, set the volumn to 1.0 (100%)
        pygame.mixer.music.play() # play the sound track

        while pygame.mixer.music.get_busy():  # Checks if the pygame is still playing the music (return true if yes, else return false)
            pygame.time.Clock().tick(10) # it fix each second can only run maximum 10 while loop iterations
                                            # mainly to prevent the while loop consume too many resources while the sound track is being played
    except Exception as e:
        print(f"❌ Failed to play alert sound: {e}")

#Being imported to be used in front end as well (end)========================================================================================================================================================



#for use only in running the application in command line based (start)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_ip_numeric(ip, ip_categories, reverse_ip_categories):
    # do the same thing as the initial mapping above
    # having this function is to repeatly convert new ip into numeric value in future
    # For example result:
    # ip_categories = {'192.168.1.111' : 1, '192.168.1.100' : 2}
    # reverse_ip_categories = {1: '192.168.1.111', 2: '192.168.1.100'}

    """Convert IP to a categorical numerical value"""
    if ip not in ip_categories:
        category = len(ip_categories)
        ip_categories[ip] = category
        reverse_ip_categories[category] = ip
    return ip_categories[ip]

def ids_main(camera, ai_model):
        
    # Load trained AI model
    model = joblib.load(ai_model)

    # Extracting IP and ports into a list of tuples
    ip_camera_list = []
    for ip, data in camera.items(): #iterate iver the camera dictionary
        services = data.get("services",[]) #get the list of dictionary storing camera services
        for service in services: #iterate over the list (each service is a dictionary)
            ip_camera_list.append((ip, service['port']))

    # Track unique IPs for encoding
    ip_categories = {}  # Forward mapping: IP -> Categorical
    reverse_ip_categories = {}  # Reverse mapping: Categorical -> IP

    # Initialize mappings
    # Convert the categorical data ip into numeric value
    # For example result:
    # ip_categories = {'192.168.1.111' : 1, '192.168.1.100' : 2}
    # reverse_ip_categories = {1: '192.168.1.111', 2: '192.168.1.100'}
    for ip in camera.keys():
        if ip not in ip_categories:
            category = len(ip_categories)
            ip_categories[ip] = category
            reverse_ip_categories[category] = ip


    def detect_attack(packet): # packet here is the network packet provided or captured by the sniff function
        """Processes incoming packets and detects potential attacks"""
        features = extract_features(packet, ip_categories, reverse_ip_categories)
        if features is not None: # check if the dataframe (features) is valid or not
            prediction = model.predict(features)[0] # use the pre-trained model to predict if the packet is a normal traffic or malicious traffic
            real_ip = reverse_ip_categories[features.iloc[0]["dst_ip"]]  # Get the real IP from reverse mapping
            if prediction == 1:  # Attack detected if the result is 1
                print(f"⚠️ ALERT! Potential DoS attack detected on IP Camera {real_ip}:{features.iloc[0]['dst_port']}!")
                log_attack(real_ip, features.iloc[0]['dst_port'])

                #for testing this script in backend folder
                current_directory = os.getcwd()
                play_alert_sound(os.path.join(current_directory, "materials", "siren-alert-96052.wav"))
            else: # else, the result will show 0
                print(f"✅ Normal Traffic to IP Camera {real_ip}:{features.iloc[0]['dst_port']}")


    iface = scapy.conf.iface # this is to get the default network interface the scapy will use to capture the network traffic
    print(f"Sniffing on interface: {iface}") # print the interface (for later if want to add function to allow user to select the inerface
                                             # if they dont wish to use the default one)

    # Generate a BPF (Berkeley Packet Filter) filter to monitor all specified IPs and ports

    # for prior knowledge, for example: ip_camera_list = [('192.168.1.100', 8555), ('192.168.1.111', 8554)]
    filter_parts = []
    for ip, port in ip_camera_list: # iterate over the list and access two each elements in the tuple
        filter_condition = f"(dst host {ip} and dst port {port})"
        filter_parts.append(filter_condition) # this create the list, for example:
                                              # filter_parts = ["(dst host 192.168.1.100 and dst port 8555)", "(dst host 192.168.1.111 and dst port 8554)"]

    filter_conditions = " or ".join(filter_parts) # join the filter_parts list into one single sentence for BPF filter using 'or' keywords
                                                  # for example: filter_conditions =
                                                  # "(dst host 192.168.1.100 and dst port 8555) or (dst host 192.168.1.111 and dst port 8554)"
    
    print(f"🛡 Monitoring cameras on: {ip_camera_list}")

    # Sniff packets related only to the IP camera, callback detect_attack function
    # Each packet is captured and then passed to the detect_attack function for analysis
    sniff(filter=filter_conditions, prn=detect_attack, store=0)

#for use only in running the application in command line based (end)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    #for testing this script in backend folder
    # Dictionary storing multiple IP camera details
    testing_camera = {
        '192.168.1.100': {
            'services': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}],
        },
        '192.168.161.13': {
            'services': [{'port': 8554, 'service': 'rtsp', 'product': 'Hikvision Camera', 'version': '5.5.0'},
                        {'port': 8556, 'service': 'rtsp', 'product': 'Hikvision Camera', 'version': '5.5.0'}],
        }
    }
    current_directory = os.getcwd()
    ai_model_path = os.path.join(current_directory, "materials", "ai_model", "ids_model_v2.pkl")
    ids_main(testing_camera, ai_model_path)