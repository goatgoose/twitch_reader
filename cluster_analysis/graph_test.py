import numpy as np
import pandas as pd
from cluster_analysis.graph import UndirectedGraph, WeightedEdge, Node

RUN = "run2"

data = pd.read_csv(f"../{RUN}/hopped.csv")
data.columns = [
    "user",
    "hopped_from",
    "hopped_to",
    "content",
    "badge_info",
    "badges",
    "emotes",
    "flags",
    "id",
    "is_mod",
    "room_id",
    "is_subscriber",
    "tmi_sent_ts",
    "is_turbo",
    "user_type",
    "is_emote_only",
    "bits",
    "sent_ts",
    "timestamp",
    "messages_in_from",
    "vader_neg",
    "vader_neu",
    "vader_pos",
    "vader_compound",
    "toxicity"
]

graph = UndirectedGraph()

for channel in data["hopped_from"]:
    graph.add_node(Node(channel))
for channel in data["hopped_to"]:
    graph.add_node(Node(channel))

hopped_counts = data["hopped_from"].value_counts()

for index, row in data.iterrows():
    hopped_from = row["hopped_from"]
    hopped_to = row["hopped_to"]

    weight = 1 / hopped_counts[hopped_from]

    if hopped_to not in graph[hopped_from].edges:
        graph.add_edge(WeightedEdge([hopped_from, hopped_to], 0))
    graph[hopped_from].edges[hopped_to].weight += weight

kst = graph.k_spanning_tree(10)
print(kst)
