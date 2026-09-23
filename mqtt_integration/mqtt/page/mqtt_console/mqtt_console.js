function ensureMqttConsoleStyle() {
	if (document.getElementById("mqtt-console-page-style")) return;

	const style = document.createElement("style");
	style.id = "mqtt-console-page-style";
	style.textContent = `
		.mqtt-console-page {
			background: #f7f9fc;
			height: calc(100vh - 132px);
			min-height: 620px;
			overflow: hidden;
			padding: 0 !important;
		}
		.mqtt-console-frame {
			border: 0;
			display: block;
			height: 100%;
			width: 100%;
		}
		.mqtt-console-loading,
		.mqtt-console-error {
			padding: 24px;
		}
		@media (max-width: 767px) {
			.mqtt-console-page {
				height: calc(100vh - 108px);
				min-height: 520px;
			}
		}
	`;
	document.head.appendChild(style);
}

frappe.pages["mqtt-console"].on_page_load = function (wrapper) {
	ensureMqttConsoleStyle();
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("MQTT Console"),
		single_column: true,
	});

	const main = wrapper.querySelector(".layout-main-section");
	main.classList.add("mqtt-console-page");
	main.innerHTML = '<div class="mqtt-console-loading text-muted">' + __("Loading MQTT console...") + "</div>";

	frappe.call({
		method: "mqtt_integration.api.settings.get_console_settings",
	}).then((response) => {
		const settings = response.message || {};
		const consoleUrl = new URL(settings.console_url, window.location.origin);
		if (settings.broker_url) {
			consoleUrl.searchParams.set("broker_url", settings.broker_url);
		}

		main.innerHTML = "";
		const frame = document.createElement("iframe");
		frame.className = "mqtt-console-frame";
		frame.title = __("MQTT Console");
		frame.src = consoleUrl.toString();
		frame.allow = "clipboard-write";
		main.appendChild(frame);
	}).catch(() => {
		main.innerHTML = '<div class="mqtt-console-error text-danger">' + __("Unable to load MQTT console settings.") + "</div>";
	});
};

frappe.pages["mqtt-console"].on_page_show = function () {
	ensureMqttConsoleStyle();
};
