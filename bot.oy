import os
import threading
import requests
import telebot
import time
import re
import html  # HTML Escape করার জন্য ইমপোর্ট করা হলো
from datetime import datetime
import pytz

# ──────────────────────────────────────────────────────────
# কনফিগারেশন
# ──────────────────────────────────────────────────────────
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "-1003449804166"
API_KEY = "MINQWI3C03A"
API_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api/success-otp"

bot = telebot.TeleBot(BOT_TOKEN)

# ডুপ্লিকেট ওটিপি চেক করার জন্য মেমোরি সেট
sent_otp_ids = set()
is_first_run = True  # পুরোনো ডেটা স্কিপ করার জন্য ফ্ল্যাগ

# 🌍 গ্লোবাল কান্ট্রি কোড ডাটাবেজ
COUNTRY_CODES = {
    "93": "🇦🇫 Afghanistan", "355": "🇦🇱 Albania", "213": "🇩🇿 Algeria",
    "376": "🇦🇩 Andorra", "244": "🇦🇴 Angola", "1268": "🇦🇬 Antigua and Barbuda",
    "54": "🇦🇷 Argentina", "374": "🇦🇲 Armenia", "61": "🇦🇺 Australia",
    "43": "🇦🇹 Austria", "994": "🇦🇿 Azerbaijan", "1242": "🇧🇸 Bahamas",
    "973": "🇧🇭 Bahrain", "880": "🇧🇩 Bangladesh", "1246": "🇧🇧 Barbados",
    "375": "🇧🇾 Belarus", "32": "🇧🇪 Belgium", "501": "🇧🇿 Belize",
    "229": "🇧🇯 Benin", "975": "🇧🇹 Bhutan", "591": "🇧🇴 Bolivia",
    "387": "🇧🇦 Bosnia and Herzegovina", "267": "🇧🇼 Botswana", "55": "🇧🇷 Brazil",
    "673": "🇧🇳 Brunei", "359": "🇧🇬 Bulgaria", "226": "🇧🇫 Burkina Faso",
    "257": "🇧🇮 Burundi", "238": "🇨🇻 Cabo Verde", "855": "🇰🇭 Cambodia",
    "237": "🇨🇲 Cameroon", "236": "🇨🇫 Central African Republic", "235": "🇹🇩 Chad",
    "56": "🇨🇱 Chile", "86": "🇨🇳 China", "57": "🇨🇴 Colombia",
    "269": "🇰🇲 Comoros", "242": "🇨🇬 Congo (Republic)", "243": "🇨🇩 Congo (DRC)",
    "506": "🇨🇷 Costa Rica", "385": "🇭🇷 Croatia", "53": "🇨🇺 Cuba",
    "357": "🇨🇾 Cyprus", "420": "🇨🇿 Czechia", "45": "🇩🇰 Denmark",
    "253": "🇩🇯 Djibouti", "1767": "🇩🇲 Dominica", "1809": "🇩🇴 Dominican Republic",
    "593": "🇪🇨 Ecuador", "20": "🇪🇬 Egypt", "503": "🇸🇻 El Salvador",
    "240": "🇬🇶 Equatorial Guinea", "291": "🇪🇷 Eritrea", "372": "🇪🇪 Estonia",
    "268": "🇸🇿 Eswatini", "251": "🇪🇹 Ethiopia", "679": "🇫🇯 Fiji",
    "358": "🇫🇮 Finland", "33": "🇫🇷 France", "241": "🇬🇦 Gabon",
    "220": "🇬🇲 Gambia", "995": "🇬🇪 Georgia", "49": "🇩🇪 Germany",
    "233": "🇬🇭 Ghana", "30": "🇬🇷 Greece", "1473": "🇬🇩 Grenada",
    "502": "🇬🇹 Guatemala", "224": "🇬🇳 Guinea", "245": "🇬🇼 Guinea-Bissau",
    "592": "🇬🇾 Guyana", "509": "🇭🇹 Haiti", "504": "🇭🇳 Honduras",
    "852": "🇭🇰 Hong Kong", "36": "🇭🇺 Hungary", "354": "🇮🇸 Iceland",
    "91": "🇮🇳 India", "62": "🇮🇩 Indonesia", "98": "🇮🇷 Iran",
    "964": "🇮🇶 Iraq", "353": "🇮🇪 Ireland", "972": "🇮🇱 Israel",
    "39": "🇮🇹 Italy", "1876": "🇯🇲 Jamaica", "81": "🇯🇵 Japan",
    "962": "🇯🇴 Jordan", "254": "🇰🇪 Kenya", "686": "🇰🇮 Kiribati",
    "383": "🇽🇰 Kosovo", "965": "🇰🇼 Kuwait", "996": "🇰🇬 Kyrgyzstan",
    "856": "🇱🇦 Laos", "371": "🇱🇻 Latvia", "961": "🇱🇧 Lebanon",
    "266": "🇱🇸 Lesotho", "231": "🇱🇷 Liberia", "218": "🇱🇾 Libya",
    "423": "🇱🇮 Liechtenstein", "370": "🇱🇹 Lithuania", "352": "🇱🇺 Luxembourg",
    "261": "🇲🇬 Madagascar", "265": "🇲🇼 Malawi", "60": "🇲🇾 Malaysia",
    "960": "🇲🇻 Maldives", "223": "🇲🇱 Mali", "356": "🇲🇹 Malta",
    "692": "🇲🇭 Marshall Islands", "222": "🇲🇷 Mauritania", "230": "🇲🇺 Mauritius",
    "52": "🇲🇽 Mexico", "691": "🇫🇲 Micronesia", "373": "🇲🇩 Moldova",
    "377": "🇲🇨 Monaco", "976": "🇲🇳 Mongolia", "382": "🇲🇪 Montenegro",
    "212": "🇲🇦 Morocco", "258": "🇲🇿 Mozambique", "95": "🇲🇲 Myanmar",
    "264": "🇳🇦 Namibia", "674": "🇳🇷 Nauru", "977": "🇳🇵Nepal",
    "31": "🇳🇱 Netherlands", "64": "🇳🇿 New Zealand", "505": "🇳🇮 Nicaragua",
    "227": "🇳🇪 Niger", "234": "🇳🇬 Nigeria", "850": "🇰🇵 North Korea",
    "389": "🇲🇰 North Macedonia", "47": "🇳🇴 Norway", "968": "🇴🇲 Oman",
    "92": "🇵🇰 Pakistan", "680": "🇵🇼 Palau", "970": "🇵🇸 Palestine",
    "507": "🇵🇦 Panama", "675": "🇵🇬 Papua New Guinea", "595": "🇵🇾 Paraguay",
    "51": "🇵🇪 Peru", "63": "🇵🇭 Philippines", "48": "🇵🇱 Poland",
    "351": "🇵🇹 Portugal", "974": "🇶🇦 Qatar", "40": "🇷🇴 Romania",
    "7": "🇷🇺 Russia / 🇰🇿 Kazakhstan", "250": "🇷🇼 Rwanda",
    "1869": "🇰🇳 Saint Kitts and Nevis", "1758": "🇱🇨 Saint Lucia",
    "1784": "🇻🇨 Saint Vincent and the Grenadines", "685": "🇼🇸 Samoa",
    "378": "🇸🇲 San Marino", "239": "🇸🇹 Sao Tome and Principe",
    "966": "🇸🇦 Saudi Arabia", "221": "🇸🇳 Senegal", "381": "🇷🇸 Serbia",
    "248": "🇸🇨 Seychelles", "232": "🇸🇱 Sierra Leone", "65": "🇸🇬 Singapore",
    "421": "🇸🇰 Slovakia", "386": "🇸🇮 Slovenia", "677": "🇸🇧 Solomon Islands",
    "252": "🇸🇴 Somalia", "27": "🇿🇦 South Africa", "82": "🇰🇷 South Korea",
    "211": "🇸🇸 South Sudan", "34": "🇪🇸 Spain", "94": "🇱🇰 Sri Lanka",
    "249": "🇸🇩 Sudan", "597": "🇸🇷 Suriname", "46": "🇸🇪 Sweden",
    "41": "🇨🇭 Switzerland", "963": "🇸🇾 Syria", "886": "🇹🇼 Taiwan",
    "992": "🇹🇯 Tajikistan", "255": "🇹🇿 Tanzania", "66": "🇹🇭 Thailand",
    "670": "🇹🇱 Timor-Leste", "228": "🇹🇬 Togo", "676": "🇹🇴 Tonga",
    "1868": "🇹🇹 Trinidad and Tobago", "216": "🇹🇳 Tunisia", "90": "🇹🇷 Turkey",
    "993": "🇹🇲 Turkmenistan", "688": "🇹🇻 Tuvalu", "256": "🇺🇬 Uganda",
    "380": "🇺🇦 Ukraine", "971": "🇦🇪 UAE", "44": "🇬🇧 United Kingdom",
    "1": "🇺🇸 USA / 🇨🇦 Canada", "598": "🇺🇾 Uruguay", "998": "🇺🇿 Uzbekistan",
    "678": "🇻🇺 Vanuatu", "379": "🇻🇦 Vatican City", "58": "🇻🇪 Venezuela",
    "84": "🇻🇳 Vietnam", "967": "🇾🇪 Yemen", "260": "🇿🇲 Zambia",
    "263": "🇿🇼 Zimbabwe"
}

