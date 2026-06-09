import re
import pandas as pd

def parse_olt_output(cli_text):
    pattern = r"(\d+)/(\d+)/(\d+)\s+(\d+)\s+([\w:]+)\s+(\w+)\s+([-\d\.]+)\s+dBm"
    matches = re.findall(pattern, cli_text)

    data = []
    for m in matches:
        rx_power = float(m[6])
        status = "GOOD" if -27 <= rx_power <= -8 else "BAD"

        data.append({
            "PON": f"{m[0]}/{m[1]}/{m[2]}",
            "ONU_ID": m[3],
            "SN": m[4],
            "State": m[5],
            "Rx_Power_dBm": rx_power,
            "Status": status
        })

    return pd.DataFrame(data)

def get_summary(df):
    total = len(df)
    bad = len(df[df['Status'] == 'BAD'])
    online = len(df[df['State'] == 'online'])
    health = round((total - bad) / total * 100, 1) if total > 0 else 0
    return total, bad, online, health
