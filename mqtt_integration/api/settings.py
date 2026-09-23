from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import frappe
from frappe import _
from mqtt_integration import __version__


ALLOWED_ROLES = {"MQTT User", "System Manager"}
DEFAULT_CONSOLE_URL = "/assets/mqtt_integration/mqtt/index.html"


def _with_release_version(value):
    if not value:
        return ""

    parsed = urlparse(value)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["v"] = __version__
    return urlunparse(parsed._replace(query=urlencode(query)))


def _validate_broker_url(value):
    if not value:
        return ""

    parsed = urlparse(value)
    if parsed.scheme not in {"ws", "wss"} or not parsed.netloc:
        frappe.throw(_("MQTT broker WebSocket URL must use ws:// or wss://."))
    return value


def _validate_dashboard_url(value):
    if not value:
        return ""

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        frappe.throw(_("MQTT dashboard URL must use http:// or https://."))
    return value


@frappe.whitelist()
def get_console_settings():
    if not ALLOWED_ROLES.intersection(frappe.get_roles()):
        frappe.throw(_("You are not permitted to open the MQTT console."), frappe.PermissionError)

    return {
        "console_url": _with_release_version(DEFAULT_CONSOLE_URL),
        "broker_url": _validate_broker_url(
            frappe.conf.get("mqtt_broker_websocket_url", "")
        ),
    }


@frappe.whitelist()
def get_dashboard_settings():
    if not ALLOWED_ROLES.intersection(frappe.get_roles()):
        frappe.throw(_("You are not permitted to open the MQTT dashboard."), frappe.PermissionError)

    return {
        "dashboard_url": _with_release_version(
            _validate_dashboard_url(
                frappe.conf.get("mqtt_bifromq_dashboard_url", "")
            )
        )
    }
