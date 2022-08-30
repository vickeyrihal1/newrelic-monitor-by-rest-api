#!env python

import _alerts as alerts

existing_monitors_name = alerts.existing_monitors_metadata()

# Delete Monitors
print("Deleting all the synthetic monitors...")
for monitor_id in list(existing_monitors_name.values()):
    print(monitor_id)
    alerts.del_monitors(monitor_id)

"""
## Normally conditions get deleted with delete of monitor.
#prod policy_id = "xxxx"
prod_alert_conditions, prod_alert_conditions_pol = alerts.existing_alert_conditions_by_id("123456")
print("Deleting alert condition for prod..")
for name in prod_alert_conditions['synthetics_conditions']:
    print(name)
    alerts.del_alert_condition(name["id"])
"""