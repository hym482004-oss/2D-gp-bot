import os, re
from telegram.ext import Application, MessageHandler, filters

TOKEN = os.environ.get("TOKEN")

class Bot:
    def calc(self, text):
        b = {'du':7,'laos':7,'mm':10,'glo':3,'me':7,'maxi':7,'dubai':7,'london':7}
        total, brand, disc = 0, "GP", 0
        
        for br, d in b.items():
            if br in text.lower(): brand, disc = br.upper(), d; break
        
        nums = re.findall(r'\d{2}', text)
        amts = [int(x) for x in re.findall(r'\d{3,4}', text)]
        
        for line in text.split('\n'):
            nline = re.findall(r'\d{2}', line)
            if len(nline)<1: continue
            
            is_r = 'r' in line.lower()
            if is_r and len(amts)>=2:
                amt1, amt2 = int(amts[-2]), int(amts[-1])
            else:
                amt1 = int(amts[-1]) if amts else 1000
                amt2 = amt1
            
            n = len(nline)
            if is_r: total += n*amt1 + n*amt2
            else: total += n*amt1
        
        cash = int(total * disc / 100)
        return total, cash, total-cash, brand, disc

bot = Bot()

async def calc(update,
