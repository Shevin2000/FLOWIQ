# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FLOWIQ Prototype Dashboard", layout="wide")
st.title("FLOWIQ Prototype Dashboard")
st.markdown("Hybrid AI framework: Process Mining → ML Prediction → Optimization")

# --------------------------
# 1️⃣ Sample Event Log
# --------------------------
st.subheader("Event Log (Sample Data)")

event_data = {
    "case_id": [1,1,1,2,2,3,3,3,3],
    "activity": ["A","B","C","A","C","A","B","B","C"],
    "timestamp": pd.to_datetime([
        "2025-10-01 08:00", "2025-10-01 10:00", "2025-10-01 12:00",
        "2025-10-01 09:00", "2025-10-01 12:00",
        "2025-10-01 07:30", "2025-10-01 08:30", "2025-10-01 09:30", "2025-10-01 11:00"
    ]),
    "resource": ["R1","R2","R3","R1","R3","R2","R2","R1","R3"]
}

df_events = pd.DataFrame(event_data)
st.dataframe(df_events)

# --------------------------
# 2️⃣ Process Map (Gantt Chart)
# --------------------------
st.subheader("Process Map (Gantt Chart)")

fig_gantt = px.timeline(
    df_events,
    x_start="timestamp",
    x_end="timestamp",
    y="case_id",
    color="activity",
    text="resource"
)
fig_gantt.update_yaxes(autorange="reversed")
st.plotly_chart(fig_gantt, use_container_width=True)

# --------------------------
# 3️⃣ Mock ML Predictions
# --------------------------
st.subheader("Predicted Remaining Time (hours)")

predictions = pd.DataFrame({
    "case_id": [1,2,3],
    "predicted_remaining_time": [2, 3, 1.5]
})
st.dataframe(predictions)

# Bar chart for predictions
fig_pred = px.bar(
    predictions,
    x="case_id",
    y="predicted_remaining_time",
    text="predicted_remaining_time",
    labels={"predicted_remaining_time": "Hours"}
)
st.plotly_chart(fig_pred, use_container_width=True)

# --------------------------
# 4️⃣ Mock Optimization Results
# --------------------------
st.subheader("Optimized Schedule / Resource Allocation")

optimization = pd.DataFrame({
    "case_id": [3,1,2],
    "priority": [1,2,3],
    "assigned_resource": ["R2","R1","R3"]
})
st.dataframe(optimization)

# --------------------------
# 5️⃣ Baseline Comparison (FIFO)
# --------------------------
st.subheader("Baseline (FIFO) vs Optimized Priority")

baseline = pd.DataFrame({
    "case_id": [1,2,3],
    "baseline_priority": [1,2,3]
})
comparison = baseline.merge(optimization, on="case_id")
st.dataframe(comparison)

st.markdown("✅ Lower priority number = higher scheduling priority in optimized plan")

# --------------------------
# 6️⃣ Summary Metrics
# --------------------------
st.subheader("Summary Metrics")

metrics = pd.DataFrame({
    "Metric": ["Average Predicted Time", "Max Predicted Time", "Min Predicted Time"],
    "Value": [predictions["predicted_remaining_time"].mean(),
              predictions["predicted_remaining_time"].max(),
              predictions["predicted_remaining_time"].min()]
})
st.dataframe(metrics)
