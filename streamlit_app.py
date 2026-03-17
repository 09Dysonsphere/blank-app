import streamlit as st

st.title("🎈 My new Streamlit app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
if "input_method" not in st.session_state:
    st.session_state.input_method = "select"
def toggle_input(toggle):
    if toggle == "select":
        st.session_state.input_method = "select"
    elif toggle == "type":
        st.session_state.input_method = "type"
#battery_input = st.toggle("toggle", False)
batteries = ["HC Valley", "SC Wuling"]
power = [1100, 3200]
battery = st.selectbox("Battery Type", batteries, on_change=toggle_input("select"))
battery_value = st.number_input("Power", 0, step=1, value=1100)
st.write(f"Power: {(power[batteries.index(battery)])}")