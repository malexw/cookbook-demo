import os
import yaml
from jinja2 import Environment, FileSystemLoader
from nbconvert import HTMLExporter, MarkdownExporter
from collections import defaultdict


def create_htdocs():
  with open('registry.yaml', 'r') as f:
      registry = yaml.safe_load(f)

  if not os.path.exists('htdocs'):
      os.makedirs('htdocs')

  tag_index = defaultdict(list)
  html_exporter = HTMLExporter(
      template_name='manta',
      extra_template_basedirs=['scripts/templates'],
  )
  for entry in registry:
      title = entry['title']
      path = entry['path']
      tags = entry['tags']
      notebook_metadata = {
          'title': title,
          'authors': ", ".join(entry['authors']),
          'path': path,
      }

      for tag in tags:
          tag_index[tag].append(notebook_metadata)
      
      (body, resources) = html_exporter.from_filename(path)
      with open(f'htdocs/{title}.html', 'w') as output_file:
          output_file.write(body)

  file_loader = FileSystemLoader('scripts/templates')
  env = Environment(loader=file_loader)
  template = env.get_template('index.html')
  output = template.render(tags=tag_index)
  with open('htdocs/index.html', 'w') as f:
      f.write(output)

def create_markdown():
  with open('registry.yaml', 'r') as f:
      registry = yaml.safe_load(f)

  if not os.path.exists('markdown'):
      os.makedirs('markdown')

  tag_index = defaultdict(list)
  exporter = MarkdownExporter(
      template_name='docmd',
      extra_template_basedirs=['scripts/templates'],
  )
  for entry in registry:
      title = entry['title']
      path = entry['path']
      tags = entry['tags']
      notebook_metadata = {
          'title': title,
          'category': entry['category'],
          'authors': ", ".join(entry['authors']),
          'path': path,
      }

      for tag in tags:
          tag_index[tag].append(notebook_metadata)
      
      (body, resources) = exporter.from_filename(
          path,
          resources={'metadata': notebook_metadata}
      )
      with open(f'markdown/{title}.md', 'w') as output_file:
          output_file.write(body)

if __name__ == "__main__":
    # create_htdocs()
    create_markdown()
