# ==== IMPORTS =====

import os

from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

from datetime import datetime

from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import slash_commands.settings as settings, utils
from slash_commands import jokes, hp_density, britishfy, views

from asf_core_data.getters import data_getters

# ==== SETUP =====

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Initalize web client
client = WebClient(token=os.environ["SLACK_TOKEN"])

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET"),
)

# Load data
hp_data = data_getters.load_data(
    bucket_name="asf-exploration",
    data_path="S3",
    file_path=settings.hp_data_file,
    usecols=settings.hp_data_columns,
)

# ==== REACTIONS =====
# Listen and react to specific message
# As of May 2023, this will only work for public channels in the Nesta workspace because of permission restrictions.


@app.message(r"fridge\sin\sreverse")
def fridge(client, message):
    """Give an alternative to the 'fridge in reverse' metaphor
    for heat pumps.
    Note: this will only work in public channels due to permission restrictions
    """

    channel_id = message["channel"]
    text = message["text"]
    ts = message["ts"]

    client.chat_postMessage(
        channel=channel_id,
        thread_ts=ts,
        text=f"Time to retire this old metaphor. A heat pump is anyway more similar to the <https://medium.com/all-you-can-heat/7-reasons-why-a-heat-pump-is-like-the-atlantic-bluefin-tuna-c2028e43600a|Atlantic Blue Fin Tuna>. :fish:",
    )


@app.message("tell me a joke")
def tell_joke(client, message):
    """Tell a joke.
    Note: this will only work in public channels due to permission restrictions."""

    channel_id = message["channel"]
    joke = jokes.get_a_joke(settings.joke_default_topic) + settings.fun_emoji
    client.chat_postMessage(channel=channel_id, text=joke)


@app.message(":wave:")
def say_hello(message, say):
    """Say hi to someone who waves.
    Note: this will only work in public channels due to permission restrictions."""

    user = message["user"]
    ts = message["ts"]
    say(f"Hi there, <@{user}>!", thread_ts=ts)


# ==== SLASH COMMANDS =====
# Specific commands executed via /

# add code to load a joke from a joke database or website


@app.command("/tell-me-a-joke")
def tell_me_a_joke(ack, respond, command):
    """Slash command to tell a joke. You can also pass a topic.
    Command: /tell-me-a-joke [topic]
    """

    ack()
    channel = command["channel_id"]

    # For direct messages, send DM to user instead of posting in channel.
    if command["channel_name"] == "directmessage":
        channel = command["user_id"]

    topic = command["text"] if command["text"] != "" else settings.joke_default_topic
    joke = jokes.get_a_joke(topic)

    if joke is None:

        joke_not_found_text = "I don't know any jokes about such obscure topics. :face_with_spiral_eyes: Here is one about cats:\n"
        joke = jokes.get_a_joke("cat")
        joke = joke_not_found_text + joke + settings.fun_emoji

    else:
        joke += settings.fun_emoji

    client.chat_postMessage(channel=channel, text=joke)


@app.command("/project-status-reminder")
def asana_reminder(ack, respond, command):
    """Slash command to schedule project status reminder.
    Command: /project-status-reminder"""

    ack()
    thursday = utils.find_date_for_next_weekday(settings.asana_reminder_day)

    channel = command["user_id"]
    global reminder_sender_channel  # to make it accessible for other function as arguments cannot be passed
    reminder_sender_channel = channel

    client.views_open(
        trigger_id=command["trigger_id"], view=views.prepare_reminder_view(thursday)
    )


@app.view("send_reminder")
def reminder_submission(ack, body, client, view, logger):
    ack()

    vals = view["state"]["values"]

    selected_users = vals["user_sel"]["multi_users_select-action"]["selected_users"]
    selected_text = vals["text_sel"]["plain_text_input-action"]["value"]
    selected_date = vals["date_sel"]["datepicker-action"]["selected_date"]
    selected_time = vals["time_sel"]["timepicker-action"]["selected_time"]

    # Generate timestamp
    timestamp = utils.get_timestamp(selected_date, selected_time)

    # Schedule messages
    for user in selected_users:

        client.chat_scheduleMessage(
            channel=user,
            text=selected_text,
            post_at=timestamp,
        )

    # Create log message
    recipients = [utils.get_user_name(client, id) for id in selected_users]
    recipients_text = ", ".join(recipients)

    log_text = f"You have successfully scheduled a project update reminder to be sent out on {selected_date} at {selected_time} to the following people: {recipients_text}."

    client.chat_postMessage(channel=reminder_sender_channel, text=log_text)


