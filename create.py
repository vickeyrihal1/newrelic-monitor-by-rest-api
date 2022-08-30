#!env python

import _alerts as alerts
import _config as config

# NR URLs
api_v3_monitors = "https://synthetics.newrelic.com/synthetics/api/v3/monitors"

# prod urls
#policy_id = "123456"
uris = config.uri_list("prod-monitors.yaml")
prod_existing_alert_conditions, prod_api_v2_alert_cond_pol = alerts.existing_alert_conditions_by_id("123456")
alerts.create_monitor_alerts(uris, prod_existing_alert_conditions, prod_api_v2_alert_cond_pol)

# Start with stage urls here
