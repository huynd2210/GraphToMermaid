import re

def parse_mermaid_code(mermaid_code):
    lines = mermaid_code.strip().split('\n')
    edges = []

    for line in lines:
        if 'flowchart' in line.lower():
            continue

        print(f"Processing line: {line}")  # Debug print

        # Handle multiple sources and destinations
        multi_match = re.match(r'([\w\s&]+)\s*-->\s*([\w\s&]+)', line)
        if multi_match:
            sources, destinations = multi_match.groups()
            sources = re.findall(r'\w+', sources)
            destinations = re.findall(r'\w+', destinations)
            for src in sources:
                for dest in destinations:
                    edges.append(f"{src} --> {dest}")
                    print(f"    Added multi edge: {src} --> {dest}")  # Debug print
            continue  # Skip to next line after processing multi-edge

        # Split the line by '&' to handle multiple edges
        parts = [part.strip() for part in line.split('&')]

        for part in parts:
            print(f"  Processing part: {part}")  # Debug print

            # Handle labeled edges
            labeled_match = re.match(r'(\w+)\s*--\s*(.*?)\s*-->\s*(\w+)', part)
            if labeled_match:
                src, label, dest = labeled_match.groups()
                edges.append(f"{src} --> {dest}: {label.strip()}")
                print(f"    Added labeled edge: {src} --> {dest}: {label.strip()}")  # Debug print
                continue

            # Handle unlabeled edges (both --> and ---)
            unlabeled_match = re.match(r'(\w+)\s*(?:-->|---)\s*(\w+)', part)
            if unlabeled_match:
                src, dest = unlabeled_match.groups()
                edges.append(f"{src} --> {dest}")
                print(f"    Added unlabeled edge: {src} --> {dest}")  # Debug print
                continue

    return edges

# Sample Mermaid code
mermaid_code = """
flowchart LR
    a --> b & c --> d
"""
# flowchart LR
#     A -- text --> B & B -- text2 --> C
#     a --> b & c --- d
#     A & B --> C & D




# Parse the Mermaid code and create the graph
output = parse_mermaid_code(mermaid_code)

# Print the result
print("\nFinal output:")
for line in output:
    print(line)