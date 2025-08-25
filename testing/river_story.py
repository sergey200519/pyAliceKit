from pyAliceKit.utils.dialogs import include_nodes


river_story = include_nodes({
    "message": "river_start",
    "buttons": ["$river_choices"],
    "childs": {
        "boat": {
            "message": "river_boat",
            "end_dialog": True
        },
        "bridge": {
            "message": "river_bridge",
            "buttons": ["$cave_choices"],
            "childs": {
                "enter": {
                    "message": "river_cave",
                    "end_dialog": True
                },
                "skip": {
                    "message": "Ты прошёл мимо пещеры и ушёл далеко. Конец.",
                    "end_dialog": True
                }
            }
        }
    }
}, True)
