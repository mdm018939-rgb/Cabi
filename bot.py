import os
import threading
import requests
import telebot
import time
import re
from lingua import Language, LanguageDetectorBuilder
import langcodes
detector = LanguageDetectorBuilder.from_all_languages().build()
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
    "93": ("🇦🇫 Afghanistan", "AF"), "355": ("🇦🇱 Albania", "AL"), "213": ("🇩🇿 Algeria", "DZ"),
    "376": ("🇦🇩 Andorra", "AD"), "244": ("🇦🇴 Angola", "AO"), "1268": ("🇦🇬 Antigua and Barbuda", "AG"),
    "54": ("🇦🇷 Argentina", "AR"), "374": ("🇦🇲 Armenia", "AM"), "61": ("🇦🇺 Australia", "AU"),
    "43": ("🇦🇹 Austria", "AT"), "994": ("🇦🇿 Azerbaijan", "AZ"), "1242": ("🇧🇸 Bahamas", "BS"),
    "973": ("🇧🇭 Bahrain", "BH"), "880": ("🇧🇩 Bangladesh", "BD"), "1246": ("🇧🇧 Barbados", "BB"),
    "375": ("🇧🇾 Belarus", "BY"), "32": ("🇧🇪 Belgium", "BE"), "501": ("🇧🇿 Belize", "BZ"),
    "229": ("🇧🇯 Benin", "BJ"), "975": ("🇧🇹 Bhutan", "BT"), "591": ("🇧🇴 Bolivia", "BO"),
    "387": ("🇧🇦 Bosnia and Herzegovina", "BA"), "267": ("🇧🇼 Botswana", "BW"), "55": ("🇧🇷 Brazil", "BR"),
    "673": ("🇧🇳 Brunei", "BN"), "359": ("🇧🇬 Bulgaria", "BG"), "226": ("🇧🇫 Burkina Faso", "BF"),
    "257": ("🇧🇮 Burundi", "BI"), "238": ("🇨🇻 Cabo Verde", "CV"), "855": ("🇰🇭 Cambodia", "KH"),
    "237": ("🇨🇲 Cameroon", "CM"), "236": ("🇨🇫 Central African", "CF"), "235": ("🇹🇩 Chad", "TD"),
    "56": ("🇨🇱 Chile", "CL"), "86": ("🇨🇳 China", "CN"), "57": ("🇨🇴 Colombia", "CO"),
    "269": ("🇰🇲 Comoros", "KM"), "242": ("🇨🇬 Congo (Republic)", "CG"), "243": ("🇨🇩 Congo (DRC)", "CD"),
    "506": ("🇨🇷 Costa Rica", "CR"), "385": ("🇭🇷 Croatia", "HR"), "53": ("🇨🇺 Cuba", "CU"),
    "357": ("🇨🇾 Cyprus", "CY"), "420": ("🇨🇿 Czechia", "CZ"), "45": ("🇩🇰 Denmark", "DK"),
    "253": ("🇩🇯 Djibouti", "DJ"), "1767": ("🇩🇲 Dominica", "DM"), "1809": ("🇩🇴 Dominican Republic", "DO"),
    "593": ("🇪🇨 Ecuador", "EC"), "20": ("🇪🇬 Egypt", "EG"), "503": ("🇸🇻 El Salvador", "SV"),
    "240": ("🇬🇶 Equatorial Guinea", "GQ"), "291": ("🇪🇷 Eritrea", "ER"), "372": ("🇪🇪 Estonia", "EE"),
    "268": ("🇸🇿 Eswatini", "SZ"), "251": ("🇪🇹 Ethiopia", "ET"), "679": ("🇫🇯 Fiji", "FJ"),
    "358": ("🇫🇮 Finland", "FI"), "33": ("🇫🇷 France", "FR"), "241": ("🇬🇦 Gabon", "GA"),
    "220": ("🇬🇲 Gambia", "GM"), "995": ("🇬🇪 Georgia", "GE"), "49": ("🇩🇪 Germany", "DE"),
    "233": ("🇬🇭 Ghana", "GH"), "30": ("🇬🇷 Greece", "GR"), "1473": ("🇬🇩 Grenada", "GD"),
    "502": ("🇬🇹 Guatemala", "GT"), "224": ("🇬🇳 Guinea", "GN"), "245": ("🇬🇼 Guinea-Bissau", "GW"),
    "592": ("🇬🇾 Guyana", "GY"), "509": ("🇭🇹 Haiti", "HT"), "504": ("🇭🇳 Honduras", "HN"),
    "852": ("🇭🇰 Hong Kong", "HK"), "36": ("🇭🇺 Hungary", "HU"), "354": ("🇮🇸 Iceland", "IS"),
    "91": ("🇮🇳 India", "IN"), "62": ("🇮🇩 Indonesia", "ID"), "98": ("🇮🇷 Iran", "IR"),
    "964": ("🇮🇶 Iraq", "IQ"), "353": ("🇮🇪 Ireland", "IE"), "972": ("🇮🇱 Israel", "IL"),
    "39": ("🇮🇹 Italy", "IT"), "1876": ("🇯🇲 Jamaica", "JM"), "81": ("🇯🇵 Japan", "JP"),
    "962": ("🇯🇴 Jordan", "JO"), "254": ("🇰🇪 Kenya", "KE"), "686": ("🇰🇮 Kiribati", "KI"),
    "383": ("🇽🇰 Kosovo", "XK"), "965": ("🇰🇼 Kuwait", "KW"), "996": ("🇰🇬 Kyrgyzstan", "KG"),
    "856": ("🇱🇦 Laos", "LA"), "371": ("🇱🇻 Latvia", "LV"), "961": ("🇱🇧 Lebanon", "LB"),
    "266": ("🇱🇸 Lesotho", "LS"), "231": ("🇱🇷 Liberia", "LR"), "218": ("🇱🇾 Libya", "LY"),
    "423": ("🇱🇮 Liechtenstein", "LI"), "370": ("🇱🇹 Lithuania", "LT"), "352": ("🇱🇺 Luxembourg", "LU"),
    "261": ("🇲🇬 Madagascar", "MG"), "265": ("🇲🇼 Malawi", "MW"), "60": ("🇲🇾 Malaysia", "MY"),
    "960": ("🇲🇻 Maldives", "MV"), "223": ("🇲🇱 Mali", "ML"), "356": ("🇲🇹 Malta", "MT"),
    "692": ("🇲🇭 Marshall Islands", "MH"), "222": ("🇲🇷 Mauritania", "MR"), "230": ("🇲🇺 Mauritius", "MU"),
    "52": ("🇲🇽 Mexico", "MX"), "691": ("🇫🇲 Micronesia", "FM"), "373": ("🇲🇩 Moldova", "MD"),
    "377": ("🇲🇨 Monaco", "MC"), "976": ("🇲🇳 Mongolia", "MN"), "382": ("🇲🇪 Montenegro", "ME"),
    "212": ("🇲🇦 Morocco", "MA"), "258": ("🇲🇿 Mozambique", "MZ"), "95": ("🇲🇲 Myanmar", "MM"),
    "264": ("🇳🇦 Namibia", "NA"), "674": ("🇳🇷 Nauru", "NR"), "977": ("🇳🇵 Nepal", "NP"),
    "31": ("🇳🇱 Netherlands", "NL"), "64": ("🇳🇿 New Zealand", "NZ"), "505": ("🇳🇮 Nicaragua", "NI"),
    "227": ("🇳🇪 Niger", "NE"), "234": ("🇳🇬 Nigeria", "NG"), "850": ("🇰🇵 North Korea", "KP"),
    "389": ("🇲🇰 North Macedonia", "MK"), "47": ("🇳🇴 Norway", "NO"), "968": ("🇴🇲 Oman", "OM"),
    "92": ("🇵🇰 Pakistan", "PK"), "680": ("🇵🇼 Palau", "PW"), "970": ("🇵🇸 Palestine", "PS"),
    "507": ("🇵🇦 Panama", "PA"), "675": ("🇵🇬 Papua New Guinea", "PG"), "595": ("🇵🇾 Paraguay", "PY"),
    "51": ("🇵🇪 Peru", "PE"), "63": ("🇵🇭 Philippines", "PH"), "48": ("🇵🇱 Poland", "PL"),
    "351": ("🇵🇹 Portugal", "PT"), "974": ("🇶🇦 Qatar", "QA"), "40": ("🇷🇴 Romania", "RO"),
    "7": ("🇷🇺 Russia / 🇰🇿 Kazakhstan", "RU"), "250": ("🇷🇼 Rwanda", "RW"), "1869": ("🇰🇳 Saint Kitts and Nevis", "KN"),
    "1758": ("🇱🇨 Saint Lucia", "LC"), "1784": ("🇻🇨 Saint Vincent and the Grenadines", "VC"), "685": ("🇼🇸 Samoa", "WS"),
    "378": ("🇸🇲 San Marino", "SM"), "239": ("🇸🇹 Sao Tome and Principe", "ST"), "966": ("🇸🇦 Saudi Arabia", "SA"),
    "221": ("🇸🇳 Senegal", "SN"), "381": ("🇷🇸 Serbia", "RS"), "248": ("🇸🇨 Seychelles", "SC"),
    "232": ("🇸🇱 Sierra Leone", "SL"), "65": ("🇸🇬 Singapore", "SG"), "421": ("🇸🇰 Slovakia", "SK"),
    "386": ("🇸🇮 Slovenia", "SI"), "677": ("🇸🇧 Solomon Islands", "SB"), "252": ("🇸🇴 Somalia", "SO"),
    "27": ("🇿🇦 South Africa", "ZA"), "82": ("🇰🇷 South Korea", "KR"), "211": ("🇸🇸 South Sudan", "SS"),
    "34": ("🇪🇸 Spain", "ES"), "94": ("🇱🇰 Sri Lanka", "LK"), "249": ("🇸🇩 Sudan", "SD"),
    "597": ("🇸🇷 Suriname", "SR"), "46": ("🇸🇪 Sweden", "SE"), "41": ("🇨🇭 Switzerland", "CH"),
    "963": ("🇸🇾 Syria", "SY"), "886": ("🇹🇼 Taiwan", "TW"), "992": ("🇹🇯 Tajikistan", "TJ"),
    "255": ("🇹🇿 Tanzania", "TZ"), "66": ("🇹🇭 Thailand", "TH"), "670": ("🇹🇱 Timor-Leste", "TL"),
    "228": ("🇹🇬 Togo", "TG"), "676": ("🇹🇴 Tonga", "TO"), "1868": ("🇹🇹 Trinidad and Tobago", "TT"),
    "216": ("🇹🇳 Tunisia", "TN"), "90": ("🇹🇷 Turkey", "TR"), "993": ("🇹🇲 Turkmenistan", "TM"),
    "688": ("🇹🇻 Tuvalu", "TV"), "256": ("🇺🇬 Uganda", "UG"), "380": ("🇺🇦 Ukraine", "UA"),
    "971": ("🇦🇪 UAE", "AE"), "44": ("🇬🇧 United Kingdom", "GB"), "1": ("🇺🇸 USA / 🇨🇦 Canada", "US"),
    "598": ("🇺🇾 Uruguay", "UY"), "998": ("🇺🇿 Uzbekistan", "UZ"), "678": ("🇻🇺 Vanuatu", "VU"),
    "379": ("🇻🇦 Vatican City", "VA"), "58": ("🇻🇪 Venezuela", "VE"), "84": ("🇻🇳 Vietnam", "VN"),
    "967": ("🇾🇪 Yemen", "YE"), "260": ("🇿🇲 Zambia", "ZM"), "263": ("🇿🇼 Zimbabwe", "ZW"),
    "225": ("🇨🇮 Côte d'Ivoire", "CI"), "262": ("🇷🇪 Réunion / Mayotte", "RE"), "297": ("🇦🇼 Aruba", "AW"),
    "298": ("🇫🇴 Faroe Islands", "FO"), "299": ("🇬🇱 Greenland", "GL"), "350": ("🇬🇮 Gibraltar", "GI"),
    "590": ("🇬🇵 Guadeloupe", "GP"), "594": ("🇬🇫 French Guiana", "GF"), "596": ("🇲🇶 Martinique", "MQ"),
    "599": ("🇨🇼 Curaçao", "CW"),
}

