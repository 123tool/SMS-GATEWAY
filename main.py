import os
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Provider Libraries
from twilio.rest import Client
import vonage
import requests

# Inisialisasi
init(autoreset=True)
G, R, Y, C, W = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.WHITE
RES = Style.RESET_ALL

class SpyESmsPro:
    def __init__(self):
        self.version = "5.0.0"
        self.author = "SPY-E & 123Tool"
        self.lock = threading.Lock()
        self.success = 0
        self.failed = 0

    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""
{C}  ██████  ██████  ██    ██      ███████     ██████  ██████   ██████  
{C} ██      ██    ██  ██  ██       ██          ██   ██ ██   ██ ██    ██ 
{C}  █████  ██    ██   ████  █████ █████       ██████  ██████  ██    ██ 
{C}      ██ ██    ██    ██         ██          ██      ██   ██ ██    ██ 
{C} ██████   ██████     ██         ███████     ██      ██   ██  ██████  
{W} ---------------------------------------------------------------------
{Y} [ Version : {self.version} ] [ Coded By : {self.author} ]
{W} ---------------------------------------------------------------------
        """)

    def log_result(self, status, phone):
        folder = "results"
        if not os.path.exists(folder): os.makedirs(folder)
        with self.lock:
            with open(f"{folder}/{status}.txt", "a") as f:
                f.write(f"{phone}\n")

    def setup_data(self):
        if not os.path.exists('data'): os.makedirs('data')
        try:
            phones = open('data/phone.txt', 'r').read().splitlines()
            message = open('data/message.txt', 'r').read()
            return phones, message
        except FileNotFoundError:
            print(f"{R}[!] Error: data/phone.txt atau data/message.txt tidak ditemukan!")
            return [], ""

    # --- Worker: Twilio ---
    def worker_twilio(self, phone, sid, token, sender, msg):
        try:
            client = Client(sid, token)
            client.messages.create(body=msg, from_=sender, to=phone)
            with self.lock: self.success += 1
            print(f"{G}[OK] {phone}{RES}")
            self.log_result("success", phone)
        except Exception as e:
            with self.lock: self.failed += 1
            print(f"{R}[FAIL] {phone} | {str(e)[:30]}{RES}")
            self.log_result("failed", phone)

    # --- Worker: Vonage ---
    def worker_vonage(self, phone, key, secret, sender, msg):
        try:
            client = vonage.Client(key=key, secret=secret)
            sms = vonage.Sms(client)
            res = sms.send_message({"from": sender, "to": phone, "text": msg})
            if res["messages"][0]["status"] == "0":
                with self.lock: self.success += 1
                print(f"{G}[OK] {phone}{RES}")
                self.log_result("success", phone)
            else:
                raise Exception(res["messages"][0]["error-text"])
        except Exception as e:
            with self.lock: self.failed += 1
            print(f"{R}[FAIL] {phone} | {str(e)[:30]}{RES}")
            self.log_result("failed", phone)

    def run(self):
        self.banner()
        phones, message = self.setup_data()
        if not phones: return

        print(f"{W}Total Numbers: {Y}{len(phones)}")
        print(f"{W}Thread Power : {Y}10 (Fast Mode)\n")
        
        print(f"{C}[1] Twilio Gateway")
        print(f"{C}[2] Vonage Gateway")
        print(f"{C}[0] Exit")
        
        opt = input(f"\n{W}Select Option > {RES}")

        if opt == '1':
            sid = input(f"{Y}Twilio SID: {RES}")
            token = input(f"{Y}Twilio Token: {RES}")
            sender = input(f"{Y}Sender Num: {RES}")
            with ThreadPoolExecutor(max_workers=10) as executor:
                for p in phones:
                    executor.submit(self.worker_twilio, p, sid, token, sender, message)
        
        elif opt == '2':
            key = input(f"{Y}Vonage Key: {RES}")
            sec = input(f"{Y}Vonage Secret: {RES}")
            sender = input(f"{Y}Sender Name: {RES}")
            with ThreadPoolExecutor(max_workers=10) as executor:
                for p in phones:
                    executor.submit(self.worker_vonage, p, key, secret, sender, message)

        print(f"\n{W}-----------------------------------")
        print(f"{G}Success: {self.success} | {R}Failed: {self.failed}")
        print(f"{W}Results saved in results/ folder.")

if __name__ == "__main__":
    app = SpyESmsPro()
    app.run()
