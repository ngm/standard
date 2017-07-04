import re
import csv
import sys
from sphinxcontrib.jsonschema import JSONSchema

schema = JSONSchema.loadfromfile(sys.argv[1])


# Based on https://stackoverflow.com/questions/30734682/extracting-url-and-anchor-text-from-markdown-using-python
INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def find_md_links(md):
    links = dict(INLINE_LINK_RE.findall(md))
    return links

def remove_links(text,links):
    for key, link in links.items():
        text = text.replace("["+key+"]("+link+")",key)
    return text
    
def display_links(links):
    link_list = []
    for key, link in links.items():
        link_list.append(link)
        
    return ", ".join(link_list)

f = sys.stdout
w = csv.DictWriter(f,['section','path','title','description','type','range','values','links','deprecated','deprecationNotes'])
w.writeheader()
for prop in schema:
    if '^' in prop.name:
        # Skip patternProperties
        continue

    links = find_md_links(prop.description)

    if isinstance(prop.attributes['type'], list):
        type_ = ', '.join(x for x in prop.attributes['type'] if x != 'null')
    else:
        type_ = prop.attributes['type']

    minn = '1' if prop.required else '0'
    maxn = 'n' if type_ == 'array' else '1'        

    w.writerow(
        {
            'section': prop.name.split('/')[0] if '/' in prop.name else '',
            'path': prop.name,
            'title': prop.title,
            'description': remove_links(prop.description, links),
            'type': type_,
            'range': minn+".."+maxn,
            'values': prop.format,
            'links': display_links(links),
            'deprecated': prop.deprecated.get('deprecatedVersion', '') if prop.deprecated else '',
            'deprecationNotes': prop.deprecated.get('description','') if prop.deprecated else ''
        }
    )
f.close()

