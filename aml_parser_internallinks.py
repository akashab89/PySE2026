import xml.etree.ElementTree as ET
import streamlit as st

ET.register_namespace('',"http://www.dke.de/CAEX")

def link_exists(source_elem_xml, source_port_id, target_port_id):
    for link in source_elem_xml.findall(".//caex:InternalLink", ns):
        if (
            link.get("RefPartnerSideA") == source_port_id and
            link.get("RefPartnerSideB") == target_port_id
        ):
            return True
    return False

tree= ET.parse("lego_car_trial.aml")
root= tree.getroot()
ns = {"caex": "http://www.dke.de/CAEX"} # need to wirte a function to get this for any

elements={}
for elem in root.findall(".//caex:InternalElement", ns):
    elem_name = elem.get("Name")
    elem_id = elem.get("ID")

    ports = []
    for iface in elem.findall("caex:ExternalInterface", ns):
        ports.append({
            "name": iface.get("Name"),
            "id": iface.get("ID")
        })

    elements[elem_name] = {
        "id": elem_id,
        "xml": elem,
        "ports": ports
    }

VIEW_CONFIG = {
    "PPR View": ["PPR_port"],
    "Engineering View": ["part_of", "contributes_to", "impacts", "constraints"],
    "Sustainability View": ["energy_flows", "material_flows", "influences"]
}

view_mode = st.radio(
    "Select Linking View",
    list(VIEW_CONFIG.keys())
)

allowed_ports = VIEW_CONFIG[view_mode]

st.info(f"Active View: {view_mode}")


filtered_elements = {}
for elem_name, elem_data in elements.items():
    valid_ports = [
        p for p in elem_data["ports"]
        if p["name"] in allowed_ports
    ]
    
    if valid_ports:
        filtered_elements[elem_name] = valid_ports

st.header("Create Internal Links")
source_elem_name = st.selectbox(
    "Select Source Element",
    list(filtered_elements.keys())
)
source_ports = filtered_elements[source_elem_name]

source_port = st.selectbox(
    "Select Source Port",
    source_ports,
    format_func=lambda x: f"{x['name']} ({x['id']})"
)
#st.write(source_port)
#st.write(elements[source_elem_name]["xml"])
selected_port_type = source_port["name"]
#st.write(selected_port_type)
valid_target_elements = {}

for elem_name, elem_data in elements.items():
    matching_ports = [
        p for p in elem_data["ports"]
        if p["name"] == selected_port_type
    ]
    if matching_ports:
        valid_target_elements[elem_name] = matching_ports

target_elem_name = st.selectbox(
    "Select Target Element",
    list(valid_target_elements.keys())
)

target_ports = valid_target_elements[target_elem_name]

target_port = st.selectbox(
    "Select Target Port",
    target_ports,
    index=None,
    format_func=lambda x: f"{x['name']} ({x['id']})"
)

if st.button("Create Internal Link"):
    source_elem_xml = elements[source_elem_name]["xml"]
    # 🔍 Check for duplicate
    if link_exists(source_elem_xml, source_port["id"], target_port["id"]):
        st.warning("⚠️ This internal link already exists!")
    else:
        new_link = ET.Element("InternalLink")
        new_link.set("RefPartnerSideA", source_port["id"])
        new_link.set("RefPartnerSideB", target_port["id"])
        new_link.set("Name", f"{view_mode}_{source_elem_name}_to_{target_elem_name}")

        source_elem_xml.append(new_link)
        ET.indent(tree, space="  ", level=0)
        tree.write("lego_car_trial.aml", encoding="utf-8")

st.write(elements["Plastic"])

st.header(" Show links according to viewpoints")
view_mode_1 = st.radio(
    "Select Linking View",
    list(VIEW_CONFIG.keys()),
    key="view_mode2"
)
st.info(f"Active View: {view_mode_1}")

allowed_ports_1 = VIEW_CONFIG[view_mode_1]

port_map = {}

for elem_name, elem_data in elements.items():
    for port in elem_data["ports"]:
        port_map[port["id"]] = {
            "element": elem_name,
            "port_name": port["name"]
        }
selected_element_1 = st.selectbox(
    "Select Element",
    list(elements.keys()),
    key="inspect_element"
)

all_links = root.findall(".//caex:InternalLink", ns)

all_links = root.findall(".//caex:InternalLink", ns)

element_links = []

for link in all_links:
    a = link.get("RefPartnerSideA")  # source port
    b = link.get("RefPartnerSideB")  # target port

    if a in port_map and b in port_map:
        source_info = port_map[a]
        target_info = port_map[b]

        # ✅ condition 1: selected element is SOURCE
        if source_info["element"] == selected_element_1:

            # ✅ condition 2: matches viewpoint
            if source_info["port_name"] in allowed_ports_1:
                
                element_links.append({
                    "target": target_info["element"],
                    "port": source_info["port_name"],
                    "name": link.get("Name")
                })


st.subheader(f"{view_mode} - Internal Links for{selected_element_1}")

if element_links:
    for link in element_links:
        st.write(
            f"{selected_element_1} → {link['target']} "
            f"(via {link['port']})"
        )
else:
    st.info("No outgoing links in this view.")