def get_country_info(phone_number):
    for length in [4, 3, 2, 1]:
        prefix = phone_number[:length]
        if prefix in COUNTRY_CODES:
            return COUNTRY_CODES[prefix]
    return "🌐 Unknown"

def detect_service(message_text):
    msg_lower = message_text.lower()
    if re.search(r'\b(instagram|ig|insta)\b', msg_lower):
        return "Instagram"
    elif re.search(r'\b(facebook|fb)\b', msg_lower):
        return "Facebook"
    elif re.search(r'\b(whatsapp|wa)\b', msg_lower):
        return "WhatsApp"
    elif re.search(r'\b(telegram|tg)\b', msg_lower):
        return "Telegram"
    elif "discord" in msg_lower: 
        return "Discord"
    elif re.search(r'\b(google|g-)\b', msg_lower):
        return "Google"
    elif re.search(r'\b(tiktok)\b', msg_lower):
        return "TikTok"
    return "Other Service"

def mask_number(phone_number):
    if len(phone_number) > 7:
        return f"{phone_number[:4]}****{phone_number[-3:]}"
    return phone_number

# 🎯 ৩ সংখ্যা, ৫ সংখ্যা কিংবা মাঝখানে স্পেস দেওয়া ওটিপি রিড করার শক্তিশালী লজিক
def extract_otp_code(message_text):
    # প্রথমে মাঝখানে স্পেস থাকা ওটিপি চেক করবে (যেমন: 301 726)
    spaced_match = re.search(r'\b\d{3}\s\d{3}\b', message_text)
    if spaced_match:
        return spaced_match.group(0)
    
    # টানা ৩ থেকে ৮ ডিজিটের যেকোনো ওটিপি চেক করবে (টেলিগ্রাম বা অন্যান্য কোড)
    match = re.search(r'\b\d{3,8}\b', message_text)
    if match:
        return match.group(0)
    return "N/A"

