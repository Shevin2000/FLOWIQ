# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="FLOWIQ Prototype Dashboard", layout="wide")
st.title("FLOWIQ Prototype Dashboard")
st.markdown("Hybrid AI framework: Process Mining → ML Prediction → Optimization")

# --------------------------
# 1️⃣ Sample Event Log (Realistic Data)
# --------------------------
st.subheader("Event Log (Sample Data)")

# Define activities
activities = ["Receive Order", "Check Inventory", "Process Payment", "Pack Items", "Ship Items", "Close Case"]
resources = ["Alice", "Bob", "Charlie", "David"]

# Create sample cases
np.random.seed(42)
cases = []
for case_id in range(1, 13):  # 12 cases
    start_time = pd.Timestamp("2025-10-01 08:00") + pd.Timedelta(hours=np.random.randint(0, 5))
    for i, activity in enumerate(activities):
        duration = pd.Timedelta(hours=np.random.randint(1, 4))
        cases.append({
            "case_id": case_id,
            "activity": activity,
            "start_time": start_time,
            "end_time": start_time + duration,
            "resource": np.random.choice(resources)
        })
        start_time += duration

df_events = pd.DataFrame(cases)
st.dataframe(df_events)

# --------------------------
# 2️⃣ Process Map (Sankey Chart)
# --------------------------
st.subheader("Process Map (Activity Flow)")

# Build activity flows
df_flows = pd.DataFrame(columns=["source", "target", "count"])
for case in df_events["case_id"].unique():
    case_activities = df_events[df_events["case_id"] == case]["activity"].tolist()
    for i in range(len(case_activities) - 1):
        df_flows = pd.concat([df_flows, pd.DataFrame({
            "source": [case_activities[i]],
            "target": [case_activities[i + 1]],
            "count": [1]
        })], ignore_index=True)

# Aggregate repeated flows
df_flows = df_flows.groupby(["source", "target"], as_index=False).sum()

# Sankey nodes
all_nodes = list(set(df_flows["source"]).union(set(df_flows["target"])))
node_indices = {node: i for i, node in enumerate(all_nodes)}

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
        value=df_flows["count"]
    )
)])
fig_sankey.update_layout(title_text="Sample Process Flow Map", font_size=12)
st.plotly_chart(fig_sankey, use_container_width=True)

# --------------------------
# 3️⃣ Gantt Chart (Timeline)
# --------------------------
st.subheader("Process Timeline (Gantt Chart)")
fig_gantt = px.timeline(
    df_events,
    x_start="start_time",
    x_end="end_time",
    y="case_id",
    color="activity",
    text="resource",
)
fig_gantt.update_yaxes(autorange="reversed")
st.plotly_chart(fig_gantt, use_container_width=True)

# --------------------------
# 4️⃣ Mock ML Predictions
# --------------------------
st.subheader("Predicted Remaining Time (hours)")
predictions = pd.DataFrame({
    "case_id": df_events["case_id"].unique(),
    "predicted_remaining_time": np.random.uniform(1, 5, size=df_events["case_id"].nunique()).round(1)
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
# 5️⃣ Mock Optimization Results
# --------------------------
st.subheader("Optimized Schedule / Resource Allocation")
optimization = pd.DataFrame({
    "case_id": df_events["case_id"].unique(),
    "priority": np.random.permutation(df_events["case_id"].nunique()) + 1,
    "assigned_resource": np.random.choice(resources, df_events["case_id"].nunique())
})
st.dataframe(optimization)

# --------------------------
# 6️⃣ Baseline Comparison (FIFO)
# --------------------------
st.subheader("Baseline (FIFO) vs Optimized Priority")
baseline = pd.DataFrame({
    "case_id": df_events["case_id"].unique(),
    "baseline_priority": range(1, df_events["case_id"].nunique() + 1)
})
comparison = baseline.merge(optimization, on="case_id")
st.dataframe(comparison)
st.markdown("✅ Lower priority number = higher scheduling priority in optimized plan")

# --------------------------
# 7️⃣ Summary Metrics
# --------------------------
st.subheader("Summary Metrics")
metrics = pd.DataFrame({
    "Metric": ["Average Predicted Time", "Max Predicted Time", "Min Predicted Time"],
    "Value": [predictions["predicted_remaining_time"].mean(),
              predictions["predicted_remaining_time"].max(),
              predictions["predicted_remaining_time"].min()]
})
st.dataframe(metrics)
