import os, re
from telegram.ext import Application, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

# Bet type to blocks mapping
BET_TYPES = {
    # 1 block
    'r': 1, 'အာ': 1,
    # 19 blocks
    'ပါ': 19, 'ပတ်': 19, 'အပါ': 19,
    # 20 blocks
    'ပူး': 20, 'ပတ်ပူး': 20, 'ပူးပို': 20, 'ထန်': 20, 'ထပ်': 20,
    # 10 blocks
    'ထ': 10, 'ထိပ်': 10, 'ဘရိတ်': 10, 'ဆယ်ပြည့်': 10, 'အပူး': 10,
    # 5 blocks
    'စုံပူး': 5, 'မပူး': 5,
    # 25/50 blocks
    'စမ': 25, 'မမ': 25,
    # 50 blocks
    'စုံဘရိတ်': 50
}

BRANDS = {'du':7,'laos':7,'mm':10,'glo':3,'me':7,'maxi':7,'dubai':7,'london':7}

def get_bet_type(line):
    line_lower = line.lower()
    for bet, blocks in BET_TYPES.items():
        if bet in line_lower: return bet, blocks
    return None, 1  # default 1 block

def calc_blocks(nums, bet_type, blocks):
    n = len(nums)
    if bet_type == 'ခွေ': return n * (n-1)
    if bet_type == 'ပူး' and 'ခွေ' in line: return n*(n-1) + n  # အပူးပါခွေ
    if bet_type == 'ကပ်' or 'ကို' in line:
        # ကပ် = left × right
        mid = len(nums)//2
        return len(nums[:mid]) * len(nums[mid:])
    if bet_type == 'ပါ' or bet_type == 'ပတ်':
        return 19 * n  # 19×numbers
    return blocks * n

def process_line(line):
    nums = re.findall(r'\d{2}', line)
    amts = [int(x) for x in re.findall(r'\d{3,4}', line)]
    is_r = 'r' in line.lower() or 'အာ' in line
    
    bet_type, base_blocks = get_bet_type(line)
    blocks = calc_blocks(nums, bet_type, base_blocks)
    
    if not amts: amts = [1000]
    amt1 = amts[-1]
    amt2 = amts[-2] if len(amts)>=2 else amt1
    
    if is_r:
        total = blocks * amt1 + blocks * amt2
    else:
        total = blocks * amt1
    
    # Special cases
    if 'စမ' in line.lower() and is_r: total *= 2  # 25→50
    if 'စုံဘရိတ်' in line.lower(): total = 50 * amt1
    
    return total

class Bot:
    def calc(self, text):
        total, brand, disc = 0, "GP", 0
        
        for br, d in BRANDS.items():
            if br in text.lower(): brand, disc = br.upper(), d; break
        
        for line in text.split('\n'):
            line = line.strip()
            if not line or brand.lower() in line: continue
            total += process_line(line)
        
        cash = int(total * disc / 100)
        return total, cash, total-cash, brand, disc

bot = Bot()

async def calc(update, context):
    t = bot.calc(update.message.text)
    if t[0]==0: return
    u = update.from_user.first_name[:8]
    await update.message.reply_text(
        f"👤**{u}**\n✅**{t[3]}**\n━━━━━━━━\n💰**{t[0]:,}**\n📉**{t[4]}%**:{t[1]:,}\n━━━━━━━━\n💵**{t[2]:,}** ဘဲလွဲ\n🎰",
        parse_mode='Markdown'
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, calc))
app.run_polling()
