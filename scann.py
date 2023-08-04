import time
import pywifi
from pywifi import const
from pywifi import PyWiFi
from pywifi import Profile
from mac_vendor_lookup import MacLookup, BaseMacLookup

BaseMacLookup.cache_path = "mac-vendors.txt"
mac = MacLookup()
#mac.update_vendors()  # <- This can take a few seconds for the download and it will be stored in the new path
def getVendor(mac_):
    bssid_=mac_.encode('raw_unicode_escape').decode('utf-8').upper()[:-1]
    vendor_='-'
    try:                        
        vendor_=mac.lookup(bssid_)
    except KeyError as e:
        vendor_='UNKNOWN'
    return vendor_

# WiFi scanner
def wifi_scan():
    # initialize wifi
    wifi = pywifi.PyWiFi()
    # use the first interface
    interface = wifi.interfaces()[0]
    # start scan
    interface.scan()
    for i in range(4):
        time.sleep(1)
        print('\rScanning WiFi, please wait...（' + str(3 - i), end='）')
    print('\rScan Completed！\n' + '-' * 38)
    print('\r{:4}{:6}{}'.format('No.', 'Strength', 'wifi name'))
    # Scan result，scan_results() returns a set, each being a wifi object
    bss = interface.scan_results()
    # a set storing wifi name
    wifi_name_set = set()
    for w in bss:
        #print(w)
        profile = w #Profile()  # create profile instance
        #print(profile.ssid)# = ssid  #name of client
        #print(profile.auth)# = const.AUTH_ALG_OPEN # auth algo
        auth__=''
        for auth_ in profile.auth:
            if auth_==0:            
                auth__='AUTH_ALG_OPEN'
            else:            
                auth__='AUTH_ALG_SHARED'
        #print(profile.akm)#.append(const.AKM_TYPE_WPA2PSK) # key management
        akm__=''
        for akm_ in profile.akm:
            if akm_==0:            
                akm__='AKM_TYPE_NONE'
            if akm_==1:            
                akm__='AKM_TYPE_WPA'
            if akm_==2:            
                akm__='AKM_TYPE_WPAPSK'
            if akm_==3:            
                akm__='AKM_TYPE_WPA2'
            if akm_==4:            
                akm__='AKM_TYPE_WPA2PSK'
        #print(profile.cipher)# = const.CIPHER_TYPE_CCMP #type of cipher     
        cipher_=''
        if profile.cipher==0:            
            cipher_='CIPHER_TYPE_NONE'
        if profile.cipher==1:            
            cipher_='CIPHER_TYPE_WEP'
        if profile.cipher==2:            
            cipher_='CIPHER_TYPE_TKIP'
        if profile.cipher==3:            
            cipher_='CIPHER_TYPE_CCMP'
        #print(profile.key)
        bssid_=w.bssid.encode('raw_unicode_escape').decode('utf-8').upper()[:-1]
        vendor_='-'
        try:                        
            vendor_=mac.lookup(bssid_)
        except KeyError as e:
            vendor_='UNKNOWN'
        # dealing with decoding        
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'), w.freq/1000000,bssid_,vendor_,auth__,akm__,cipher_)
        wifi_name_set.add(wifi_name_and_signal)
    # store into a list sorted by signal strength
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    # format output
    while num < len(wifi_name_list):
        print('\r{:<3d} {}% |{}| {}Ghz [{}]-{}-{},{},{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1], wifi_name_list[num][2], wifi_name_list[num][3], wifi_name_list[num][4], wifi_name_list[num][5], wifi_name_list[num][6], wifi_name_list[num][7]))
        num += 1
    interface.disconnect()
    interface.status()

wifi_scan()
