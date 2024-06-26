import argparse
from time import sleep
from colorama import init, Fore, Back, Style
import random

from Core.Config import *
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls

# Initialize colorama
init(autoreset=True)

def display_banner():
    '''Display the banner'''
    banner_text = f"""
    {Fore.MAGENTA + Style.BRIGHT}
    ████████╗███████╗███████╗██╗  ██╗ █████╗ ██████╗       ██████╗ ██████╗ ███████╗
    ╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔══██╗██╔══██╗      ██╔══██╗██╔══██╗██╔════╝
       ██║   █████╗  ███████╗███████║███████║██║  ██║█████╗██████╔╝██████╔╝███████╗
       ██║   ██╔══╝  ╚════██║██╔══██║██╔══██║██║  ██║╚════╝██╔══██╗██╔═══╝ ╚════██║
       ██║   ███████╗███████║██║  ██║██║  ██║██████╔╝      ██║  ██║██║     ███████║
       ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝       ╚═╝  ╚═╝╚═╝     ╚══════╝
    {Style.RESET_ALL}
    """
    print(banner_text)

def debug_config():
    '''Print the current config for debugging'''
    config = check_config()
    print(Fore.BLUE + "Current Configuration:")
    for key, value in config.items():
        print(Fore.BLUE + f"{key}: {value}")
    return config

def prompt_user_inputs():
    '''Prompt user for input'''
    print(Fore.CYAN + Style.BRIGHT + "Enter the number without '+': ", end="")
    number = input()
    while not number.isdigit():
        print(Fore.RED + "Enter a valid number!")
        print(Fore.CYAN + Style.BRIGHT + "Enter the number without '+': ", end="")
        number = input()

    print(Fore.CYAN + Style.BRIGHT + "Enter the number of rounds (1 to 50): ", end="")
    replay = input()
    while not replay.isdigit() or not (1 <= int(replay) <= 50):
        print(Fore.RED + "Enter a valid number of rounds!")
        print(Fore.CYAN + Style.BRIGHT + "Enter the number of rounds (1 to 50): ", end="")
        replay = input()

    print(Fore.CYAN + Style.BRIGHT + "Choose attack type (MIX, SMS, CALL): ", end="")
    type_attack = input().upper()
    while type_attack not in ['MIX', 'SMS', 'CALL']:
        print(Fore.RED + "Enter a valid attack type!")
        print(Fore.CYAN + Style.BRIGHT + "Choose attack type (MIX, SMS, CALL): ", end="")
        type_attack = input().upper()

    print(Fore.CYAN + Style.BRIGHT + "Enable feedback services? (y/n): ", end="")
    feedback = input().lower()
    while feedback not in ['y', 'n']:
        print(Fore.RED + "Enter 'y' to enable or 'n' to disable!")
        print(Fore.CYAN + Style.BRIGHT + "Enable feedback services? (y/n): ", end="")
        feedback = input().lower()

    return number, int(replay), type_attack, feedback == 'y'

def show_info():
    '''Show information about the bomber'''
    info_text = (f'''{Fore.GREEN + Style.BRIGHT}Services - {len(urls("12345"))}\n'''
                 f'''{Fore.GREEN}RU - {sum(1 for i in urls("12345") if i["info"]["country"] == "RU")}'''
                 f'''   |   UZ - {sum(1 for i in urls("12345") if i["info"]["country"] == "UZ")}'''
                 f'''   |   ALL - {sum(1 for i in urls("12345") if i["info"]["country"] == "ALL")}\n\n'''
                 f'''{Fore.GREEN + Style.BRIGHT}Feedback Services - {len(feedback_urls("12345"))}\n'''
                 f'''{Fore.GREEN}RU - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "RU")}'''
                 f'''   |   UZ - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "UZ")}'''
                 f'''   |   ALL - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "ALL")}\n\n'''
                 f'''{Fore.GREEN + Style.BRIGHT}Total - {len(urls("12345")) + len(feedback_urls("12345"))}''')
    print(info_text)

def start_attack(number, replay):
    '''Start the attack'''
    config = debug_config()
    if config['attack'] == 'False':
        print(Fore.GREEN + "Starting attack...")
        change_config('attack', 'True')
        debug_config()  # Print config to verify change
        start_async_attacks(number, replay)
        change_config('attack', 'False')
        debug_config()  # Print config to verify change back
        print(Fore.GREEN + "Attack completed.")
    else:
        print(Fore.RED + "Too many attacks, please wait!")

def main():
    display_banner()
    print(Fore.YELLOW + Style.BRIGHT + "Welcome to TESHAR BOOMBER CLI!")
    show_info()

    while True:
        print(Fore.CYAN + "Choose action (info/start/exit): ", end="")
        action = input().lower()
        while action not in ['info', 'start', 'exit']:
            print(Fore.RED + "Enter a valid action!")
            print(Fore.CYAN + "Choose action (info/start/exit): ", end="")
            action = input().lower()

        if action == 'info':
            show_info()
        elif action == 'start':
            number, replay, type_attack, feedback = prompt_user_inputs()
            change_config('type_attack', type_attack)
            change_config('feedback', 'True' if feedback else 'False')
            debug_config()  # Print config to verify changes
            start_attack(number, replay)
        elif action == 'exit':
            print(Fore.GREEN + "Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
