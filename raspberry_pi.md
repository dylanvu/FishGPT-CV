* ssh: https://stackoverflow.com/questions/71804429/raspberry-pi-ssh-access-denied
* WiFi: https://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/
    * Use `iwconfig` to check if connected: https://linuxhint.com/check-internet-connectivity-raspberry-pi-terminal/
    * If you are running into WiFi Issues, here are some troubleshooting ideas:
      * Follow this: https://raspberrypi.stackexchange.com/a/114564
      * If you encounter some sort of error, it may be due to an incorrectly written wpa_supplicant.conf file. Keep these in mind:
         * Use double quotes instead of single quotes for names and stuff
         * If no passphrase is required for a network, just omit it altogether:
            ```json
               network={
                   ssid="UCInet Mobile Access"
                   key_mgmt=NONE
               }
            ```
* To fix SSH issues, enable Internet Connection Sharing
   * Windows 10: Go to settings -> "Network and Internet" -> "Advanced Network Settings" -> The WiFi network -> "More adapter options" (edit button) -> "Sharing"
* To download Python, if you are stuck, you can wget from Python directly: https://hub.tcno.co/pi/software/python-update/
