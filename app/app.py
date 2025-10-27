# --------------------------
# 2️⃣ Process Map (Sankey Chart)
# --------------------------
st.subheader("Process Map (Activity Flow)")

# Build activity flows (from -> to) with counts
df_flows = pd.DataFrame(columns=["source","target","count"])

for case in df_events["case_id"].unique():
    case_activities = df_events[df_events["case_id"]==case]["activity"].tolist()
    for i in range(len(case_activities)-1):
        df_flows = pd.concat([df_flows, pd.DataFrame({
            "source":[case_activities[i]],
            "target":[case_activities[i+1]],
            "count":[1]
        })], ignore_index=True)

# Aggregate counts for repeated flows
df_flows = df_flows.groupby(["source","target"], as_index=False).sum()

# Create Sankey chart
all_nodes = list(set(df_flows["source"]).union(set(df_flows["target"])))
node_indices = {node:i for i,node in enumerate(all_nodes)}

import plotly.graph_objects as go

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

