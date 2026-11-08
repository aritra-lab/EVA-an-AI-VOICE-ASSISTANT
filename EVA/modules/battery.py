import psutil

def battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery information is unavailable."
    percent = battery.percent
    if percent <= 20 and not battery.power_plugged:
        return f"Warning. Battery is only {percent} percent. Please connect the charger."
    elif battery.power_plugged:
        reply=f"Battery is {percent} percent and charging."
        return reply
    
    else:
        reply = f"BATTERY IS AT {percent} PERCENT AND THE CHARGER IS NOT CONNECTED."
        return reply