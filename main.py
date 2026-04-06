import telebot
from telebot import types
import requests

BOT_TOKEN = "7998869249:AAF-BKaU2r-C12tTtiFsAjQZ1-k-xIz4evc"
API_URL = "https://hevoteam.com/api/v2"
API_KEY = "bfa5d29a084f235800e06d930c1c242c"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
user_data = {}

SERVICES = {
    "Instagram": {
        "Followers": {
            "75": "متابعين انستجرام (10k/لليوم) بدون اعادة تعبئة",
            "6481": "متابعين انستجرام (50k/لليوم) بدون اعادة تعبئة",
            "6476": "متابعين انستجرام (100k/لليوم) بدون اعادة تعبئة",
        },
        "Likes": {
            "5551": "اعجابات انستجرام (10k/لليوم) بدون اعادة تعبئة",
            "57": "اعجابات انستجرام (50k/لليوم) بدون اعادة تعبئة",
        },
        "Views": {
            "4625": "مشاهدات انستجرام رخيصة",
            "4478": "مشاهدات انستجرام (5m/لليوم)",
            "628": "مشاهدات انستجرام VIP",
        },
        "Save": {
            "4562": "حفظ انستجرام سريع",
        },
        "Share": {
            "5552": "مشاركات انستجرام الأرخص",
        },
    },
    "Facebook": {
        "Followers": {
            "288": "متابعين فيسبوك (10-50ك/لليوم) بدون اعادة تعبئة",
            "16": "متابعين فيسبوك (50k/لليوم)",
            "291": "متابعين فيسبوك (10-50ك/لليوم)",
            "7": "متابعين فيسبوك (1k/لليوم) اعادة تعبئة 30 يوم",
        },
        "Reactions": {
            "4196": "رياكت فيسبوك (❤️-👍) (10k/لليوم) vip fast",
            "5605": "رياكت فيسبوك (👍) (10k/لليوم) vip fast",
            "4181": "رياكت فيسبوك (🥰) (10k/لليوم) vip fast",
            "4192": "رياكت فيسبوك (❤️) (10k/لليوم) vip fast",
            "4193": "رياكت فيسبوك (😮) (10k/لليوم) vip fast",
            "4194": "رياكت فيسبوك (😂) (10k/لليوم) vip fast",
            "4195": "رياكت فيسبوك (😥) (10k/لليوم) vip fast",
        },
        "Views": {
            "647": "مشاهدات فيسبوك (20k/لليوم) (اعادة تعبئة شهر)",
            "6413": "مشاهدات فيسبوك (5m/لليوم) (اعادة تعبئة شهر)",
        },
    },
    "TikTok": {
        "Followers": {
            "6400": "متابعين تيك توك (15k/لليوم)",
            "6402": "متابعين تيك توك (20k/لليوم)",
        },
        "Likes": {
            "795": "لايكات تيك توك (5-10k/لليوم)",
            "376": "لايكات تيك توك (50k/لليوم)",
            "5402": "لايكات تيك توك (100k/لليوم) vip fast",
        },
        "Views": {
            "4586": "مشاهدات تيك توك (رخيصة)",
            "4340": "مشاهدات تيك توك (اعادة تعبئة شهر) vip fast",
        },
    },
    "Telegram": {
        "Members": {
            "5802": "اعضاء تيليجرام (15k/لليوم) (vip) (ضمان 3 شهور)",
            "6429": "اعضاء تيليجرام ثابتة (ضمان 3 شهور) (fast)",
        },
        "Reactions": {
            "6304": "تفاعل ايجابي تيليجرام + مشاهدات (vip fast)",
            "6234": "تفاعل سلبي تيليجرام + مشاهدات (vip fast)",
        },
        "Views": {
            "4746": "مشاهدات تيليجرام رخيصة",
            "6152": "مشاهدات تيليجرام عرب (vip fast)",
        },
    },
}


def calculate_sell_price(cost):
    if cost < 1:
        return round(cost + 1.5, 2)
    elif cost < 5:
        return round(cost + 2.5, 2)
    elif cost < 50:
        return round(cost + 5, 2)
    elif cost < 100:
        return round(cost + 10, 2)
    elif 150 <= cost <= 200:
        return round(cost + 20, 2)
    else:
        return round(cost + 20, 2)


def get_all_service_rates():
    try:
        response = requests.post(API_URL, data={
            "key": API_KEY,
            "action": "services"
        }, timeout=30)
        response.raise_for_status()
        data = response.json()

        rates = {}
        if isinstance(data, list):
            for item in data:
                service_id = str(item.get("service", "")).strip()
                rate = item.get("rate")
                if service_id and rate is not None:
                    try:
                        rates[service_id] = float(rate)
                    except:
                        pass
        return rates
    except:
        return {}


