import os
import yaml
import nbformat
from nbconvert import HTMLExporter
from collections import defaultdict

# Parse registry.yaml
with open('registry.yaml', 'r') as f:
    registry = yaml.safe_load(f)

# Create 'htdocs' directory if it doesn't exist
if not os.path.exists('htdocs'):
    os.makedirs('htdocs')

# Traverse registry and convert notebooks
tag_index = defaultdict(list)
html_exporter = HTMLExporter()
for entry in registry:
    title = entry['title']
    path = entry['path']
    authors = ", ".join(entry['authors'])
    tags = entry['tags']

    for tag in tags:
        tag_index[tag].append((title, authors))
    
    # Convert notebook to HTML
    with open(path, 'r') as notebook_file:
        notebook_content = notebook_file.read()
        (body, resources) = html_exporter.from_notebook_node(nbformat.reads(notebook_content, nbformat.NO_CONVERT))
        with open(f'htdocs/{title}.html', 'w') as output_file:
            output_file.write(body)

# Generate index.html
with open('htdocs/index.html', 'w') as f:
    f.write("<html>\n<head>\n<title>Notebook Index</title>\n</head>\n<body>\n")
    for tag in sorted(tag_index.keys()):
        f.write("<h2>%s</h2>\n<ul>\n" % tag)
        for title, authors in tag_index[tag]:
            f.write(f'<li><a href="{title}.html">{title}</a> by {authors}</li>\n')
        f.write("</ul>\n")
    f.write("</body>\n</html>\n")
