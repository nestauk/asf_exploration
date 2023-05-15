# ==== IMPORTS ====

import random
import datetime

# ================

def britishfy(who, to_dos, by_when, my_part):
    """Britishfy a message.

    Args:
        who (str): Recipient.
        to_dos (list): To does.
        by_when (datetime.date): Date by when task(s) should be completed.
        my_part (str): What sender will do in the meantime.

    Returns:
        str: Full britishfied message.
    """

    phrases = [
        "it would be tremendously helpful if you could {}.",
        "I would really appreciate it if you could spare some time to {}.",
        "if it's not too much trouble, it would be fantastic if you could {}.",
        "could I kindly ask you to {}?",
        "would it possible for you to {}?",
        "could you do me a huge favour and {}?",
        "I would be very grateful if you could {}.",
    ]

    connectors = ["Furthermore,", "Also,", "In addition,", "Besides,"]

    requests = []
    for i, to_do in enumerate(to_dos.strip().split("\n")):
 
        if i > 0:
            phrase = random.choice(phrases).format(to_do)
            requests.append(random.choice(connectors))
            requests.append(phrase)

        else:
            phrase = random.choice(phrases).format(to_do)
            phrase = phrase[0].upper() + phrase[1:]
            requests.append(phrase)

    requests = " ".join(requests)

    today = datetime.datetime.today().date()
    date_request = datetime.datetime.strptime(by_when, "%Y-%m-%d").date()

    urgent_dict = {
        0: "I know it's much to ask, but could you try to have a look today?",
        1: "Do you think you'll have time for this tomorrow?",
        2: "Is this something that could be done within the next 2 days?",
        3: "Could you look at this by the end of the week?",
        4: "Would you have time for this sometime next week?",
    }
    time = (date_request - today).days

    if time > 4:
        urgency_level = "It's really not that urgent."
    else:
        if time == -1:
            time = 0
        urgency_level = urgent_dict[time]

    if my_part is not None and my_part.strip() != "":
        my_parts = my_part.strip().split("\n")
        tasks = " and ".join(my_parts)
        meantime = "\n\nIn the meantime, I will {}.".format(tasks)

    ending = "\n\nThank you so much! I wish you a lovely day!"

    msg = f"Hi {who},\nHow are you? I hope you're having a wonderful week.\n\n{requests} {urgency_level} :pray: {meantime} {ending}"

    return msg
