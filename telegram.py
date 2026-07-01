import requests

from config import BOT_TOKEN
from config import CHAT_ID


def send_message(message):

    if BOT_TOKEN is None:
        print("BOT_TOKEN Missing")
        return

    if CHAT_ID is None:
        print("CHAT_ID Missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        },
        timeout=30
    )

    print("Telegram:", response.status_code)

    print(response.text)


def send_error(error):

    send_message(

        f"""⚠️ Website Monitor Error

<code>{error}</code>
"""

    )


def send_update(name, url):

    send_message(

f"""🚨 <b>Website Updated</b>

🌐 <b>Name :</b> {name}

🔗 <b>URL :</b>

{url}

🕒 Checked Successfully
"""

    )
