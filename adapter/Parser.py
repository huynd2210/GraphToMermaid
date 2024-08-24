from typing import Set, List
import re

from utils import get_string_between_delimiters

INT_MAX = 1e9

def extractNodeLabel(line, delimiters) -> List[str]:
    for delimiter in delimiters:
        firstDelimiter, secondDelimiter = delimiter
        substring = get_string_between_delimiters(line, firstDelimiter, secondDelimiter)
        if substring is not None:
            return substring


def extractNodes(mermaidCode:str, delimiters: Set[str], mermaid_links_types: List[str]) -> dict:
    mermaid_code_as_list = mermaidCode.strip('\n').split("\n")[1:]
    mermaid_code_as_list = [line.strip() for line in mermaid_code_as_list if line.strip()]
    nodeIds_labels = {}

    nodeIdsFromLinks = extractNodesFromLinks(mermaidCode, mermaid_links_types)

    for line in mermaid_code_as_list:
        if not extractEdgeDetailFromLine(line, mermaid_links_types)[0]:
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

def extractNodesFromLinks(mermaidCode: str, mermaid_links_types: List[str]):
    mermaid_code_as_list = mermaidCode.strip("\n").split("\n")
    nodes = []

    for line in mermaid_code_as_list[1:]:
        while (match := extractEdgeDetailFromLine(line, mermaid_links_types))[0]:
            link_type = match[0]
            left_nodes = line.split(link_type, 1)[0].strip(" ")
            right_sides = line.split(link_type, 1)[1] # there maybe more links involved 
            line = right_sides

            for node in getNodeFromSite(left_nodes):
                if node not in nodes: nodes.append(node)    

            if not extractEdgeDetailFromLine(line, mermaid_links_types)[0]:
                for node in getNodeFromSite(line):
                    if node not in nodes: nodes.append(node)    
    return nodes

def getNodeFromSite(site: str):
    return [node.strip() for node in site.split("&")]

def normalizedEdge(firstNodes: list[str], secondNodes: list[str], description = None):
    return [(a, b, description) for a in firstNodes for b in secondNodes]  
def extractEdgesFromMermaid(mermaidCode: str, mermaid_links_types: List[str]):
    mermaid_code_as_list = mermaidCode.strip("\n").split("\n")
    edges = []
    for line in mermaid_code_as_list:
        #If there is a link in the line, extract the edge (node connection)
        last_site = []
        last_description = ""
        while (match := extractEdgeDetailFromLine(line, mermaid_links_types))[0]: 
            link_type = match[0]
            left_nodes = getNodeFromSite(line.split(link_type, 1)[0].strip())
            if last_site:
                edges.extend(normalizedEdge(last_site, left_nodes, last_description))

            last_description = match[1]
            line = line.split(link_type, 1)[1]
            last_site = left_nodes
            
            if not extractEdgeDetailFromLine(line, mermaid_links_types)[0]:
                edges.extend(normalizedEdge(left_nodes, getNodeFromSite(line), last_description))
    return edges

def extractEdgeDetailFromLine(line, mermaid_links_types):
    last_match, description, start_index = None, "", INT_MAX

    for pattern in mermaid_links_types:
        if match := re.search(pattern, line):
            if match.start() >= start_index: 
                continue
            last_match = match.group(0)
            if len(match.groups()) > 0:
                description = match.group(1)
            start_index = match.start()
            
    return (last_match, description)


