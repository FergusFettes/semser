from semanticscholar import SemanticScholar, SemanticScholarException
from pathlib import Path
from pyzotero import zotero

# load API key from file
api_key = Path('~/pa/zotero').expanduser().read_text().strip()

zot = zotero.Zotero('5339216', 'group', api_key)
sch = SemanticScholar()

items = zot.top(limit=50)

# Print the name and the DOI
for item in items:
    if 'DOI' not in item['data']:
        print(f"No DOI for {item['data']['title']}")
        continue
    # print(item['data']['title'])
    # print(item['data']['DOI'])
    try:
        paper = sch.get_paper(item['data']['DOI'])
    except SemanticScholarException.ObjectNotFoundException:
        print(f"Could not find {item['data']['title']}")
        continue
    print(paper['url'])
