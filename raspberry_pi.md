* ssh: https://stackoverflow.com/questions/71804429/raspberry-pi-ssh-access-denied
* WiFi: https://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/
    * Use `iwconfig` to check if connected: https://linuxhint.com/check-internet-connectivity-raspberry-pi-terminal/
    * If you are running into WiFi Issues, here are some troubleshooting ideas:
      * Follow this: https://raspberrypi.stackexchange.com/a/114564
      * If you encounter some sort of error, it may be due to an incorrectly written wpa_supplicant.conf file. Keep these in mind:
         * Use double quotes instead of single quotes for names and stuff
         * If no passphrase is required for a network, just omit it altogether:
            ```
               network={
                   ssid="UCInet Mobile Access"
                   key_mgmt=NONE
               }
            ```
      * Here is how you fix WiFi issues forever. This was all done with the pi sshed into the computer via an ethernet cable, with the sharing settings enabled.
         * Here is my wpa_supplicant.conf. Make sure it is properly formatted with no long spaces, all double quotes, etc:
            ```
               ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
               update_config=1
               country=US
               
               network={
               ssid="Dylan-iPhone"
               psk="Goanteaters!"
               proto=RSN
               key_mgmt=WPA-PSK
               pairwise=CCMP
               auth_alg=OPEN
               }
               
               network={
               ssid="UCInet Mobile Access"
               key_mgmt=NONE
               }
               
               network={
               ssid="PlazaVerde-MyCampusNet"
               psk="DylansPassword123"
               proto=RSN
               key_mgmt=WPA-PSK
               pairwise=CCMP
               auth_alg=OPEN
               }
            ```
        * Make sure that the localization, timezone, and WLAN Country are set properly:
           * `sudo raspi-config` --> Localization --> L1 (Locale) should be set to `en_US.UTF-8 UTF-8`, --> go back --> L2 (Timezone) should be `US` --> go back --> L4 (WLAN Country) should be set to the US.
        * Follow these troubeshooting guides
         1. `sudo iwlist wlan0 scan` -> if this returns "Network is down", then try running `sudo ifconfig wlan0 up`. Then, try again. If this works, then the `interfaces file is wrong.`
               * `sudo nano /etc/network/interfaces` then make sure it looks something like:
                  ```
                     auto wlan0
                     iface wlan0 inet dhcp
                     wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
                  ```
         2. Use `iwconfig` to check if the pi sees the WiFi as an accesspoint.
              * Here is a normal one:
                 ```
                  pi@raspberrypi-dylan:~ $ iwconfig
                  lo        no wireless extensions.
                  
                  eth0      no wireless extensions.
                  
                  wlan0     IEEE 802.11  ESSID:"PlazaVerde-MyCampusNet"
                            Mode:Managed  Frequency:5.52 GHz  Access Point: B0:B8:67:2F:D8:D5
                            Bit Rate=24 Mb/s   Tx-Power=31 dBm
                            Retry short limit:7   RTS thr:off   Fragment thr:off
                            Power Management:on
                            Link Quality=50/70  Signal level=-60 dBm
                            Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
                            Tx excessive retries:0  Invalid misc:0   Missed beacon:0
                 ```
         3. If things are abnormal, reboot the pi and then run: `journalctl -xe | grep wpa_supplicant`. The logs should hopefully help.
* To fix SSH issues, enable Internet Connection Sharing
   * Windows 10: Go to settings -> "Network and Internet" -> "Advanced Network Settings" -> The WiFi network -> "More adapter options" (edit button) -> "Sharing"
* To download Python, if you are stuck, you can wget from Python directly: https://hub.tcno.co/pi/software/python-update/
