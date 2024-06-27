from cwstorm.dsl.work_node import WorkNode
import re


class Slack(WorkNode):
    """
    A Slack node is a bot that sends a notification to a Slack channel.
    """

    ORDER = 70
    ATTRS = {
        "token": {
            "type": "str",
            "default": "xoxb-000000000000",
            "validator": re.compile(r"^[xoxb-][a-zA-Z0-9-]+$"),
        },
        "channel": {
            "type": "str",
            "default": "#storm-renders",
        },
        "message": {
            "type": "str",
            "default": "Completed ${workflow-id}",
            "validator": re.compile(r"^[\s\S]*$", re.IGNORECASE),
        },
        "username": {
            "type": "str",
            "validator": re.compile(r"^[a-zA-Z0-9._-]+$"),
            "default": "storm-bot",
        },
        "icon_emoji": {
            "type": "str",
            "validator": re.compile(r"^:[a-zA-Z0-9_\-]+:$"),
            "default": ":grapes:",
        },
    }