def get_service_info(service_id):
    rates = get_all_service_rates()
    cost = rates.get(str(service_id))
    if cost is None:
        return None, None
    sell = calculate_sell_price(cost)
    return cost, sell


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Instagram", "Facebook")
    markup.row("TikTok", "Telegram")
    return markup


def category_menu(platform):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    categories = list(SERVICES[platform].keys())
    row = []
    for cat in categories:
        row.append(cat)
        if len(row) == 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    markup.row("رجوع للرئيسية")
    return markup


def services_menu(platform, category):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    current = SERVICES[platform][category]

    for service_id, service_name in current.items():
        _, sell_price = get_service_info(service_id)
        if sell_price is not None:
            text = f"{service_id} | {service_name} | السعر: {sell_price}/1000"
        else:
            text = f"{service_id} | {service_name}"
        markup.row(text)

    markup.row("رجوع")
    markup.row("رجوع للرئيسية")
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "أهلا بيك 👋\nاختار المنصة:",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda m: m.text == "رجوع للرئيسية")
def back_to_home(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "اختار المنصة:", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text in SERVICES.keys())
def choose_platform(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"platform": message.text}
    bot.send_message(
        chat_id,
        f"اختر القسم داخل {message.text}:",
        reply_markup=category_menu(message.text)
    )


@bot.message_handler(func=lambda m: m.text == "رجوع")
def go_back(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id, {})
    platform = data.get("platform")
    if platform:
        bot.send_message(
            chat_id,
            f"اختر القسم داخل {platform}:",
            reply_markup=category_menu(platform)
        )
    else:
        bot.send_message(chat_id, "اختار المنصة:", reply_markup=main_menu())


@bot.message_handler(func=lambda m: any(m.text in SERVICES[p] for p in SERVICES))
def choose_category(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id, {})
    platform = data.get("platform")

    if not platform:
        bot.send_message(chat_id, "ابدأ بـ /start", reply_markup=main_menu())
        return

    if message.text not in SERVICES[platform]:
        return

    user_data[chat_id]["category"] = message.text

    bot.send_message(
        chat_id,
        "اختار الخدمة:",
        reply_markup=services_menu(platform, message.text)
    )


@bot.message_handler(func=lambda m: "|" in m.text and m.text.split("|")[0].strip().isdigit())
def choose_service(message):
    chat_id = message.chat.id
    data = user_data.get(chat_id, {})
    platform = data.get("platform")
    category = data.get("category")

    if not platform or not category:
        bot.send_message(chat_id, "ابدأ بـ /start", reply_markup=main_menu())
        return

    service_id = message.text.split("|")[0].strip()
    service_name = SERVICES[platform][category].get(service_id, "خدمة غير معروفة")

    cost, sell_price = get_service_info(service_id)

    user_data[chat_id]["service_id"] = service_id
    user_data[chat_id]["service_name"] = service_name
    user_data[chat_id]["cost_price"] = cost
    user_data[chat_id]["sell_price"] = sell_price
    user_data[chat_id]["step"] = "waiting_link"

    msg = f"تم اختيار:\n<b>{service_name}</b>\nID: <code>{service_id}</code>"
    if sell_price is not None:
        msg += f"\nسعر البيع لكل 1000: <b>{sell_price}</b>"

    msg += "\n\nابعت الرابط الآن:"
    bot.send_message(chat_id, msg)


@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "waiting_link")
def get_link(message):
    chat_id = message.chat.id
    user_data[chat_id]["link"] = message.text.strip()
    user_data[chat_id]["step"] = "waiting_quantity"
    bot.send_message(chat_id, "ابعت الكمية الآن:")


@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") == "waiting_quantity")
def get_quantity(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if not text.isdigit():
        bot.send_message(chat_id, "الكمية لازم تكون رقم فقط.")
        return

    quantity = int(text)
    data = user_data.get(chat_id, {})

    service_id = data["service_id"]
    service_name = data["service_name"]
    link = data["link"]
    sell_price = data.get("sell_price")

    total_price = None
    if sell_price is not None:
        total_price = round((quantity / 1000) * sell_price, 2)

    payload = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity
    }

    try:
        response = requests.post(API_URL, data=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "order" in result:
            msg = (
                f"تم تنفيذ الطلب ✅\n\n"
                f"الخدمة: <b>{service_name}</b>\n"
                f"الكمية: <b>{quantity}</b>\n"
                f"الرابط: <code>{link}</code>\n"
                f"رقم الطلب: <code>{result['order']}</code>"
            )
            if total_price is not None:
                msg += f"\nالسعر المحسوب: <b>{total_price}</b>"
            bot.send_message(chat_id, msg, reply_markup=main_menu())
        else:
            bot.send_message(chat_id, f"حصل خطأ ❌\n{result}", reply_markup=main_menu())

    except Exception as e:
        bot.send_message(chat_id, f"حصل خطأ في الاتصال ❌\n{e}", reply_markup=main_menu())

    user_data[chat_id] = {}


print("Bot is running...")
bot.infinity_polling()
