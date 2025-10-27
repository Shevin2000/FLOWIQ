# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------
# Page Setup
# --------------------------
st.set_page_config(page_title="FLOWIQ Prototype Dashboard", layout="wide")
st.title("FLOWIQ Prototype Dashboard")
st.markdown("Hybrid AI framework: Process Mining → ML Prediction → Optimization")

# --------------------------
# 1️⃣ Sample Event Log (More Data)
# --------------------------
st.subheader("Event Log (Sample Data)")

event_data = {
    "case_id": [1,1,1,2,2,2,3,3,3,3,4,4,4,5,5,5,5,6,6,6],
    "activity": [
        "A","B","C",
        "A","C","D",
        "A","B","B","C",
        "B","C","D",
        "A","B","C","D",
        "C","B","D"
    ],
    "timestamp": pd.to_datetime([
        "2025-10-01 08:00","2025-10-01 10:00","2025-10-01 12:00",
        "2025-10-01 09:00","2025-10-01 12:00","2025-10-01 15:00",
        "2025-10-01 07:30","2025-10-01 08:30","2025-10-01 09:30","2025-10-01 11:00",
        "2025-10-01 08:00","2025-10-01 09:00","2025-10-01 11:00",
        "2025-10-01 07:00","2025-10-01 08:00","2025-10-01 09:30","2025-10-01 11:30",
        "2025-10-01 08:00","2025-10-01 09:00","2025-10-01 10:30"
    ]),
    "resource": ["R1","R2","R3","R1","R3","R2","R2","R2","R1","R3",
                 "R1","R3","R2","R2","R1","R2","R3","R3","R2","R1"]
}

df_events = pd.DataFrame(event_data)
st.dataframe(df_events)

# --------------------------
# 2️⃣ Process Map (Sankey Chart)
# --------------------------
st.subheader("Process Map (Activity Flow)")

# Build activity flows (source -> target) with counts
df_flows = pd.DataFrame(columns=["source","target","count"])
for case in df_events["case_id"].unique():
    case_activities = df_events[df_events["case_id"]==case]["activity"].tolist()
    for i in range(len(case_activities)-1):
        df_flows = pd.concat([df_flows, pd.DataFrame({
            "source":[case_activities[i]],
            "target":[case_activities[i+1]],
            "count":[1]
        })], ignore_index=True)

# Aggregate repeated flows
df_flows = df_flows.groupby(["source","target"], as_index=False).sum()
df_flows["count"] = pd.to_numeric(df_flows["count"])
total_flows = df_flows["count"].sum()
df_flows["percentage"] = (df_flows["count"] / total_flows * 100).round(1)

all_nodes = list(set(df_flows["source"]).union(set(df_flows["target"])))
node_indices = {node:i for i,node in enumerate(all_nodes)}

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes,
        color="skyblue"
    ),
    link=dict(
        source=[node_indices[s] for s in df_flows["source"]],
        target=[node_indices[t] for t in df_flows["target"]],
        value=df_flows["count"],
        label=[f"{c} times ({p}%)" for c,p in zip(df_flows["count"], df_flows["percentage"])]
    )
)])
fig_sankey.update_layout(title_text="Sample Process Flow Map", font_size=12)

# --------------------------
# 2️⃣ Process Map (Gantt-style Timeline)
# --------------------------
st.subheader("Process Timeline (Gantt-style)")

# Prepare start and end times per activity per case
df_events_sorted = df_events.sort_values(by=["case_id", "timestamp"])
df_events_sorted["start_time"] = df_events_sorted["timestamp"]
df_events_sorted["end_time"] = df_events_sorted.groupby("case_id")["timestamp"].shift(-1)
df_events_sorted["end_time"].fillna(df_events_sorted["start_time"] + pd.Timedelta(hours=1), inplace=True)

fig_gantt = px.timeline(
    df_events_sorted,
    x_start="start_time",
    x_end="end_time",
    y="case_id",
    color="activity",
    text="resource"
)
fig_gantt.update_yaxes(autorange="reversed")
fig_gantt.update_layout(title_text="Process Timeline per Case", font_size=12)

# --------------------------
# Display both charts side by side
# --------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_sankey, use_container_width=True)
with col2:
    st.plotly_chart(fig_gantt, use_container_width=True)

# --------------------------
# 3️⃣ Mock ML Predictions
# --------------------------
st.subheader("Predicted Remaining Time (hours)")

predictions = pd.DataFrame({
    "case_id": [1,2,3,4,5,6],
    "predicted_remaining_time": [2, 3, 1.5, 2.5, 3, 1]
})
st.dataframe(predictions)

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
    "case_id": [3,1,4,2,5,6],
    "priority": [1,2,3,4,5,6],
    "assigned_resource": ["R2","R1","R3","R1","R2","R3"]
})
st.dataframe(optimization)

# --------------------------
# 5️⃣ Baseline Comparison (FIFO)
# --------------------------
st.subheader("Baseline (FIFO) vs Optimized Priority")

baseline = pd.DataFrame({
    "case_id": [1,2,3,4,5,6],
    "baseline_priority": [1,2,3,4,5,6]
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
