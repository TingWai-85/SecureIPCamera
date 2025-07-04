#Mitigation Retrieve
import requests
from bs4 import BeautifulSoup # type: ignore
import time

#Being imported to be used in front end as well (start)========================================================================================================================================================

def check_if_have_vuls(camera_dict):
    selected_ip = []
    for ip, data in camera_dict.items():
        try:
            if data['vulnerabilities']:
                selected_ip.append(ip)
        except:
            data['vulnerabilities'] = []
    return selected_ip,camera_dict


def mitigation_retrieve(vulns_list):

    for vulnerabilities in vulns_list:
        if vulnerabilities[0][0:3] == "CVE":
            try:
                cve_id = vulnerabilities[0]
                year = cve_id.split('-')[1]  # Extract the year
                url = f"https://www.clouddefense.ai/cve/{year}/{cve_id}"

                # Request the webpage
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code != 200:
                    print(f"Failed to fetch {cve_id}")
                    vulnerabilities.append("Mitigation Request Fail. This can be due to your unstable network connection.")
                    continue

                # Parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                mitigation_text = "Refer to the vendor and update to the latest patch."  # Default text

                # Find the <h3> tag that contains "Immediate Steps to Take"
                h3_tag = soup.find("h3", string=lambda t: t and "Immediate Steps to Take" in t)

                if h3_tag:
                    # Check the first sibling element after <h3>
                    next_elem = h3_tag.find_next_sibling()
                    if next_elem:
                        # If it's a <ul>, extract all text from the list
                        if next_elem.name == "ul":
                            mitigation_text = next_elem.get_text(separator=" | ", strip=True)
                        
                        # If it's a <p>, extract its text
                        elif next_elem.name == "p":
                            mitigation_text = next_elem.get_text(strip=True)

                vulnerabilities.append(mitigation_text)
                print(f"Scraped mitigation for {cve_id}: {mitigation_text}")

                time.sleep(2)  # Delay to avoid being blocked

            except Exception as e:
                print(f"Error processing {cve_id}: {e}")
                vulnerabilities.append("Error")
        else:
            if vulnerabilities[0] == "Default Credentials Used":
                vulnerabilities.append("Change the default credentials immediately. | Use strong passwords with at least 12 characters (mix of uppercase, lowercase, numbers, special chars). | Implement multi-factor authentication (MFA) if supported.")
            elif vulnerabilities[0] == "Open RTSP Stream Without Authentication":
                vulnerabilities.append("Enable authentication for RTSP. | If not needed, disable RTSP streaming. | Restrict RTSP access to trusted IP addresses only.")
            elif vulnerabilities[0] == "Weak or No Encryption for Video Streams":
                vulnerabilities.append("Enable end-to-end encryption for video streams. | Use secured VPN tunnels for remote access. | If possible, implement AES-256 encryption for streaming.")
            else:
                vulnerabilities.append("Review vendor recommendations and apply appropriate security patches.")
    return vulns_list

def update_mitigation(ip_list,camera_dict):
    
    for ip in ip_list:
        vulns = camera_dict[ip]['vulnerabilities']
        mitigation = mitigation_retrieve(vulns)
        camera_dict[ip]['vulnerabilities'] = mitigation
    
    
    return camera_dict

#Being imported to be used in front end as well (end)========================================================================================================================================================


if __name__ == "__main__":

    testing_camera = {
    '192.168.212.37': {
        'services': [{'port': 8554, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}, {'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}], 
        'vulnerabilities': [
            ['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], 
            ['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], 
            ['Open RTSP Stream Without Authentication', 'The Real-Time Streaming Protocol (RTSP) is publicly accessible without login credentials.'], 
            ['Weak or No Encryption for Video Streams', 'The video feed is transmitted without encryption, allowing attackers to intercept footage.']
            ]
        }, 
    '192.168.212.177': {
        'services': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}],
        'vulnerabilities': [
            ['CVE-2023-30806', 'Heap'],
            ['Weak or No Encryption for Video Streams', 'The video feed is transmitted without encryption, allowing attackers to intercept footage.']
        ]
        }
    }
    #testing_camera = {'192.168.212.37': {'services': [{'port': 8554, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}, {'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}], 'detail': {'vendor': 'Dahua', 'firmware version': '123'}, 'vulnerabilities': [['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], ['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.']]}, '192.168.212.177': {'services': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}]}}

    example_list = [['CVE-2024-0183', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], ['CVE-2019-10958', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], ['Open RTSP Stream Without Authentication', 'The Real-Time Streaming Protocol (RTSP) is publicly accessible without login credentials.'], ['Weak or No Encryption for Video Streams', 'The video feed is transmitted without encryption, allowing attackers to intercept footage.']]
    testing = [['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.'], ['Open RTSP Stream Without Authentication', 'The Real-Time Streaming Protocol (RTSP) is publicly accessible without login credentials.'], ['Weak or No Encryption for Video Streams', 'The video feed is transmitted without encryption, allowing attackers to intercept footage.']]
    testing_camera_m = {'192.168.1.100': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}], '192.168.1.254': [{'port': 80, 'service': 'http', 'product': 'TP-LINK TD-W8968 http admin', 'version': ''}, {'port': 443, 'service': 'http', 'product': 'TP-LINK TD-W8968 http admin', 'version': ''}]}

    
    #vulns_list = mitigation_retrieve(testing)
    #for i in vulns_list:
    #   print(i)
    ip, testing_camera = check_if_have_vuls(testing_camera)
    testing_camera = update_mitigation(ip,testing_camera)

    print(testing_camera)