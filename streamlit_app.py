import streamlit as st
import pandas as pd
import math

title = st.container(horizontal=True, vertical_alignment="center")
title.image("images/16.png", width=70)
title.title(" My new Streamlit app🎈")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

st.logo("images/300px-Endfield_Industries.webp")

if "power" not in st.session_state:
    st.session_state.power = 1100

#battery values
batteries = ["HC Valley", "SC Wuling"]
power_list = [1100, 3200]

#choose battery
battery_input = st.toggle("enter manually", False)
if battery_input == False:
    try:
        battery = st.selectbox("Battery Type", batteries, index = power_list.index(st.session_state.power))
    except ValueError:
        battery = st.selectbox("Battery Type", batteries, index = 0)
else:
    battery_manual = st.number_input("Power", 0, step=1, value=st.session_state.power)


#selected power value
st.session_state.power = power_list[batteries.index(battery)] if battery_input == False else battery_manual
power = st.session_state.power
st.write(f"Power: {power}")

#more input
battery_freq = st.number_input("Frequency", value=40, step=1)
req_power = st.number_input("Required Power", value = 1000, step = 1)
full_batt = st.number_input(f"full batteries (rec: {math.floor((req_power-200)/power)})", 0, step = 1)

#splits
depth = st.number_input("Splits", value=5, step = 0, width=130)

splits_select = st.container(horizontal=True, gap="large")

splits_info = splits_select.container()
splits = splits_info.segmented_control("orange", range(depth+1), selection_mode="multi")


#table
time = [battery_freq * 2**x for x in range(depth+1)]
avg_power = [power * (40/battery_freq) / 2**x for x in range(depth+1)]
table = pd.DataFrame({"time":time, "avg power":avg_power})
table.index.name = "splits"
power_table = splits_select.table(table, width="content")

#infomation
remain_power = req_power - (full_batt * power) - sum([avg_power[x] for x in splits])
splits_info.write(f"remaining power req: {remain_power}")
distances = [abs(remain_power - avg_power[x]) for x in range(depth+1)]
splits_info.write(f"closest: {distances.index(min(distances))}")

#auto splits
splits_info.space("xxsmall")
margin = splits_info.number_input("margin of error", 0, value = 100, width=120)
auto_split = splits_info.button("recommend splits")

if auto_split:
    rec_split = []
    temp_remain = remain_power
    while True:
        if len(rec_split) > 0:
            temp_remain = req_power - sum([avg_power[x] for x in rec_split])
        dist = [temp_remain - avg_power[x] for x in range(depth+1)]
        abs_dist = [abs(dist[x]) for x in range(depth+1)]
        close = [abs_dist.index(min(abs_dist)), min(abs_dist)]
        if close[0] in rec_split:
            rec_split.append(close[0])
            break
        if dist[close[0]] <= 0: 
            if close[1] <= margin:
                rec_split.append(close[0])
                break
            elif close[0] + 1 <= depth:
                rec_split.append(close[0] + 1)
                continue
            else:
                rec_split.append(close[0] + 1)
                break
        else:
            if close[1] <= margin:
                if abs_dist[close[0] - 1] <= margin:
                    rec_split.append(close[0] - 1)
                    break
                else:
                    rec_split.append(close[0])
                    continue
            else:
                rec_split.append(close[0])
                continue
    
    splits_info.write(f"{rec_split}")

#downtime
if len(splits) > 0:
    lcm = time[max(splits)]
    uptime = [(0, 40)]
    for split in splits:
        for i in range(1, int(lcm / time[split])):
            uptime.append((time[split] * i, time[split] * i + 40))
    uptime.sort(key = lambda x:x[0])
    uptime.append((lcm, lcm))

    downtimes = []
    for i in range(len(uptime) - 1):
        downtimes.append(uptime[i+1][0] - uptime[i][1])

    st.write(f"drain : {max(downtimes) * ((full_batt * power) + 200 - req_power)}")
    st.write(f"downtime : {max(downtimes)}")