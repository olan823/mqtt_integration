# MQTT Integration

`mqtt_integration` adds the existing Starchart MQTT web console to ERPNext Desk.
The console remains a static browser application; this app only supplies the
ERPNext role, Workspace, Desk Page, packaged asset, and runtime broker URL.

## Site Configuration

Configure the browser-reachable MQTT over WebSocket endpoint. Production
ERPNext uses HTTPS, so this endpoint must normally use `wss://`.

```bash
bench --site erp.skychip.top set-config \
  mqtt_broker_websocket_url 'wss://mqtt.example.com/mqtt'
```

The packaged console asset is served from:

```text
/assets/mqtt_integration/mqtt/index.html
```

## Local Validation

```bash
python -m compileall mqtt_integration
node --check mqtt_integration/mqtt/page/mqtt_console/mqtt_console.js
```

## Installation

```bash
bench --site erp.skychip.top install-app mqtt_integration
bench --site erp.skychip.top migrate
bench --site erp.skychip.top clear-cache
```

Assign `MQTT User` to users who need the console. `System Manager` also has
access.
