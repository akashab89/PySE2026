# ==========================================================
# VIEWPOINT CONFIGURATION FOR BASIC ENGINEERING
# ==========================================================
BASIC_ENGINEERING_CONFIG = {
    "view_key": "be",
    "view_name": "Basic Engineering View",
    "class_default_attributes": {
        "SystemUnitClassLib/Product": "Cost",
        "SystemUnitClassLib/Process": "Cycle time",
        "SystemUnitClassLib/Resource": "Operating speed"
    },
    "edge_label_map": {
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Product"): "Part of",
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Process"): "created by",
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Resource"): "Contributed by",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Product"): "Creates",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Process"): "constraints",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Resource"): "impacted by",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Product"): "contributes to",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Process"): "impacts",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Resource"): "constraints",
    }
}

# ==========================================================
# VIEWPOINT CONFIGURATION FOR SUSTAINABILITY
# ==========================================================
SUSTAINABILITY_CONFIG = {
    "view_key": "sus",
    "view_name": "Sustainability View",
    "class_default_attributes": {
        "SystemUnitClassLib/Product": "CO2 emission per unit",
        "SystemUnitClassLib/Process": "specific energy consumption",
        "SystemUnitClassLib/Resource": "energy flow rate"
    },
    "edge_label_map": {
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Product"): "materiality",
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Process"): "influenced by",
        ("SystemUnitClassLib/Product", "SystemUnitClassLib/Resource"): "consumes from",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Product"): "Influences",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Process"): "constraints",
        ("SystemUnitClassLib/Process", "SystemUnitClassLib/Resource"): "energy flows",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Product"): "contributes to",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Process"): "material flows",
        ("SystemUnitClassLib/Resource", "SystemUnitClassLib/Resource"): "constraints",
    }
}