from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pytz

# Make sure the Flask app instance name matches the one used in the route decorators
app = Flask(__name__)

# List of items to cycle through
display_items = [
    "ItemAlpha",
    "ItemBeta",
    "ItemGamma",
    "ItemDelta",
    "ItemEpsilon",
    "ItemZeta",
]

# Use the correct app instance name in the route decorator
@app.route("/api/DailyRotationData", methods=["POST"])
def get_daily_rotation():
    if request.method != "POST":
        return "", 405 # Using 405 Method Not Allowed for non-POST requests

    # Configure the target time and timezone for the switch
    target_timezone = pytz.timezone('America/Chicago')
    switch_hour = 18 # 6 PM

    # Get the current time in UTC
    current_utc_time = datetime.utcnow()

    # Convert current UTC time to the target timezone
    current_local_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone(target_timezone)

    # Determine the exact switch point for today
    today_switch_time = current_local_time.replace(hour=switch_hour, minute=0, second=0, microsecond=0)

    # Calculate the start time for the current display period
    if current_local_time < today_switch_time:
        # If before the switch time, the period started yesterday at the switch hour
        period_start_time_local = today_switch_time - timedelta(days=1)
    else:
        # If at or after the switch time, the period started today at the switch hour
        period_start_time_local = today_switch_time

    # Calculate the end time for the current display period (24 hours after the start)
    period_end_time_local = period_start_time_local + timedelta(days=1)

    # Convert the local period times back to UTC for the API response
    period_start_time_utc = period_start_time_local.astimezone(pytz.utc)
    period_end_time_utc = period_end_time_local.astimezone(pytz.utc)

    # Format the times into the required string format
    start_timestamp_str = period_start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    end_timestamp_str = period_end_time_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # Determine which item to display based on the start date of the period
    # Using a fixed epoch to ensure consistent daily indexing
    epoch_date = datetime(2000, 1, 1).date()
    days_since_epoch = (period_start_time_local.date() - epoch_date).days
    item_selection_index = days_since_epoch % len(display_items)
    current_display_item = display_items[item_selection_index]

    # Structure the response data
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
            # Add more stand entries as needed
        ],
    }

    return jsonify(response_payload)

# Remove or comment out the __main__ block for Vercel deployment
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)
