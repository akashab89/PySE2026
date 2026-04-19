from pages1.Utils1 import config
def build_elements_dict(root, ns):
    elements = {}   # ✅ local dictionary

    def extract_elements(elem, parent_name=None):
        elem_name = elem.get("Name")
        elem_id = elem.get("ID")
        elem_class= elem.get("RefBaseSystemUnitPath")
        elem_class = elem_class.split("/")[-1] if elem_class else None

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

def extract_links(root, ns):
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
    return link_list

def iface_mapping(root, ns):
    iface_mapping_dict = {}
    #Assuming that the PPR model has only PPR ports as external interfaces.
    # If there are other types of interfaces, additional filtering logic may be needed here to only include PPR ports in the mapping.
    for elem in root.findall(".//caex:InternalElement", ns):
        elem_id = elem.get("Name")

        for iface in elem.findall(".//caex:ExternalInterface", ns):
            iface_id = iface.get("ID")
            iface_mapping_dict[iface_id] = elem_id

    return iface_mapping_dict



def extract_ppr_links(link_list:list, iface_mapping_dict:dict):
    ppr_links = []
    for link in link_list:
        source_iface_id = link["source"]
        target_iface_id = link["target"]

        source_elem = iface_mapping_dict.get(source_iface_id)
        target_elem = iface_mapping_dict.get(target_iface_id)

        if source_elem and target_elem:
            ppr_links.append({
                "name": source_elem + "_to_" + target_elem,  # You can customize the naming convention as needed
                "source": source_elem,
                "target": target_elem,
                "type": config.edgeType_by_view["PPR View"][0],  # Assuming all links extracted here are PPR links. Adjust if there are different types of links.
                "cardinality": link.get("cardinality")
            })

    return ppr_links