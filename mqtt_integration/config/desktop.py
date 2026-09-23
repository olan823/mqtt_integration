from frappe import _


def get_data():
    return [
        {
            "module_name": "MQTT",
            "type": "module",
            "label": _("MQTT"),
            "icon": "octicon octicon-broadcast",
        }
    ]
