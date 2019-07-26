# WifiTracker
Example of using and abusing Movistar/O2 SmartWifi API to create an application to track the connections of the devices

## Motivation
Since some months ago I have an O2 fiber connection at home. Attached to this subscription you can use the Movistar SmartWifi app to manage some settings in the provided HGU router. One of the most interesting features is the chance to get a list of the devices connected (WiFi or cabling) in "almost real time" to it but the app does not offer any list or registry of the connecions and disconnections for the devices. I do not know if in the app internal database this information will be stored. So, why not try to create a new aplication and monitor the status for the devices continously and store in some place and, why not, send them by Telegram. With this information you will get the full connections and disconnections for a device.

Because everyone connects to WiFi when they get home, or worse, don't turn it off from their mobile devices when they leave, it can be used to track when a person enters or leaves the house. But this is not the right way to use this example. I am not responsible for any misuse that may be given to this example, is made for academic purposes only.

## Getting the background API calls
