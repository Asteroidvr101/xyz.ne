from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pytz

web_app = Flask(__name__)

display_items = [
    "ItemAlpha",
    "ItemBeta",
    "ItemGamma",
    "ItemDelta",
    "ItemEpsilon",
    "ItemZeta",
]

@web_app.route("/api/DailyRotationData", methods=["POST"])
def get_daily_rotation():
    if request.method != "POST":
        return "", 405

    target_timezone = pytz.timezone('America/Chicago')
    switch_hour = 18

    current_utc_time = datetime.utcnow()

    current_local_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone(target_timezone)

    today_switch_time = current_local_time.replace(hour=switch_hour, minute=0, second=0, microsecond=0)

    if current_local_time < today_switch_time:
        period_start_time_local = today_switch_time - timedelta(days=1)
    else:
        period_start_time_local = today_switch_time

    period_end_time_local = period_start_time_local + timedelta(days=1)

    period_start_time_utc = period_start_time_local.astimezone(pytz.utc)
    period_end_time_utc = period_end_time_local.astimezone(pytz.utc)

    start_timestamp_str = period_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_timestamp_str = period_end_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    epoch_date = datetime(2000, 1, 1).date()
    days_since_epoch = (period_start_time_local.date() - epoch_date).days
    item_selection_index = days_since_epoch % len(display_items)
    current_display_item = display_items[item_selection_index]

    response_payload = {
        "DailyItems": [
            {
                "StandIdentifier": "CosmeticStandAlpha",
                "DisplayedItem": current_display_item,
                "ActiveFromUTC": start_timestamp_str,
                "ActiveUntilUTC": end_timestamp_str
            },
            {
                "StandIdentifier": "MainPedestal",
                "DisplayedItem": current_display_item,
                "ActiveFromUTC": start_timestamp_str,
                "ActiveUntilUTC": end_timestamp_str
            },
            {
                "StandIdentifier": "CosmeticStandBeta",
                "DisplayedItem": current_display_item,
                "ActiveFromUTC": start_timestamp_str,
                "ActiveUntilUTC": end_timestamp_str
            },
            {
                "StandIdentifier": "CosmeticStandGamma",
                "DisplayedItem": current_display_item,
                "ActiveFromUTC": start_timestamp_str,
                "ActiveUntilUTC": end_timestamp_str
            },
        ],
    }

    return jsonify(response_payload)

if __name__ == "__main__":
    web_app.run(debug=True, port=5001)
