import os
import re
from telegram.ext import Application, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

b = {'du':7,'laos':7,'mm':10,'glo':3,'me':7,'maxi':7,'dubai':7,'london':7}

async def calc(update, context):
    text = update.message.text.lower()
    total, brand, disc = 0, "GP", 0
    
    for br, d in b.items():
        if br in text: brand, disc = br.upper(), d; break
    
    nums = re.findall(r'\d{2}', update.message.text)
    amts = [int(x) for x in re.findall(r'\d{3,4}', update.message.text)]
    
    n = len(nums)
    if 'r' in text and len(amts)>=2:
        total = n*amts[-2] + n*amts[-1]
    else:
        total = n * (amts[-1] if amts else 1000)
    
    cash = int(total * disc / 100)
    u = update.from_user.first_name[:8]
    
    await update.message.reply_text(
        f"👤**{u}**\n✅**{brand}**\n━━━━━━━━\n💰**{total:,}**\n📉**{disc}%**:{cash:,}\n━━━━━━━━\n💵**{total-cash:,}** ဘဲလွဲ\n🎰",
        parse_mode='Markdown'
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, calc))
print("Bot started")
app.run_polling()
