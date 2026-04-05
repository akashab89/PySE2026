import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
from yfiles_graphs_for_streamlit import NodeStyle, NodeShape
import xml.etree.ElementTree as ET
import networkx as nx

def nx_to_yfiles_graph(nx_graph,node_cardinality_mapping=None):
    nodes = []
    edges = []

    # ---- Nodes ----
    for node_id, attrs in nx_graph.nodes(data=True):
        parent = attrs.get("parent", None)
        attributes = attrs.get("attributes", [])
        base_label= attrs.get("name",str(node_id))

        #Append cardinality to label if exists
        card= node_cardinality_mapping.get(node_id)
        label=f"{base_label}\n({card}x)" if card else base_label
        # Start with parent
        properties = {
            "parent": parent,
            "class": attrs.get("node_class",""),
            "label": label
        }

        # Flatten attributes list into properties
        for attr in attributes:
            attr_name = attr.get("attr_name")
            value = attr.get("value")

            if attr_name:
                properties[attr_name] = value

        nodes.append({
            "id": str(node_id),
            "properties": properties
        })

    # ---- Edges ----
    for source, target, attrs in nx_graph.edges(data=True):
        cardinality = attrs.get("cardinal", None)

        edges.append({
            "id": f"{source}-{target}",
            "start": str(source),
            "end": str(target),
            "cardinality": cardinality
        })

    return nodes, edges
def class_to_shape(node):
    props = node.get("properties", {})
    node_class = props.get("class", "")

    if node_class == "SystemUnitClassLib/Process":
        return NodeStyle(shape=NodeShape.RECTANGLE)

    elif node_class == "SystemUnitClassLib/Product":
        return NodeStyle(shape=NodeShape.ELLIPSE,color="red")

    elif node_class == "SystemUnitClassLib/Resource":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE,color="green")

    else:
        return NodeStyle(shape=NodeShape.HEXAGON)

tree= ET.parse("lego_car_ppr.aml")
root= tree.getroot()
ns = {"caex": "http://www.dke.de/CAEX"}

def build_elements_dict(root, ns):
    elements = {}   # ✅ local dictionary

    def extract_elements(elem, parent_name=None):
        elem_name = elem.get("Name")
        elem_id = elem.get("ID")
        elem_class= elem.get("RefBaseSystemUnitPath")

        ppr_iface = elem.find("caex:ExternalInterface[@Name='PPR_port']", ns)
        port_id = ppr_iface.get("ID") if ppr_iface is not None else None
        ppr_attrs = []
        for attr in elem.findall("caex:Attribute", ns):
            value_elem= attr.find("caex:Value",ns)
            value = value_elem.text.strip() if value_elem is not None and value_elem.text else None
            ppr_attrs.append({
                "attr_name": attr.get("Name"),
                "data_type": attr.get("AttributeDataType"),
                "value": value
                })

        elements[elem_name] = {
            "name": elem_name,
            "id": elem_id,
            "class": elem_class,
            "xml": elem,
            "port_id": port_id,
            "parent": parent_name,
            "attributes": ppr_attrs
        }

        for child in elem.findall("caex:InternalElement", ns):
            extract_elements(child, elem_name)

    # Start recursion
    for top_elem in root.findall(".//caex:InstanceHierarchy/caex:InternalElement", ns):
        extract_elements(top_elem)

    return elements

elements = build_elements_dict(root, ns)

link_list=[]
for elem in root.findall(".//caex:InternalElement",ns):
    for il in elem.findall("caex:InternalLink",ns):
        il_name = il.get("Name")
        il_source = il.get("RefPartnerSideA")
        il_target = il.get("RefPartnerSideB")
        cardinality = None
        for attr in il.findall("caex:Attribute", ns):
            if attr.get("Name")== "cardinality":
                cardinality = attr.get("Value")
        link_list.append({"name": il_name, "source": il_source, "target": il_target, "cardinality": cardinality})

iface_mapping_dict = {}
for elem in root.findall(".//caex:InternalElement", ns):
    elem_id = elem.get("ID")
    for iface in elem.findall(".//caex:ExternalInterface", ns):
        iface_id = iface.get("ID")
        iface_mapping_dict[iface_id] = elem_id

G=nx.DiGraph()

for elem in elements.values():
    G.add_node(
        elem["id"], 
        name=elem["name"],
        node_class=elem["class"],  # Renamed 'class' to 'node_class' to avoid Python errors
        xml=elem["xml"],
        port_id=elem["port_id"],
        parent=elem["parent"],
        attributes=elem["attributes"]
    )


for il in link_list:
    actual_source= iface_mapping_dict[il["source"]]
    actual_target=iface_mapping_dict[il["target"]]
    G.add_edge(actual_source, actual_target,label=il["name"],cardinal=il["cardinality"])
node_cardinality_mapping = {}
for u,v,data in G.edges(data=True):
    card= data.get("cardinal", "")
    if card:
        try:
            node_cardinality_mapping[u] = int(card)
        except:
            pass
st.write("Node Cardinality Mapping:", node_cardinality_mapping)
nodes, edges = nx_to_yfiles_graph(G,node_cardinality_mapping)




graph = StreamlitGraphWidget()
graph = StreamlitGraphWidget(nodes=nodes, edges=edges, directed_mapping= "True", node_styles_mapping=class_to_shape)
graph.node_size_mapping = lambda node: (
    (90, 40) if node.get("properties", {}).get("parent") is not None else (120, 60)
)
with st.container():
    st.subheader("PPR Diagram of Lego Car")
    graph.show(graph_layout=Layout.HIERARCHIC)
