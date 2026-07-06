import requests
from datetime import datetime

from config import BOT_TOKEN, CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_message(message):

    if not BOT_TOKEN:
        print("❌ BOT_TOKEN Missing")
        return False

    if not CHAT_ID:
        print("❌ CHAT_ID Missing")
        return False

    try:

        response = requests.post(
            TELEGRAM_API,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if result.get("ok"):
            print("✅ Telegram Message Sent")
            return True

        print(result)
        return False

    except Exception as e:

        print("Telegram Error :", e)

        return False


def send_startup():

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    message = f"""
🚀 <b>Universal Website Monitor Started</b>

✅ Status : Running

🕒 Started :
<code>{now}</code>

🤖 GitHub Actions Ready
"""

    send_message(message)


def send_update(name, url):

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    message = f"""
🚨 <b>Website Updated</b>

🌐 <b>Website :</b>
<code>{name}</code>

🔗 <b>URL :</b>
{url}

🕒 <b>Detected :</b>
<code>{now}</code>

━━━━━━━━━━━━━━━━━━━━
"""

    send_message(message)


def send_error(error):

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    message = f"""
⚠️ <b>Website Monitor Error</b>

🕒
<code>{now}</code>

<code>{error}</code>
"""

    send_message(message)


def send_test():

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    message = f"""
🧪 <b>Telegram Test Successful</b>

Everything is working correctly.

🕒
<code>{now}</code>
"""

    send_message(message)


def send_custom(title, body):

    message = f"""
<b>{title}</b>

{body}
"""

    send_message(message)
