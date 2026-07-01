from config import URLS

from utils import (
    download,
    clean_text,
    get_hash,
    check_change,
)

from telegram import (
    send_update,
    send_error,
    send_message,
)


def check_website(site):

    name = site.get("name")
    url = site.get("url")
    mode = site.get("mode", "text")

    print("=" * 60)
    print(f"Checking : {name}")
    print(f"URL      : {url}")
    print(f"Mode     : {mode}")

    try:

        html = download(url)

        text = clean_text(html)

        new_hash = get_hash(text)

        changed = check_change(name, new_hash)

        if changed:

            print(f"🔔 {name} Updated")

            send_update(name, url)

            return True

        else:

            print(f"✅ {name} No Change")

            return False

    except Exception as e:

        print(f"❌ ERROR : {e}")

        send_error(f"{name}\n\n{e}")

        return None


def send_summary(total, changed, failed):

    try:

        message = f"""
📊 <b>Website Monitor Summary</b>

🌐 Total Checked : <b>{total}</b>

🔔 Updated : <b>{changed}</b>

❌ Failed : <b>{failed}</b>
"""

        send_message(message)

    except Exception as e:

        print(e)


def main():

    print("=" * 60)
    print("UNIVERSAL WEBSITE MONITOR")
    print("=" * 60)

    total = 0
    changed = 0
    failed = 0

    for site in URLS:

        total += 1

        result = check_website(site)

        if result is True:

            changed += 1

        elif result is None:

            failed += 1

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total   : {total}")
    print(f"Updated : {changed}")
    print(f"Failed  : {failed}")
    print("=" * 60)

    # Summary sirf tab bhejo jab kuch update ya error ho
    if changed > 0 or failed > 0:

        send_summary(total, changed, failed)


if __name__ == "__main__":

    main()
