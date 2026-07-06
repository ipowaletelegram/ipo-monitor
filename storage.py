import json
import os

DATA_FILE = "monitor.json"


def load_data():

    if not os.path.exists(DATA_FILE):
        return {}

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def has_changed(ipo):

    """
    Returns

    changed : True/False

    old_data : previous data
    """

    db = load_data()

    company = ipo["company"]

    old = db.get(company)

    # First Time
    if old is None:

        db[company] = ipo

        save_data(db)

        return False, None

    # Compare Important Fields

    important = [

        "gmp",

        "gain",

        "issue_price",

        "lot",

        "open",

        "close",

        "listing"

    ]

    changed = False

    for field in important:

        if old.get(field) != ipo.get(field):

            changed = True

            break

    if changed:

        previous = old.copy()

        db[company] = ipo

        save_data(db)

        return True, previous

    return False, old
