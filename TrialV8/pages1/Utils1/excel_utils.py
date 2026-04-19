import pandas as pd
from pages1.Utils1 import config

REQUIRED_SHEETS = ["Nodes", "Edges"]
REQUIRED_NODE_COLUMNS = ["Node_ID", "Name"]
REQUIRED_EDGE_COLUMNS = ["Start Node", "End Node"]


# -----------------------------
# VALIDATION
# -----------------------------
def validate_excel(file_path):
    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")

    # Validate sheets
    missing_sheets = [s for s in REQUIRED_SHEETS if s not in xls.sheet_names]
    if missing_sheets:
        raise ValueError(
            f"Missing required sheet(s): {missing_sheets}. "
            f"Available sheets: {xls.sheet_names}"
        )

    df_nodes = pd.read_excel(xls, sheet_name="Nodes")
    df_edges = pd.read_excel(xls, sheet_name="Edges")

    # Validate node columns
    missing_node_cols = [c for c in REQUIRED_NODE_COLUMNS if c not in df_nodes.columns]
    if missing_node_cols:
        raise ValueError(
            f"Missing required column(s) in 'Nodes': {missing_node_cols}. "
            f"Available columns: {list(df_nodes.columns)}"
        )

    # Validate edge columns
    missing_edge_cols = [c for c in REQUIRED_EDGE_COLUMNS if c not in df_edges.columns]
    if missing_edge_cols:
        raise ValueError(
            f"Missing required column(s) in 'Edges': {missing_edge_cols}. "
            f"Available columns: {list(df_edges.columns)}"
        )

    return xls


# -----------------------------
# NODE MAP
# -----------------------------
def build_id_to_name_map(df_nodes):
    return {
        str(row["Node_ID"]).strip(): str(row["Name"]).strip()
        for _, row in df_nodes.iterrows()
        if pd.notna(row["Node_ID"]) and pd.notna(row["Name"])
    }

def validate_cardinality(value, row_index):
    if pd.isna(value) or value == "":
        return None

    # reject floats like 2.5 or strings like "abc"
    if isinstance(value, (int, float)) and float(value).is_integer():
        return int(value)

    # sometimes Excel gives strings
    if isinstance(value, str):
        if value.strip().isdigit():
            return int(value.strip())

    raise ValueError(
        f"Invalid Cardinality at row {row_index + 2}: '{value}'. "
        f"Must be an integer or empty."
    )

# -----------------------------
# NODES
# -----------------------------
def elements_from_excel(xls: pd.ExcelFile):
    df_nodes = pd.read_excel(xls, sheet_name="Nodes")

    elements = {}

    for _, row in df_nodes.iterrows():
        if pd.isna(row["Node_ID"]) or pd.isna(row["Name"]):
            continue

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


# -----------------------------
# LINKS
# -----------------------------
def links_from_excel(xls: pd.ExcelFile):
    df_nodes = pd.read_excel(xls, sheet_name="Nodes")
    df_edges = pd.read_excel(xls, sheet_name="Edges")

    id_to_name = build_id_to_name_map(df_nodes)

    links = []

    for idx, row in df_edges.iterrows():

        if pd.isna(row["Start Node"]) or pd.isna(row["End Node"]):
            continue

        source_id = str(row["Start Node"]).strip()
        target_id = str(row["End Node"]).strip()

        source = id_to_name.get(source_id)
        target = id_to_name.get(target_id)

        if source is None or target is None:
            continue

        # 🔴 STRICT VALIDATION HERE
        cardinality = validate_cardinality(row.get("Cardinality"), idx)

        links.append({
            "name": f"{source}_to_{target}",
            "source": source,
            "target": target,
            "type": config.edgeType_by_view["PPR View"][0],
            "cardinality": cardinality
        })

    return links


# -----------------------------
# MAIN ENTRY POINT
# -----------------------------
def parse_excel(file_path):
    """
    Full pipeline:
    - validate structure
    - extract nodes
    - extract links
    """
    xls = validate_excel(file_path)

    elements = elements_from_excel(xls)
    links = links_from_excel(xls)

    return elements, links