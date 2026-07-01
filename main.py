from config import URLS

from utils import download
from utils import clean_text
from utils import get_hash
from utils import check_change

from telegram import send_message
from telegram import send_update
from telegram import send_error


def check_website(site):

    name = site["name"]

    url = site["url"]

    print("=" * 60)
    print("Checking :", name)
    print(url)

    try:

        html = download(url)

        text = clean_text(html)

        new_hash = get_hash(text)

        changed = check_change(name, new_hash)

        if changed:

            print("CHANGE DETECTED")

            send_update(name, url)

        else:

            print("No Change")

    except Exception as e:

        print("ERROR :", e)

        send_error(f"{name}\n\n{e}")


def startup_message():

    try:

        send_message(

"""✅ <b>Universal Website Monitor Started</b>

Monitoring Started Successfully.

GitHub Actions : Running

Ready to Detect Website Changes.
"""
        )

    except Exception as e:

        print(e)


def main():

    print()

    print("=" * 60)
    print("Universal Website Monitor")
    print("=" * 60)

    startup_message()

    for site in URLS:

        check_website(site)

    print()

    print("=" * 60)
    print("Finished")
    print("=" * 60)


if __name__ == "__main__":

    main()
