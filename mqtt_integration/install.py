import json

import frappe


APP_NAME = "mqtt_integration"
APP_HOME = "/app/mqtt"
APP_LOGO_URL = "/assets/mqtt_integration/images/mqtt.svg"
MODULE_NAME = "MQTT"
PAGE_NAME = "mqtt-console"
ROLE_NAME = "MQTT User"
WORKSPACE_NAME = "MQTT"


def after_install():
    ensure_role()
    ensure_module_def()
    ensure_workspace()


def after_uninstall():
    if frappe.db.exists("Workspace", WORKSPACE_NAME):
        frappe.delete_doc("Workspace", WORKSPACE_NAME, force=True, ignore_permissions=True)


def ensure_role():
    if not frappe.db.exists("Role", ROLE_NAME):
        frappe.get_doc({"doctype": "Role", "role_name": ROLE_NAME}).insert(
            ignore_permissions=True
        )


def ensure_module_def():
    if not frappe.db.exists("Module Def", MODULE_NAME):
        frappe.get_doc(
            {
                "doctype": "Module Def",
                "module_name": MODULE_NAME,
                "app_name": APP_NAME,
            }
        ).insert(ignore_permissions=True)


def ensure_workspace():
    ensure_role()
    ensure_module_def()
    ensure_desktop_icon()

    workspace = (
        frappe.get_doc("Workspace", WORKSPACE_NAME)
        if frappe.db.exists("Workspace", WORKSPACE_NAME)
        else frappe.new_doc("Workspace")
    )
    workspace.update(
        {
            "label": WORKSPACE_NAME,
            "title": WORKSPACE_NAME,
            "module": MODULE_NAME,
            "icon": "network",
            "public": 1,
            "is_hidden": 0,
            "content": json.dumps(
                [
                    {
                        "id": "mqtt-console-shortcut",
                        "type": "shortcut",
                        "data": {"shortcut_name": "MQTT 控制台", "col": 4},
                    }
                ]
            ),
            "shortcuts": [
                {"label": "MQTT 控制台", "type": "Page", "link_to": PAGE_NAME}
            ],
            "roles": [{"role": ROLE_NAME}, {"role": "System Manager"}],
        }
    )

    if workspace.is_new():
        workspace.insert(ignore_permissions=True)
    else:
        workspace.save(ignore_permissions=True)

    ensure_custom_workspace_shortcut()
    frappe.clear_cache(doctype="Workspace")


def ensure_custom_workspace_shortcut():
    customization_name = frappe.db.exists("Custom Workspace", {"workspace": WORKSPACE_NAME})
    if not customization_name:
        return

    customization = frappe.get_doc("Custom Workspace", customization_name)
    if not customization.content:
        return

    content = frappe.parse_json(customization.content)
    if any(
        block.get("type") == "shortcut"
        and block.get("data", {}).get("shortcut_name") == "MQTT 控制台"
        for block in content
    ):
        return

    content.insert(
        0,
        {
            "id": "mqtt-console-shortcut",
            "type": "shortcut",
            "data": {"shortcut_name": "MQTT 控制台", "col": 4},
        },
    )
    customization.content = json.dumps(content)
    customization.save(ignore_permissions=True)


def ensure_desktop_icon():
    app_icon_names = frappe.get_all(
        "Desktop Icon",
        filters={"app": APP_NAME, "icon_type": "App"},
        pluck="name",
        order_by="creation asc",
    )
    matching_icon_names = frappe.get_all(
        "Desktop Icon",
        filters={"label": WORKSPACE_NAME},
        pluck="name",
        order_by="creation asc",
    )
    icon_name = app_icon_names[0] if app_icon_names else None
    icon_name = icon_name or (matching_icon_names[0] if matching_icon_names else None)

    for duplicate_name in dict.fromkeys([*app_icon_names, *matching_icon_names]):
        if duplicate_name != icon_name:
            frappe.delete_doc("Desktop Icon", duplicate_name, force=True, ignore_permissions=True)

    icon = frappe.get_doc("Desktop Icon", icon_name) if icon_name else frappe.new_doc("Desktop Icon")
    icon.update(
        {
            "label": WORKSPACE_NAME,
            "link_type": "External",
            "link_to": None,
            "icon_type": "App",
            "app": APP_NAME,
            "link": APP_HOME,
            "logo_url": APP_LOGO_URL,
        }
    )

    if icon.is_new():
        icon.insert(ignore_permissions=True)
    else:
        icon.save(ignore_permissions=True)

    frappe.cache.delete_key("desktop_icons")
    frappe.cache.delete_key("bootinfo")
