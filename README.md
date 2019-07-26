# WifiTracker
Example of using and abusing Movistar/O2 SmartWifi API to create an application to track the connections of the devices

## Motivation
Since some months ago I have an O2 fiber connection at home. Attached to this subscription you can use the Movistar SmartWifi app to manage some settings in the provided HGU router. 

[Google Play Movistar SmartWifi App](https://play.google.com/store/apps/details?id=com.movistar.base)
[App Store Movistar SmartWifi App](https://apps.apple.com/us/app/movistar-smart-wifi/id1229740209)

One of the most interesting features is the chance to get a list of the devices connected (WiFi or cabling) in "almost real time" to it but the app does not offer any list or registry of the connecions and disconnections for the devices. I do not know if in the app internal database this information will be stored. So, why not try to create a new aplication and monitor the status for the devices continously and store in some place and, why not, send them by Telegram. With this information you will get the full connections and disconnections for a device.

Because everyone connects to WiFi when they get home, or worse, don't turn it off from their mobile devices when they leave, it can be used to track when a person enters or leaves the house. But this is not the right way to use this example. I am not responsible for any misuse that may be given to this example, is made for academic purposes only.

## Getting the API calls to get the information
To know the API calls that the app make to the Movistar SmartWifi servers you will need a rooted android device with the SmartWifi app installed on it. After that you can send all the traffic through BurpSuite configuring it as a proxy for the device but you wouldn't get any request because the app has the certificate pinning well configured. You can read the following tutorial to bypass this feature and send all the requests to your BurpSuite.

[APP Bypass for SSL Certificate Pinning](https://thehackingfactory.com/bypass-de-certificate-pinning)

## Using the developed example
I only needed three API calls to create this example. 

First of all, I needed the login call to get a JWT token. 

On the second hand I needed another call to get the telephone number for the user (this could be a static value because you will know your own phone number) but, maybe you did not remember it ;). 

Finally, I needed the call to get the list of connected devices. This request get a full list of all the devices that are stored in the HGU router, connected and disconnected, so reviewing the data, if the field rssi_dbm has some value is because the device is currently connected via WiFi.

With all this information is relatively simple to create a script to get the list of devices each 60 seconds and compare it with the previous value stored in a local json file.

## Next steps and ToDo
I am finishing the testing phase of this example and I know that I am not a developer so I have a lot of things to improve in the script. Please, feel free to open a pull request or contact me if you have some questions to be clarified or some ideas to add.

For the ToDo phase I would like to store the devices and application logs in a database as well as the previous state for the devices. After it I would like to add some interactivity in the Telegram Bot.
