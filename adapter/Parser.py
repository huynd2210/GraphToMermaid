from typing import Set, List

from adapter.utils import get_string_between_delimiters

def extractNodeLabel(line, delimiters) -> List[str]:
    for delimiter in delimiters:
        firstDelimiter, secondDelimiter = delimiter
        substring = get_string_between_delimiters(line, firstDelimiter, secondDelimiter)
        if substring is not None:
            return substring

def extractNodeLabelAndId(line, delimiters) -> List[str]:
    for delimiter in delimiters:
        firstDelimiter, secondDelimiter = delimiter
        node_label = get_string_between_delimiters(line, firstDelimiter, secondDelimiter)
        node_id = line.split(firstDelimiter, 1)[0]
        if substring is not None:
            return (node_id, node_label)

def extractNodes(mermaidCode:str, delimiters: Set[str], mermaid_links_types: Set[str]) -> dict:
    mermaid_code_as_list = mermaidCode.strip('\n').split("\n")[1:]
    mermaid_code_as_list = [line.strip() for line in mermaid_code_as_list if line.strip()]
    nodeIds_labels = {}

    nodeIdsFromLinks = extractNodesFromLinks(mermaidCode, mermaid_links_types)

    for line in mermaid_code_as_list:
        if not isLineContainsLink(line, mermaid_links_types):
            nodeLabel = extractNodeLabel(line, delimiters)
            nodeId = line[0]
            nodeIds_labels[nodeId] = nodeLabel

    for nodeId in nodeIdsFromLinks:
        if nodeId not in nodeIds_labels:
            nodeIds_labels[nodeId] = nodeId
    return nodeIds_labels

    

def extractNodeDeclarationFromMermaid(mermaid_code_as_list: List[str], delimiters) -> Set[str]:
    declarations = set()
    for line in mermaid_code_as_list:
        for delimiter in delimiters:
            firstDelimiter, secondDelimiter = delimiter
            if firstDelimiter in line and secondDelimiter in line:
                declarations.add(line)
    return declarations

def extractNodesFromLinks(mermaidCode: str, mermaid_links_types: Set[str]):
    mermaid_code_as_list = mermaidCode.strip("\n").split("\n")
    nodes = []

    for line in mermaid_code_as_list[1:]:
        while link_type := isLineContainsLink(line, mermaid_links_types):
            left_nodes = line.split(link_type, 1)[0].strip(" ")
            right_sides = line.split(link_type, 1)[1] # there maybe more links involved 
            line = right_sides

            for node in getNodeFromSite(left_nodes):
                if node not in nodes: nodes.append(node)    

            if not isLineContainsLink(line, mermaid_links_types):
                for node in getNodeFromSite(line):
                    if node not in nodes: nodes.append(node)    


    return nodes

def isLineContainsLink(line: str, mermaid_links_types: Set[str]):
    for i in range(0, len(line) - 3):
        for link_type in mermaid_links_types:
            if link_type in line[i: i + 3]:
                return link_type
    return None

def getNodeFromSite(site: str):
    return [node.strip() for node in site.split("&")]
    

#TODO: Handle complex mermaid links
def extractEdgesFromMermaid(mermaidCode: str, mermaid_links_types: Set[str]):
    mermaid_code_as_list = mermaidCode.strip("\n").split("\n")
    edges = []
    for line in mermaid_code_as_list:
        #If there is a link in the line, extract the edge (node connection)
        last_site = []
        while link_type := isLineContainsLink(line, mermaid_links_types):
            left_nodes = getNodeFromSite(line.split(link_type, 1)[0].strip())
            if left_nodes:
                for a in last_site:
                    for b in left_nodes:
                        edges.append((a, b))
            
            line = line.split(link_type, 1)[1]
            last_site = left_nodes
            
            if not isLineContainsLink(line, mermaid_links_types):
                for a in last_site:
                    for b in getNodeFromSite(line):
                        edges.append((a, b)) 
    return edges
