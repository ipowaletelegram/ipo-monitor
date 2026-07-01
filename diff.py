import difflib


def get_changes(old_text, new_text):

    old_lines = old_text.splitlines()

    new_lines = new_text.splitlines()

    diff = difflib.unified_diff(

        old_lines,

        new_lines,

        lineterm=""

    )

    added = []

    removed = []

    for line in diff:

        if line.startswith("+++"):

            continue

        if line.startswith("---"):

            continue

        if line.startswith("@@"):

            continue

        if line.startswith("+"):

            added.append(line[1:])

        elif line.startswith("-"):

            removed.append(line[1:])

    return added, removed


def format_changes(added, removed):

    msg = ""

    if added:

        msg += "🟢 Added\n\n"

        for item in added[:10]:

            if item.strip():

                msg += f"+ {item}\n"

        msg += "\n"

    if removed:

        msg += "🔴 Removed\n\n"

        for item in removed[:10]:

            if item.strip():

                msg += f"- {item}\n"

    if msg == "":

        msg = "Minor Change Detected"

    return msg
