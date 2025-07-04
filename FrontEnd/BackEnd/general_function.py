import re

#Being imported to be used in front end as well (start)========================================================================================================================================================
def validate_ip(ip):
    # Regular expression for validating an IPv4 address
    ip_regex = re.compile(
        r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    return bool(ip_regex.match(ip)) #Converts the match result into True or False
#Being imported to be used in front end as well (end)========================================================================================================================================================


#for use only in running the application in command line based (start)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def choice(number_of_choices):
    choices = []
    for i in range(1,number_of_choices+1):
        choices.append(str(i))

    operation = True
    while operation:
        choosing = input().strip()
        if choosing in choices:
            operation = False
            break
        else:
            print("Sorry, your choice is out of range.")
            print(f"Please select your choice again within {choices}\n")
            continue
    
    return choosing
#for use only in running the application in command line based (end)----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    ip = "255.255.255.255"
    validate_ip(ip)
    if validate_ip(ip):
        print(f"The IP address '{ip}' is valid!")
    else:
        print("Invalid IP address format. Please try again.")