print("📡 ওটিপি মনিটরিং বট ফুল স্পিডে চালু হয়েছে...")

def run_keep_alive_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class PingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    server.serve_forever()


threading.Thread(target=run_keep_alive_server, daemon=True).start()

while True:
    try:
        headers = {
            "mauthapi": API_KEY,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        response = requests.get(API_URL, headers=headers, timeout=5)
        
        if response.status_code == 200:
            res_data = response.json()
            
            if res_data.get("meta", {}).get("code") == 200:
                otps_list = res_data.get("data", {}).get("otps", [])
                
                # প্রথম রান হলে এপিআই-এর বর্তমান ওল্ড ডাটা সেট-এ সেভ করে স্কিপ করবে
                if is_first_run:
                    for otp in otps_list:
                        otp_id = otp.get("otp_id")
                        if otp_id:
                            sent_otp_ids.add(otp_id)
                    is_first_run = False
                    print("✅ পুরোনো সব ওটিপি মেমোরিতে সেভ করা হয়েছে। এখন নতুন ওটিপির জন্য রেডি...")
                    continue
                
                # নতুন লাইভ ওটিপি রিসিভ করার লুপ
                for otp in otps_list:
                    otp_id = otp.get("otp_id")
                    
                    if otp_id and otp_id not in sent_otp_ids:
                        raw_number = str(otp.get("number", ""))
                        message_content = otp.get("message", "")
                        unix_time = otp.get("time", 0)
                        
                        # 🔒 HTML parsing error ফিক্স করার জন্য html.escape ব্যবহার
                        safe_message_content = html.escape(message_content)
                        otp_code = html.escape(extract_otp_code(message_content))
                        service_name = html.escape(detect_service(message_content))
                        country_display = html.escape(get_country_info(raw_number))
                        masked_num = html.escape(mask_number(raw_number))
                        
                        try:
                            utc_dt = datetime.utcfromtimestamp(unix_time / 1000.0).replace(tzinfo=pytz.utc)
                            bd_tz = pytz.timezone('Asia/Dhaka')
                            bd_dt = utc_dt.astimezone(bd_tz)
                            formatted_time = bd_dt.strftime('%Y-%m-%d %H:%M:%S')
                        except Exception:
                            formatted_time = "Unknown"
                            
                        # 📝 আগের সব ডিটেইলস ঠিক রেখে শুধু নিচের মেসেজটি blockquote করা হলো
                        otp_message_text = (
                            f"🔊 <b>YOUR Key Received</b>\n\n"
                            f"🌐 <b>Service:</b> {service_name}\n"
                            f"🏳️ <b>Country:</b> {country_display}\n"
                            f"📞 <b>Number:</b> <code>{masked_num}</code>\n"
                            f"🔑 <b>Your Key:</b> <code>{otp_code}</code>\n"
                            f"🕒 <b>Time:</b> {formatted_time}\n\n\n"
                            f"<blockquote>{safe_message_content}</blockquote>"
                        )
                        
                        # 🔘 বাটন দুটি এক লাইনে পাশাপাশি (Inline Row) সেট করা হলো
                        markup = telebot.types.InlineKeyboardMarkup()
                        markup.row(
                            telebot.types.InlineKeyboardButton("🤖 Number Bot", url="https://t.me/SMSTOSMSBOT?start=start"),
                            telebot.types.InlineKeyboardButton("📬 Main channel", url="https://t.me/+LZrutZRrpbRkNDVl")
                        )
                        
                        bot.send_message(CHAT_ID, otp_message_text, parse_mode="HTML", reply_markup=markup)
                        print(f"✅ নতুন লাইভ ওটিপি গ্রুপে পাঠানো হয়েছে: {raw_number}")
                        
                        sent_otp_ids.add(otp_id)
                        
                # মেমোরি কন্ট্রোল
                if len(sent_otp_ids) > 5000:
                    sent_otp_ids = set(list(sent_otp_ids)[-2000:])
                    
        else:
            print(f"⚠️ API Status Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ লুপ এরর: {str(e)}")
        
    time.sleep(2)  # ২ সেকেন্ড পর পর সেফলি রিকোয়েস্ট হিট হবে
