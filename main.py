from config import URLS

from utils import (
    download,
    clean_text,
    get_hash,
    check_change,
)

from telegram import (
    send_message,
    send_update,
    send_error,
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

            print("✅ CHANGE DETECTED")

            send_update(name, url)

        else:

            print("✅ No Change")

    except Exception as e:

        print(f"❌ ERROR : {e}")

        send_error(f"{name}\n\n{str(e)}")


def startup_message():

    try:

        send_message(
            """🚀 <b>Universal Website Monitor Started</b>

✅ GitHub Actions Running

Monitoring all configured websites...
"""
        )

    except Exception as e:

        print(e)


def summary(total, changed, failed):

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Websites : {total}")
    print(f"Changed        : {changed}")
    print(f"Failed         : {failed}")
    print("=" * 60)


def main():

    print("=" * 60)
    print("UNIVERSAL WEBSITE MONITOR")
    print("=" * 60)

    startup_message()

    total = 0
    changed = 0
    failed = 0

    for site in URLS:

        total += 1

        try:

            name = site["name"]
            url = site["url"]

            html = download(url)

            text = clean_text(html)

            new_hash = get_hash(text)

            if check_change(name, new_hash):

                changed += 1

                send_update(name, url)
                print("Old Hash Changed")

                print(f"🔔 {name} Updated")

            else:

                print(f"✔ {name} No Change")

        except Exception as e:

            failed += 1

            print(e)

            send_error(f"{site.get('name')}\n\n{e}")

    summary(total, changed, failed)


if __name__ == "__main__":

    main()
