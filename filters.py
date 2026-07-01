import re

IGNORE_WORDS = [

    "cookie",

    "cookies",

    "privacy",

    "privacy policy",

    "terms",

    "copyright",

    "all rights reserved",

    "advertisement",

    "advertising",

    "subscribe",

    "sign in",

    "login",

    "accept",

    "reject",

    "menu"

]


def remove_ignore_words(text):

    text = text.lower()

    for word in IGNORE_WORDS:

        text = text.replace(word.lower(), "")

    return text


def remove_extra_spaces(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_numbers(text):

    return re.sub(r"\d+", "", text)


def clean_text(text):

    text = remove_ignore_words(text)

    text = remove_extra_spaces(text)

    return text
