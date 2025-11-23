from colorama import init, Fore, Style
init(autoreset=True)

def info(msg):
    print(Fore.CYAN + "[*] " + Style.RESET_ALL + str(msg))

def warn(msg):
    print(Fore.YELLOW + "[!] " + Style.RESET_ALL + str(msg))

def error(msg):
    print(Fore.RED + "[-] " + Style.RESET_ALL + str(msg))
