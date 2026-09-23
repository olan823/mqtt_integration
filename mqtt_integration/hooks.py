app_name = "mqtt_integration"
app_title = "MQTT Integration"
app_publisher = "Skychip"
app_description = "ERPNext Desk entry point for the Starchart MQTT web console"
app_email = ""
app_license = "MIT"
app_logo_url = "/assets/mqtt_integration/images/mqtt.svg"
app_home = "/app/mqtt"

add_to_apps_screen = [
	{
		"name": app_name,
		"logo": app_logo_url,
		"title": "MQTT",
		"route": app_home,
	}
]

after_install = "mqtt_integration.install.after_install"
after_migrate = "mqtt_integration.install.ensure_workspace"
after_uninstall = "mqtt_integration.install.after_uninstall"
