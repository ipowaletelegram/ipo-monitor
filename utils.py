import hashlib
import json
import os
import re

import requests

from bs4 import BeautifulSoup

from config import HEADERS
from config import DATA_FILE
from config import IGNORE_WORDS
from config import TIMEOUT


def download(url):

    session = requests.Session()

    response = session.get(

        url,

        headers=HEADERS,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.text


def clean_text(html):

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    text = text.lower()

    for word in IGNORE_WORDS:

        text = text.replace(word.lower(), "")

    text = re.sub(r"\s+", " ", text)

    return text


def get_hash(text):

    return hashlib.sha256(

        text.encode()

    ).hexdigest()


def load_hashes():

    if not os.path.exists(DATA_FILE):

        return {}

    with open(DATA_FILE, "r") as f:

        return json.load(f)


def save_hashes(data):

    with open(DATA_FILE, "w") as f:

        json.dump(

            data,

            f,

            indent=4

        )


def check_change(name, new_hash):

    hashes = load_hashes()

    old_hash = hashes.get(name)

    if old_hash is None:

        hashes[name] = new_hash

        save_hashes(hashes)

        return False

    if old_hash != new_hash:

        hashes[name] = new_hash

        save_hashes(hashes)

        return True

    return False
