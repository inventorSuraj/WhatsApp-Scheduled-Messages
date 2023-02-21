import os
import sys
import time
import platform
import subprocess
import configparser
from twilio.rest import Client


def install(package_manager, package_name):
    """Installs the specified package using the given package manager."""
    if package_manager == 'apt-get':
        cmd = f'sudo apt-get install {package_name} -y'
    elif package_manager == 'brew':
        cmd = f'brew install {package_name}'
    elif package_manager == 'choco':
        cmd = f'choco install {package_name} -y'
    else:
        print(f'Error: Unsupported package manager {package_manager}.')
        sys.exit(1)
    
    subprocess.call(cmd.split())


def check_dependencies():
    """Checks if Python3 and pip are installed, and installs them if not."""
    if not os.path.exists('/usr/bin/python3'):
        if platform.system() == 'Linux':
            if os.path.exists('/usr/bin/apt-get'):
                print('Installing Python3...')
                install('apt-get', 'python3')
            else:
                print('Error: apt-get package manager not found.')
                sys.exit(1)
        elif platform.system() == 'Darwin':
            if os.path.exists('/usr/local/bin/brew'):
                print('Installing Python3...')
                install('brew', 'python@3')
            else:
                print('Error: Homebrew package manager not found.')
                sys.exit(1)
        else:
            print('Error: Unsupported operating system.')
            sys.exit(1)
    
    if not os.path.exists('/usr/bin/pip'):
        if platform.system() == 'Linux':
            if os.path.exists('/usr/bin/apt-get'):
                print('Installing pip...')
                install('apt-get', 'python3-pip')
            else:
                print('Error: apt-get package manager not found.')
                sys.exit(1)
        elif platform.system() == 'Darwin':
            if os.path.exists('/usr/local/bin/brew'):
                print('Installing pip...')
                install('brew', 'pip')
            else:
                print('Error: Homebrew package manager not found.')
                sys.exit(1)
        else:
            print('Error: Unsupported operating system.')
            sys.exit(1)


def get_user_input():
    """Prompts the user for Twilio credentials, message timing, frequency, and recipient numbers."""
    print('Enter your Twilio credentials:')
    account_sid = input('Account SID: ')
    auth_token = input('Auth Token: ')
    
    print('\nEnter the message timing:')
    start_time = input('Start time (HH:MM:SS): ')
    end_time = input('End time (HH:MM:SS): ')
    interval = input('Interval (in minutes): ')
    
    print('\nEnter the recipient numbers:')
    recipient_numbers = []
    while True:
        number = input('Recipient number (with country code and + symbol): ')
        recipient_numbers.append(number)
        more_numbers = input('Add another recipient? (y/n): ')
        if more_numbers.lower() != 'y':
            break
    
    return account_sid, auth_token, start_time, end_time, interval, recipient_numbers


def save_user_input(account_sid, auth_token, start_time, end_time, interval, recipient_numbers):
    """Saves the user input to a file."""
    config = configparser.ConfigParser