def get_country_info(phone_number):
    for length in [4, 3, 2, 1]:
        prefix = phone_number[:length]
        if prefix in COUNTRY_CODES:
            name, code = COUNTRY_CODES[prefix]
            return f"{name} ({code})"
    return "🌐 Unknown"

def detect_service(message_text):
    msg_lower = message_text.lower()
    
    known = {
        "Instagram": ["instagram", "insta"],
        "Facebook": ["facebook", "fb", "فيسبوك", "фейсбук"],
        "WhatsApp": ["whatsapp", "واتساب"],
        "Telegram": ["telegram", "телеграм"],
        "Discord": ["discord"],
        "Google": ["google", "gmail"],
        "TikTok": ["tiktok"],
        "Snapchat": ["snapchat"],
        "Twitter": ["twitter", "x.com"],
        "Microsoft": ["microsoft", "outlook", "hotmail"],
        "PayPal": ["paypal"],
        "Amazon": ["amazon"],
        "Netflix": ["netflix"],
        "LinkedIn": ["linkedin"],
        "Apple": ["apple", "icloud"],
        "Uber": ["uber"],
        "Spotify": ["spotify"],
        "Binance": ["binance"],
    }
    
    for service, keywords in known.items():
        for keyword in keywords:
            if keyword in msg_lower:
                return service
    
    skip = {"Your", "The", "This", "Code", "OTP", "PIN", "SMS", "From", "Dear", "Hello", "Please", "Use", "Don", "Not", "Share", "New", "Account", "For", "With", "You", "Has", "Been", "Are", "Was", "That", "Have", "Will", "Can", "Get", "Our", "One", "Time", "Enter", "Verify", "Login", "Sign", "App", "Now", "Click", "Here", "Link", "Sent", "Send", "Never", "Anyone", "Someone", "Anybody", "Nobody", "Everybody", "Everyone", "Anything", "Nothing", "Contact", "Support", "Team", "Thank", "Thanks", "Best", "Regards", "If", "It", "And", "But", "So", "Do", "Did", "Just", "Only", "Valid", "Expires", "Expire", "Minutes", "Minute", "Seconds", "Hour", "Hours", "Day", "Days", "Number", "Phone", "Mobile", "Message", "Text", "Reply", "Call", "Ignore", "Disregard", "Warning", "Alert", "Important", "Note", "Notice", "Attention", "Security", "Confirm", "Confirmation", "Request", "Requested", "Made", "Change", "Changed", "Update", "Updated", "Reset", "Password", "Access", "Activity", "Detected", "Device", "Location", "May", "Might", "Should", "Would", "Could", "Must", "Also", "Again", "Still", "Yet", "Already", "Below", "Above", "Following", "Customer", "Center", "Website", "Visit", "Open", "Tap", "Press", "Type", "Copy", "Paste", "Screen", "Page"}
    
    match = re.search(r'\b([A-Z][a-zA-Z0-9]{2,})\b', message_text)
    if match:
        word = match.group(1)
        if word not in skip:
            return word
    
    return "𝙐𝙣𝙠𝙣𝙤𝙬𝙣"

