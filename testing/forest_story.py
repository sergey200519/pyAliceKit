from typing import Any

from pyAliceKit.utils.dialogs import include_nodes


forest_story = include_nodes({
    "message": "forest_start",
    "buttons": ["$forest_choices"],
    "keywords": ["forest", "лес"],
    "childs": {
        "fight": {
            "message": "forest_fight",
            "buttons": ["$hut_choices"],
            "childs": {
                "hut": {
                    "message": "forest_clearing",
                    "buttons": ["$hut_choices"],
                    "childs": {
                        "enter": {
                            "message": "forest_hut_inside",
                            "end_dialog": True
                        },
                        "skip": {
                            "message": "forest_continue",
                            "transitions": ["/river"]
                        }
                    }
                }
            }
        },
        "talk": {
            "message": "forest_talk",
            "buttons": ["$hut_choices"],
            "childs": {
                "hut": {
                    "message": "forest_clearing",
                    "buttons": ["$hut_choices"],
                    "childs": {
                        "enter": {
                            "message": "forest_hut_inside",
                            "end_dialog": True
                        },
                        "skip": {
                            "message": "forest_continue",
                            "transitions": ["/river"]
                        }
                    }
                }
            }
        }
    }
}, True)