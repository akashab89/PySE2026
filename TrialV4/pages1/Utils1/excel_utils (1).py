import pandas as pd
from pages1.Utils1 import config


def build_id_to_name_map(file_path: str):  #mapping IDs to node names
    df_nodes = pd.read_excel(file_path, sheet_name="Nodes")

    return {
        str(row["Node_ID"]).strip(): str(row["Name"]).strip()
        for _, row in df_nodes.iterrows()
        if pd.notna(row["Node_ID"]) and pd.notna(row["Name"])
    }

def elements_from_excel(file_path: str):
    df_nodes = pd.read_excel(file_path, sheet_name="Nodes")

    elements = {}

    for _, row in df_nodes.iterrows():
        node_id = str(row["Node_ID"]).strip()
        name = str(row["Name"]).strip()
        ppr_type = row.get("PPR_Type")

        attributes = []

        for col in df_nodes.columns:
            if col not in ["Node_ID", "Name", "PPR_Type"]:
                value = row.get(col)
                if pd.notna(value):
                    attributes.append({
                        "attr_name": col,
                        "data_type": None,
                        "value": str(value)
                    })

        # IMPORTANT: use NAME as graph key
        elements[name] = {
            "name": name,
            "id": node_id,
            "class": ppr_type,
            "xml": None,
            "port_id": None,
            "parent": None,
            "attributes": attributes
        }

    return elements

def links_from_excel(file_path: str):
    df_edges = pd.read_excel(file_path, sheet_name="Edges")
    id_to_name = build_id_to_name_map(file_path)

    links = []

    for _, row in df_edges.iterrows():
        source_id = str(row["Start Node"]).strip()
        target_id = str(row["End Node"]).strip()

        # convert IDs → names
        source = id_to_name.get(source_id)
        target = id_to_name.get(target_id)

        if source is None or target is None:
            continue  # skip invalid rows

        cardinality = row.get("Cardinality")

        links.append({
            "name": f"{source}_to_{target}",
            "source": source,
            "target": target,
            "type": config.edgeType_by_view["PPR View"][0],
            "cardinality": int(cardinality) if pd.notna(cardinality) else None
        })

    return links