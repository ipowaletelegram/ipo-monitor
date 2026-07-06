from config import URLS
from utils import download

from parser import parse_investorgain
from storage import has_changed
from telegram import send_gmp_update


def main():

    print("=" * 60)
    print("BE.IPOWale GMP Monitor")
    print("=" * 60)

    total = 0
    changed = 0

    for site in URLS:

        if "InvestorGain" not in site["name"]:
        continue
        try:

            html = download(site["url"])

            ipos = parse_investorgain(html)

            print(f"Found {len(ipos)} IPOs")

            total += len(ipos)

            for ipo in ipos:

                is_changed, old = has_changed(ipo)

                if is_changed:

                    changed += 1

                    print(f"Updated : {ipo['company']}")

                    send_gmp_update(ipo, old)

        except Exception as e:

            print(e)

    print("=" * 60)
    print(f"Total IPOs : {total}")
    print(f"Changed    : {changed}")
    print("=" * 60)


if __name__ == "__main__":

    main()
