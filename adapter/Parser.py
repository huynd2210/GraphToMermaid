from typing import Set, List

from adapter.utils import get_string_between_delimiters


def extractNodeLabel(line, delimiters) -> List[str]:
    for delimiter in delimiters:
        firstDelimiter, secondDelimiter = delimiter
        substring = get_string_between_delimiters(line, firstDelimiter, secondDelimiter)
        if substring is not None:
            return substring

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
    mermaid_code_as_list = mermaidCode.split("\n")
    nodes = []

    for line in mermaid_code_as_list:
        linkType = isLineContainsLink(line, mermaid_links_types)
        if linkType:
            leftNode = line.split(linkType)[0].strip()
            rightNode = line.split(linkType)[1].strip()
            if leftNode not in nodes:
                nodes.append(leftNode)
            if rightNode not in nodes:
                nodes.append(rightNode)

    return nodes

def isLineContainsLink(line: str, mermaid_links_types: Set[str]):
    """
    Checks if the line contains any of the specified mermaid link types.

    Args:
        line (str): The line to check for links.
        mermaid_links_types (Set[str]): The set of mermaid link types to look for.

    Returns:
        str: The link type found in the line, or False if none found.
    """
    for link_type in mermaid_links_types:
        if link_type in line:
            return link_type
    return False

#TODO: Handle complex mermaid links
def extractEdgesFromMermaid(mermaidCode: str, mermaid_links_types: Set[str]):
    mermaid_code_as_list = mermaidCode.split("\n")
    edges = []
    for line in mermaid_code_as_list:
        #If there is a link in the line, extract the edge (node connection)
        linkType = isLineContainsLink(line, mermaid_links_types)
        if linkType:
            edge = (line.split(linkType)[0].strip(), line.split(linkType)[1].strip())
            edges.append(edge)
    return edges