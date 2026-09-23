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

Configure the browser-reachable SCD BifroMQ dashboard URL. This must point to
the `bifromq-dashboard.html` served by SCD. When ERPNext uses HTTPS, this URL
must also use HTTPS so the browser does not block the iframe as mixed content.
The dashboard must stay on the SCD origin because it calls relative
`/api/bifromq/*` endpoints.

```bash
bench --site erp.skychip.top set-config \
  mqtt_bifromq_dashboard_url \
  'https://tchart.skychip.top/static/bifromq-dashboard.html'
```

Do not configure the production HTTPS ERPNext site with the direct
`http://tchart.skychip.top:8710/...` URL. Browsers block that iframe as mixed
content. The HTTPS reverse proxy must forward both `/static/` and
`/api/bifromq/` to SCD so the dashboard's relative API requests stay on the
same origin.

The MQTT client source is maintained by SCD at
`http://tchart.skychip.top:8710/static/index.html`. Copy that file into
`mqtt_integration/public/mqtt/index.html` before each MQTT integration release.
The packaged copy is served from:

```text
/assets/mqtt_integration/mqtt/index.html
```

Both iframe URLs receive the package version as a `v` query parameter so a new
immutable release does not reuse the previous HTML from browser caches.

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

The MQTT Workspace contains two entries:

- `MQTT 客户端`: the browser MQTT publish/subscribe client.
- `MQTT 控制台`: the SCD BifroMQ operations dashboard.
