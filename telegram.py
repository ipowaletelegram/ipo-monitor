import requests
from datetime import datetime

from config import BOT_TOKEN, CHAT_ID

API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_message(message):

    requests.post(
        API,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=30,
    )


def send_gmp_update(new, old=None):

    now = datetime.now().strftime("%d %b %Y %I:%M %p")

    company = new["company"]
    issue = new["issue_price"]
    gmp = new["gmp"]
    gain = new["gain"]
    lot = new["lot"]
    open_date = new["open"]
    close_date = new["close"]
    listing = new["listing"]

    # Decide Increase / Decrease
    title = "🆕 New IPO GMP"

    if old:

        try:

            old_gmp = float(old["gmp"])
            new_gmp = float(gmp)

            if new_gmp > old_gmp:

                title = "🟢 GMP Increased"

            elif new_gmp < old_gmp:

                title = "🔴 GMP Decreased"

            else:

                title = "🔄 IPO Updated"

        except:

            pass

    message = f"""
<b>{title}</b>

🏢 <b>{company}</b>

💰 <b>Issue Price</b>
₹{issue}

📈 <b>Current GMP</b>
₹{gmp} ({gain})

📦 <b>Lot Size</b>
{lot}

📅 <b>Open</b>
{open_date}

📅 <b>Close</b>
{close_date}

🚀 <b>Listing</b>
{listing}

━━━━━━━━━━━━━━━━━━

📢 <b>BE.IPOWale</b>

🕒 <code>{now}</code>
"""

    send_message(message)