def mask_number(phone_number):
    if len(phone_number) > 8:
        middle_x = "X" * (len(phone_number) - 8)
        return f"{phone_number[:5]}{middle_x}{phone_number[-3:]}"
    return phone_number

# 🎯 ৩ সংখ্যা, ৫ সংখ্যা কিংবা মাঝখানে স্পেস দেওয়া ওটিপি রিড করার শক্তিশালী লজিক
def extract_otp_code(message_text):
    # কোড মাঝখানে স্পেস বা হাইফেন দিয়ে আলাদা থাকতে পারে (যেমন: 301 726 বা 404-793)
    # অথবা টানা সংখ্যা হতে পারে (৩ থেকে ১০ সংখ্যা পর্যন্ত)
    match = re.search(r'\b\d{2,5}[\s-]\d{2,5}\b|\b\d{3,10}\b', message_text)
    if match:
        # যেভাবেই আসুক, স্পেস/হাইফেন সরিয়ে একটানা সংখ্যা বানিয়ে ফেরত দেওয়া হচ্ছে
        return re.sub(r'[\s-]', '', match.group(0))
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
                for otp_index, otp in enumerate(otps_list):
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
                            lang = detector.detect_language_of(message_content)
                            lang_name = lang.name.title() if lang else "Unknown"
                            lang_tag = f"#{lang_name}"
                        except:
                            lang_tag = "#Unknown"
                        
                        # 📝 আগের সব ডিটেইলস ঠিক রেখে শুধু নিচের মেসেজটি blockquote করা হলো
                        otp_message_text = (
                            f"🪽 <b>Your SMS Received</b> 🪽\n\n"
                            f"🌐 <b>Service:</b> {service_name}\n"
                            f"🏳️ <b>Country:</b> {country_display}\n"
                            f"📞 <b>Number:</b> <code>{masked_num[:-3]}</code>{masked_num[-3:]}\n\n"
                            f"🔐 <b>Code:</b> <code>{otp_code}</code>\n\n"
                            f"{lang_tag}\n<blockquote><code>{safe_message_content}</code></blockquote>"
                        )
                        
                        # 🔘 বাটন দুটি এক লাইনে পাশাপাশি (Inline Row) সেট করা হলো
                        colors = ["primary", "success", "danger"]
                        color1 = colors[otp_index % 3]
                        color2 = colors[(otp_index + 1) % 3]
                        color3 = colors[(otp_index + 2) % 3]

                        markup = telebot.types.InlineKeyboardMarkup()
                        markup.row(
                            telebot.types.InlineKeyboardButton(
                                "Copy Code",
                                copy_text=telebot.types.CopyTextButton(text=str(otp_code)),
                                style=color1
                            )
                        )
                        markup.row(
                            telebot.types.InlineKeyboardButton("Get Number", url="https://t.me/SMSTOSMSBOT?start=start", style=color2),
                            telebot.types.InlineKeyboardButton("Join Channel", url="https://t.me/+LZrutZRrpbRkNDVl", style=color3)
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
        
    time.sleep(5)  # ২ সেকেন্ড পর পর সেফলি রিকোয়েস্ট হিট হবে
