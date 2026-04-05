global_nodes_list = ["Product", "Process", "Resource"] 

edgeType_by_view= {
    "PPR View": ["PPR_port"],
    "Engineering View": ["part_of", "contributes_to", "impacts", "constraints"],
    "Sustainability View": ["energy_flows", "material_flows", "influences"]
}

# PPR View Attributes
PPR_ATTRS = {
    "Product": {
        "color": {"type": list, "options": ["Red", "Blue", "Green", "Black", "Yellow"]},
        "size": {"type": list, "options": ["Small", "Medium", "Big"]}
    },
    "Process": {},
    "Resource": {}
}

# Engineering View Attributes
ENG_ATTRS = {
    "Product": {
        "product_cost": {"type": float, "unit": "Euro"}
    },
    "Process": {
        "cycle_time": {"type": float, "unit": "seconds"}
    },
    "Resource": {
        "operating_speed": {"type": float, "unit": "Units/min"},
        "operating_cost": {"type": float, "unit": "Euro"}
    }
}

# Sustainability View Attributes
SUST_ATTRS = {
    "Product": {
        "durability": {"type": int, "unit": "years"},
        "co2_per_unit": {"type": float, "unit": "kg/unit"}
    },
    "Process": {
        "specific_energy_consumption": {"type": float, "unit": "KW/unit"},
        "co2_emission": {"type": float, "unit": "kg/hr"}
    },
    "Resource": {
        "energy_flow_rate": {"type": float, "unit": "KW/hr"}
    }
}

VIEW_ATTRS_MAPPING = {
    "PPR View": PPR_ATTRS,
    "Engineering View": ENG_ATTRS,
    "Sustainability View": SUST_ATTRS
}