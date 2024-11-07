# sharepoint-knowledge-graph
Create knowledge graph from a Sharepoint site (for Sharepoint in Microsoft 365).

## Sharepoint Pages Used

Folder [pages](pages) contains all Sharepoint pages (in PDF format) used as reference. The contents are mostly generated using ChatGPT.

## Get Sharepoint Data using Microsoft Graph API

Related files:
- [graph.py](graph.py)
- [main.py](main.py)

```bash
pip install -r requirements.txt
python main.py
```

Results are stored in `data` directory.

## Load Sharepoint data to Neo4j

Related file:
- [01_load_data.ipynb](01_load_data.ipynb)

## Get image description using OpenAI 

Related file:
- [02_get_image_description.ipynb](02_get_image_description.ipynb)

## Semantic Search

Related file:
- [03_semantic_search.ipynb](03_semantic_search.ipynb)