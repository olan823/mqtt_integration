function ensureMqttDashboardStyle() {
	if (document.getElementById("mqtt-dashboard-page-style")) return;

	const style = document.createElement("style");
	style.id = "mqtt-dashboard-page-style";
	style.textContent = `
		.mqtt-dashboard-page {
			background: #f7f9fc;
			height: calc(100vh - 132px);
			min-height: 620px;
			overflow: hidden;
			padding: 0 !important;
		}
		.mqtt-dashboard-frame {
			border: 0;
			display: block;
			height: 100%;
			width: 100%;
		}
		.mqtt-dashboard-loading,
		.mqtt-dashboard-error {
			padding: 24px;
		}
		@media (max-width: 767px) {
			.mqtt-dashboard-page {
				height: calc(100vh - 108px);
				min-height: 520px;
			}
		}
	`;
	document.head.appendChild(style);
}

frappe.pages["mqtt-dashboard"].on_page_load = function (wrapper) {
	ensureMqttDashboardStyle();
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("MQTT Console"),
		single_column: true,
	});

	const main = wrapper.querySelector(".layout-main-section");
	main.classList.add("mqtt-dashboard-page");
	main.innerHTML = '<div class="mqtt-dashboard-loading text-muted">' + __("Loading MQTT console...") + "</div>";

	frappe.call({
		method: "mqtt_integration.api.settings.get_dashboard_settings",
	}).then((response) => {
		const dashboardUrl = response.message && response.message.dashboard_url;
		if (!dashboardUrl) {
			throw new Error("MQTT dashboard URL is not configured");
		}

		main.innerHTML = "";
		const frame = document.createElement("iframe");
		frame.className = "mqtt-dashboard-frame";
		frame.title = __("MQTT Console");
		frame.src = dashboardUrl;
		frame.allow = "clipboard-write";
		main.appendChild(frame);
	}).catch(() => {
		main.innerHTML = '<div class="mqtt-dashboard-error text-danger">' + __("Unable to load MQTT console. Check mqtt_bifromq_dashboard_url in site configuration.") + "</div>";
	});
};

frappe.pages["mqtt-dashboard"].on_page_show = function () {
	ensureMqttDashboardStyle();
};