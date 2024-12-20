import subprocess
import time
import requests
import keyboard
import threading
import atexit
import sys
import os
import ctypes
from colorama import init, Fore, Back, Style
init()

def set_console_size():
    kernel32 = ctypes.WinDLL('kernel32')
    handle = kernel32.GetStdHandle(-11)
    buf = ctypes.create_string_buffer(22)
    rect = kernel32.GetConsoleScreenBufferInfo(handle, buf)
    
    coordinates = ctypes.wintypes._COORD(20, 15)
    kernel32.SetConsoleScreenBufferSize(handle, coordinates)

def kill_tor_processes():
    if os.name == 'nt':
        os.system('taskkill /f /im firefox.exe >nul 2>&1')
        os.system('taskkill /f /im tor.exe >nul 2>&1')
    else:
        os.system('pkill -f firefox')
        os.system('pkill -f tor')

class TorManager:
    def __init__(self):
        if os.name == 'nt':
            os.system('mode con: cols=50 lines=15')
        self.tor_process = None
        self.running = True
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9150',
            'https': 'socks5h://127.0.0.1:9150'
        }
        atexit.register(self.cleanup)
        kill_tor_processes()
    
    def cleanup(self):
        kill_tor_processes()
            
    def start_tor_browser(self):
        kill_tor_processes()
        time.sleep(2)
            
        tor_path = r"D:\Tor Browser\Browser\firefox.exe"
        self.tor_process = subprocess.Popen([
            tor_path,
            '--headless'
        ], 
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
        time.sleep(10)
        self.display_menu()
        
    def get_ip_info(self):
        try:
            real_ip = requests.get('https://api.ipify.org?format=json').json()['ip']
            
            session = requests.session()
            session.proxies = self.proxies
            tor_ip = session.get('https://api.ipify.org?format=json').json()['ip']
            
            return real_ip, tor_ip
        except Exception as e:
            return "Error", "Error"

    def display_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        real_ip, tor_ip = self.get_ip_info()
        
        content = [
            "SQTorProxy v1.0",
            "LOLZ - lolz.live/kqlol/",
            f"Real IP: {real_ip}",
            f"TOR IP: {tor_ip}",
            f"Proxy: {self.proxies['http']}",
            "Controls:",
            "[PAGE UP] Restart TOR and get new IP",
            "[PAGE DOWN] Quit"
        ]
        
        width = max(len(line) for line in content) + 4
        
        print(f"{Fore.CYAN}╔{'═' * (width-2)}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}{content[0].center(width-2)}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}{Fore.MAGENTA}{content[1].center(width-2)}{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * (width-2)}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}{content[2]}{' ' * (width-4-len(content[2]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}{content[3]}{' ' * (width-4-len(content[3]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}{content[4]}{' ' * (width-4-len(content[4]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * (width-2)}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}{content[5]}{' ' * (width-4-len(content[5]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.RED}{content[6]}{' ' * (width-4-len(content[6]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.RED}{content[7]}{' ' * (width-4-len(content[7]))}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * (width-2)}╝{Style.RESET_ALL}")

def main():
    manager = TorManager()
    manager.start_tor_browser()
    
    def check_keyboard():
        while manager.running:
            if keyboard.is_pressed('page up'):
                print("\nRestarting TOR...")
                time.sleep(0.5)
                manager.start_tor_browser()
            elif keyboard.is_pressed('page down'):
                print("\nShutting down...")
                manager.running = False
                manager.cleanup()
                os._exit(0)
            time.sleep(0.1)
    
    keyboard_thread = threading.Thread(target=check_keyboard, daemon=True)
    keyboard_thread.start()
    
    while manager.running:
        time.sleep(1)

if __name__ == "__main__":
    set_console_size()
    main()