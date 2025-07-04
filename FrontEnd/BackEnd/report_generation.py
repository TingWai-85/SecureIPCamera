from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit
import os


#Being imported to be used in front end as well (start)========================================================================================================================================================

# Function to add the title on each new page
def draw_title(canva_object, height):
    canva_object.setFont("Times-Bold", 25)
    canva_object.setFillColor(colors.darkblue)
    canva_object.drawString(50, height - 50, "IP Camera Security Report")

# Function to add text with wrapping
def draw_text(canva_object, text, x, y, font="Times-Roman", font_size=14, color=colors.black, max_width=400):
    canva_object.setFont(font, font_size)
    canva_object.setFillColor(color)
    lines = simpleSplit(text, font, font_size, max_width)
    for line in lines:
        canva_object.drawString(x, y, line)
        y -= 14
    return y

# Function to check and create a new page if needed
def check_page_break(canva_object, height, y_position, min_space=100):
    """ Ensures enough space is available before printing. Creates a new page if needed. """
    if y_position < min_space:
        canva_object.showPage()
        draw_title(canva_object, height)
        return height - 100  # Reset Y position after new page
    return y_position

# Function to start a new page when switching cameras
def new_camera_page(canva_object, height):
    """ Forces a new page when switching to another camera. """
    canva_object.showPage()
    draw_title(canva_object, height)
    return height - 100  # Reset y position

def report_main(name, camera_dict):
    
    # Ensure the directory exists
    report_directory = "Report" # define a directory (or aka folder) name
    os.makedirs(report_directory, exist_ok=True) # If the directory (or folder) does not exist, crete it; else pass

    # Define the report file path
    report_file_path = os.path.join(report_directory, name) # define the specific file to store the report
    # Create PDF file
    pdf_filename = report_file_path #"IP_Camera_Security_Report.pdf"
    canva_object = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # Draw the first title
    draw_title(canva_object, height)
    y_position = height - 100

    # Iterate through each camera, ensuring page breaks between cameras
    for index, (ip, data) in enumerate(camera_dict.items()):
        # Always start a new page for each camera (except the first one)
        if index > 0:
            y_position = new_camera_page(canva_object,height)

        # Print Camera IP
        y_position -= 30
        canva_object.setFont("Times-Bold", 19)
        canva_object.setFillColor(colors.red)
        canva_object.drawString(80, y_position, f"Camera IP: {ip}")

        #Print Camera Detail (Vendor & Firmware Version)
        y_position -= 30
        canva_object.setFont("Times-Bold", 17)
        canva_object.setFillColor(colors.darkblue)
        canva_object.drawString(100, y_position, "Camera Detail:") 

        y_position -= 18
        try: 
            y_position = draw_text(canva_object, f"Vendor: {data['detail']['vendor']}", 120, y_position, font_size=12, color=colors.black)
            y_position = draw_text(canva_object, f"Firmware Version: {data['detail']['firmware version']}", 120, y_position, font_size=12, color=colors.black)
        except:
            y_position = draw_text(canva_object, f"Vendor: Unknown", 120, y_position, font_size=12, color=colors.black)
            y_position = draw_text(canva_object, f"Firmware Version: Unknown", 120, y_position, font_size=12, color=colors.black)

        # Camera Services - Structured Format
        y_position -= 30
        canva_object.setFont("Times-Bold", 17)
        canva_object.setFillColor(colors.darkblue)
        canva_object.drawString(100, y_position, "Services:")

        for service in data['services']:
            y_position = check_page_break(canva_object, height, y_position, 150)  # Ensure space before adding services
            y_position -= 18

            y_position = draw_text(canva_object, f"Port: {service['port']}", 120, y_position, font_size=12, color=colors.black)
            y_position = draw_text(canva_object, f"Service: {service['service']}", 120, y_position - 2, font_size=12, color=colors.black)
            y_position = draw_text(canva_object, f"Product: {service['product']}", 120, y_position - 2, font_size=12, color=colors.black)
            y_position = draw_text(canva_object, f"Version: {service['version'] or 'Unknown'}", 120, y_position - 2, font_size=12, color=colors.black)

            y_position -= 15  # Add spacing between services

        # Print Vulnerabilities Section (Only if there are any vulnerabilities)
        if data['vulnerabilities']:
            y_position -= 20
            canva_object.setFont("Times-Bold", 17)
            canva_object.setFillColor(colors.darkred)
            canva_object.drawString(100, y_position, "Vulnerabilities Found:")

            for vuln in data['vulnerabilities']:
                y_position = check_page_break(canva_object, height, y_position, 150)  # Ensure space before adding vulnerabilities
                y_position -= 20
                canva_object.setFont("Times-Bold", 15)
                canva_object.setFillColor(colors.darkgreen)
                canva_object.drawString(120, y_position, f"- {vuln[0]}")

                y_position = draw_text(canva_object, vuln[1], 140, y_position - 15, font_size=12, color=colors.black)

                y_position -= 15
                canva_object.setFont("Times-Bold", 15)
                canva_object.setFillColor(colors.magenta)
                canva_object.drawString(140, y_position, "Mitigation:")

                y_position -= 15
                if '|' in vuln[2]:
                    num = 1
                    vuln_list = vuln[2].split('|')
                    for text in vuln_list:
                        y_position = draw_text(canva_object, f"{num}. {text}", 160, y_position - 2, font_size=12, color=colors.black)
                        num +=1
                else:
                    y_position = draw_text(canva_object, vuln[2], 160, y_position - 2, font_size=12, color=colors.black)

        y_position -= 30  # Add spacing before the next camera

    # Save PDF
    canva_object.save()
    return f"✅ Report saved as {pdf_filename}"

