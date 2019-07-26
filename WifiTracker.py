# ----------------------------------
# Imports section
# ----------------------------------
import requests
import json
import telegram
import time
# ----------------------------------

# ----------------------------------
# Global Static Variables
# ----------------------------------

# User credentials
# DNI/Passport for the user
identifier = "11111111A"
isPassport = "false"
password = "some_secure_pass"

# Telegram chat_id and token
chat_id = "111111111"
bot_token = "111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

# Connection settings
protocol = "https://"
server = "smartwifi.niji.mobi"
content_type = "application/json; charset=UTF-8"
user_agent = "okhttp/3.11.0"
# Previous devices filename json
previous_filename = "previous.json"
# Log filename
log_devices_filename = "devices.log"
log_application_filename = "application.log"

# Start telegram bot
bot = telegram.Bot(token=bot_token)
# ----------------------------------

# ----------------------------------
# Get token if auth is succesful
# ----------------------------------
def get_token_login():

    # Data and headers for the request
    url = "/api/2.4.0/identity/login"
    headers = {"Content-Type":content_type,"User-Agent":user_agent}
    data = '{"identifier":"%s","isPassport":"%s","password":"%s"}' % (identifier,isPassport,password)
    # Token JWT
    token = ""

    try:
        r = requests.post(protocol + server + url, data = data, headers = headers)
        token = r.json()
        token = token['data']['token']

    except requests.RequestException as e:
        pass

    return token
# ----------------------------------

# ----------------------------------
# Get client line number
# ----------------------------------
def get_client_data_line(token):

    if token is not "":

        # Data and headers for the request
        url = "/api/2.4.0/identity/client/data"
        headers = {'Content-Type':content_type, 'x-niji-token':token,'User-Agent':user_agent}

        try:
            r = requests.get(protocol + server + url, headers=headers)
            line = r.json()
            line = line['data']['lines'][0]['mainNumber']

        except requests.RequestException as e:
            pass

    return line
# ----------------------------------

# ----------------------------------
# Get connected devices
# ----------------------------------
def get_connected_device_list(token, line):

    # Variable to store the deviceMap
    devices_list = ""
    connected_devices_list = []

    if token is not "" and line is not "":

        # Data and headers for the request
        url = "/api/2.4.0/routing/router/" + line + "/deviceMap"
        headers = {'Content-Type':content_type, 'x-niji-token':token,'User-Agent':user_agent}

        try:
            r = requests.get(protocol + server + url, headers=headers)
            devices_list = r.json()
            devices_list = devices_list['data']['device_list']
            for value in devices_list:
                # Assume that if rssi_dbm has some value is because the device is connected
                if value['rssi_dbm']:
                    connected_devices_list.append(
                        {
                            'display_name':value['display_name'],
                            'host_name':value['host_name'],
                            'mac_addr':value['mac_addr'],
                        }
                    )

        except Exception as e:

            try:
                log_file = open(log_application_filename,"a")
                log_file.write("[" + time.asctime(time.localtime(time.time())) + "] Token not valid" +'\n')
                log_file.writable("[" + time.asctime(time.localtime(time.time())) + "] Getting auth token" +'\n')
                log_file.close()

            except IOError:
                pass

            token = get_token_login()
            line = get_client_data_line(token)
            get_connected_device_list(token, line)

    return connected_devices_list
# ----------------------------------

# ----------------------------------
# Check Differences between devices connected readed from API and stored in the json file
# ----------------------------------
def check_diff(current_connected_devices):

    previous_connected_devices = ""
    list_to_notify = []

    # Sometimes the API call return empty values. Only check if there is some data to compare
    if len(current_connected_devices) != 0:

        try:
            previous_file = open(previous_filename,"r")
            previous_connected_devices = json.load(previous_file)
            previous_file.close()

            for value in previous_connected_devices:
                if value not in current_connected_devices:
                    list_to_notify.append(
                        {
                            'display_name':value['display_name'],
                            'host_name':value['host_name'],
                            'mac_addr':value['mac_addr'],
                            'action':'disconnected',
                            'time':time.asctime(time.localtime(time.time()))
                        }
                    )

            for value in current_connected_devices:
                if value not in previous_connected_devices:
                    list_to_notify.append(
                        {
                            'display_name':value['display_name'],
                            'host_name':value['host_name'],
                            'mac_addr':value['mac_addr'],
                            'action':'connected',
                            'time':time.asctime(time.localtime(time.time()))
                        }
                    )

        except IOError:
            for value in current_connected_devices:
                list_to_notify.append(
                    {
                        'display_name':value['display_name'],
                        'host_name':value['host_name'],
                        'mac_addr':value['mac_addr'],
                        'action':'new device',
                        'time':time.asctime(time.localtime(time.time()))
                    }
                )

    # Only write file and send notifications if there is any changes
    for value in list_to_notify:

        try:
            previous_file = open(previous_filename,"w")
            json.dump(current_connected_devices, previous_file)
            previous_file.close()

        except IOError:
            pass

        send_notifications(value)

# ----------------------------------

# ----------------------------------
# Send notification
# ----------------------------------
def send_notifications(device):
    # Send Telegram notification
    bot.send_message(chat_id=chat_id, text=str(device))

    # Save entry to log file
    try:
        try:
            log_file = open(log_application_filename,"a")
            log_file.write("[" + time.asctime(time.localtime(time.time())) + "] Saving entries to log file" +'\n')
            log_file.close()

        except IOError:
            pass

        log_file = open(log_devices_filename,"a")
        #json.dump(device,log_file)
        # Remove first and last char -> '{' and '}'
        log_file.write(str(device)[1:-1]+'\n')
        log_file.close()

    except IOError:
        pass

# ----------------------------------

# ----------------------------------
# Main function
# ----------------------------------
def main():

    # Get telegram chat id
    # bot = telegram.Bot(token=bot_token)
    # updates = bot.get_updates()
    # print([u.message.chat_id for u in updates])

    print("Starting app...")

    try:
        log_file = open(log_application_filename,"a")
        log_file.write("[" + time.asctime(time.localtime(time.time())) + "] Starting app" +'\n')
        log_file.write("[" + time.asctime(time.localtime(time.time())) + "] Getting auth token" +'\n')
        log_file.close()

    except IOError:
        pass

    token = get_token_login()

    try:
        log_file = open(log_application_filename,"a")
        log_file.write("[" + time.asctime(time.localtime(time.time())) + "] Getting client data line" +'\n')
        log_file.close()

    except IOError:
        pass

    line = get_client_data_line(token)

    print("Running app...")

    while True:
        connected_devices_list = get_connected_device_list(token, line)
        check_diff(connected_devices_list)
        time.sleep(60)

main()