@app.command("/closeby-hps")
def get_closeby_hp_count(ack, respond, command):
    """Slash command to compute closeby heat pumps, meaning within a 10km radius.
    Command: /closeby-hps"""

    ack()

    postcode = command["text"]
    channel = command["channel_id"]

    # For direct messages, send DM to user instead of posting in channel.
    if command["channel_name"] == "directmessage":
        channel = command["user_id"]

    postcode = postcode.strip().upper()

    closeby_hp_count = hp_density.get_n_hp_closeby(
        hp_data, postcode, property_type=None, max_dist=10
    )

    if closeby_hp_count is None:
        text = "Sorry, we couldn't find the coordinates for this postcode... :face_with_peeking_eye:"
    else:
        text = f"There are {closeby_hp_count} heat pumps within a 10km radius of your postcode {postcode}."

    client.chat_postMessage(channel=channel, text=text)


@app.command("/closeby-hps-picker")
def closeby_hp_selection(ack, respond, command):
    """Slash command to compute closeby heat pumps.
    Pick postcode, property type and radius in pop-up window.
    Command: /closeby-hps-picker"""

    ack()
    channel = command["channel_id"]

    # For direct messages, send DM to user instead of posting in channel.
    if command["channel_name"] == "directmessage":
        channel = command["user_id"]

    global hp_selection_channel
    hp_selection_channel = channel

    client.views_open(
        trigger_id=command["trigger_id"],
        view=views.closeby_hp_view,
    )


@app.view("closeby-window")
def hp_count_submission(ack, body, client, view, logger):

    ack()

    postcode = view["state"]["values"]["postcode"]["plain_text_input-action"]["value"]
    prop_type = view["state"]["values"]["proptype"]["radio_buttons-action"][
        "selected_option"
    ]["text"]["text"]
    dist = view["state"]["values"]["dist"]["plain_text_input-action"]["value"]

    if prop_type == "Any":
        prop_type = None

    closeby_hp_count = hp_density.get_n_hp_closeby(
        hp_data, postcode.strip().upper(), property_type=prop_type, max_dist=int(dist)
    )

    prop_type_string = " in {}".format(prop_type) if prop_type is not None else ""
    postcode_string = postcode.upper()

    if closeby_hp_count is None:
        text = "Sorry, we couldn't find the coordinates for this postcode... :face_with_peeking_eye:"
    else:
        text = f"There are {closeby_hp_count} heat pumps{prop_type_string} within a {dist}km radius of postcode {postcode_string.upper()}."

    client.chat_postMessage(channel=hp_selection_channel, text=text)


@app.command("/britishfy")
def britishfy_message(ack, respond, command):
    """Slash command generate British-fied message to colleague.
    Pick tasks, date and recipient in pop-up window.
    Command: /britishfy"""

    today = datetime.today().strftime("%Y-%m-%d")
    ack()

    client.views_open(
        trigger_id=command["trigger_id"], view=views.prepare_britishfy_view(today)
    )


@app.view("britishfy_view")
def britishfy_submission(ack, body, client, view, logger):

    ack()

    who = view["state"]["values"]["who"]["users_select-action"]["selected_user"]
    other_to_do = view["state"]["values"]["todo"]["plain_text_input-action"]["value"]
    by_when = view["state"]["values"]["date"]["datepicker-action"]["selected_date"]
    my_part = view["state"]["values"]["mypart"]["plain_text_input-action"]["value"]
    user = body["user"]["id"]

    recipient_name = utils.get_first_name(client, who)

    errors = {}
    if other_to_do is not None and len(other_to_do) <= 3:
        errors["todo"] = "The value must be longer than 3 characters"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return

    britishfied = britishfy.britishfy(recipient_name, other_to_do, by_when, my_part)

    # Message the user (not final recipient)
    client.chat_postMessage(channel=user, text=britishfied)


# ==== RUN APP =====

# Start socket handler
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("APP_LEVEL_TOKEN"))
    handler.start()