#Being imported to be used in front end as well (end)========================================================================================================================================================


if __name__ == "__main__":

    testing_camera = {
    '192.168.1.100': {
        'services': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}],
        'detail': {'vendor': "Hikvision", "firmware version": "2.1"},
        'vulnerabilities': [
            ['CVE-2008-0225', 'Heap-based buffer overflow in xine-lib 1.1.9.', 'Mitigation not found'],
            ['Open RTSP Stream Without Authentication', 'RTSP is accessible without login.', 'Enable authentication. | Restrict access.']
        ]
    },
    '192.168.1.101': {
        'services': [{'port': 554, 'service': 'rtsp', 'product': 'Hikvision Camera', 'version': '5.5.0'}],
        'detail': {'vendor': "Dahua", "firmware version": "Unknown"},
        'vulnerabilities': []
    },
    '192.168.1.102': {
        'services': [{'port': 8080, 'service': 'http', 'product': 'Dahua Web Service', 'version': '3.2.1'}],
        'vulnerabilities': [
            ['Weak or No Encryption', 'Video feed is transmitted without encryption.', 'Enable encryption. | Use VPN.']
        ]
    },
    '192.168.1.254': {
        'services': [
            {'port': 80, 'service': 'http', 'product': 'TP-LINK TD-W8968 http admin', 'version': ''},
            {'port': 443, 'service': 'http', 'product': 'TP-LINK TD-W8968 http admin', 'version': ''}
        ],
        'vulnerabilities': [
            ['CVE-2008-0225', 'Heap-based buffer overflow in xine-lib 1.1.9.', 'Mitigation not found'],
            ['Open RTSP Stream Without Authentication', 'RTSP is accessible without login.', 'Enable authentication. | Restrict access.'],
            ['Weak or No Encryption for Video Streams', 'Video feed is transmitted without encryption.', 'Enable encryption. | Use VPN.']
        ]
    }
    }

    #testing_camera = {'192.168.212.37': {'services': [{'port': 8554, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}, {'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}], 'detail': {'vendor': 'Dahua', 'firmware version': '123'}, 'vulnerabilities': [['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.', 'Refer to the vendor and update to the latest patch.'], ['CVE-2008-0225', 'Heap-based buffer overflow in the rmff_dump_cont function in input/libreal/rmff.c in xine-lib 1.1.9 and earlier allows remote attackers to execute arbitrary code via the SDP Abstract attribute in an RTSP session, related to the rmff_dump_header function and related to disregarding the max field.  NOTE: some of these details are obtained from third party information.', 'Refer to the vendor and update to the latest patch.']]}, '192.168.212.177': {'services': [{'port': 8555, 'service': 'rtsp', 'product': 'VLC rtspd', 'version': '1.1.9'}], 'vulnerabilities': []}}

    print(report_main("IP_Camera_Security_Report.pdf",testing_camera))