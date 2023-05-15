# ==== IMPORTS ====

import slash_commands.settings as settings

# ================

closeby_hp_view = {
            "type": "modal",
            # View identifier
            "callback_id": "closeby-window",
            "title": {"type": "plain_text", "text": "Heat pump density"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "How many heat pumps are close-by?",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "postcode",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action",
                    },
                    "label": {"type": "plain_text", "text": "Postcode", "emoji": True},
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "proptype",
                    "element": {
                        "type": "radio_buttons",
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Any",
                                    "emoji": True,
                                },
                                "value": "any",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Detached Houses",
                                    "emoji": True,
                                },
                                "value": "detached",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Semi-detached Houses",
                                    "emoji": True,
                                },
                                "value": "semidetached",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Flats",
                                    "emoji": True,
                                },
                                "value": "flat",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Terraced Houses",
                                    "emoji": True,
                                },
                                "value": "terraced",
                            },
                        ],
                        "action_id": "radio_buttons-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Property Type",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "dist",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Radius in km",
                        "emoji": True,
                    },
                },
            ],
        }

def prepare_reminder_view(date):
    """Prepare the reminder view for the pop-up window.

    Args:
        date (datetime.date or str): Default date, usually next Thursday.

    Returns:
        str: Full view for pop-up window.
    """

    reminder_view =   {
            "type": "modal",
            # View identifier
            "callback_id": "send_reminder",
            "title": {"type": "plain_text", "text": "Project Status Reminder"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "user_sel",
                    "element": {
                        "type": "multi_users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select users",
                            "emoji": True,
                        },
                        "action_id": "multi_users_select-action",
                        "initial_users": settings.default_members,
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Pick whom to message",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "This is the default message. Change below if you need to.",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "block_id": "text_sel",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action",
                        "initial_value": settings.asana_reminder_text,
                        "placeholder": {
                            "type": "plain_text",
                            "text": settings.asana_preview_text,
                            "emoji": True,
                        },
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Change message here",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "date_sel",
                    "element": {
                        "type": "datepicker",
                        "initial_date": str(date),
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True,
                        },
                        "action_id": "datepicker-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select date",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "time_sel",
                    "element": {
                        "type": "timepicker",
                        "initial_time": settings.asana_reminder_time,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select time",
                            "emoji": True,
                        },
                        "action_id": "timepicker-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select time",
                        "emoji": True,
                    },
                },
            ],
        }

    return reminder_view


def prepare_britishfy_view(today):
    """Prepare the britishfy view for the pop-up window.

    Args:
        today (datetime.date or str): Today's date.

    Returns:
        str: Full view for pop-up window.
    """

    britishfy_view={
            "type": "modal",
            # View identifier
            "callback_id": "britishfy_view",
            "title": {"type": "plain_text", "text": "British-fy Your Message"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "British-fy Your Message",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "block_id": "who",
                    "text": {"type": "mrkdwn", "text": "Who are you writing to?"},
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True,
                        },
                        "action_id": "users_select-action",
                    },
                },
                {
                    "type": "input",
                    "block_id": "todo",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Tasks you need them to do (one by per line)",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "date",
                    "element": {
                        "type": "datepicker",
                        "initial_date": str(today),
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True,
                        },
                        "action_id": "datepicker-action",
                    },
                    "label": {"type": "plain_text", "text": "By when", "emoji": True},
                },
                {
                    "type": "input",
                    "block_id": "mypart",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "What I'll be doing",
                        "emoji": True,
                    },
                },
            ],
        }


    return britishfy_view