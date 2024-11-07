import os
import asyncio
import json
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
from kiota_serialization_json.json_serialization_writer import JsonSerializationWriter
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory

site_id = 'd4782aca-aacc-4f4f-a6d1-af9e0f41c4be'

async def get_site_by_id(graph: Graph):
    print('get a site by id..')
    result = await graph.get_site_by_id()

    print(f'id: {result.id}')
    print(f'display name: {result.display_name}')

async def get_all_pages(graph: Graph):
    print(f'Get all pages from site {site_id}')
    result = await graph.get_list_site_pages(site_id=site_id)
    if result and result.value:
        for res in result.value:
            print(f'page id: {res.id}')

async def get_page_content(graph: Graph, site_id, page_id):
    """
    Get page content
    """
    content = await graph.get_page_content(site_id, page_id)

    writer = JsonSerializationWriterFactory().get_serialization_writer('application/json')
    content.serialize(writer=writer)
    result_str = writer.get_serialized_content()

    result_obj = json.loads(result_str)
    result = json.dumps(result_obj, indent=2)

    return result

async def get_base_site_pages(graph: Graph):
    """
    Get the collection of baseSitePage objects from the site pages list in a site. 
    """
    base_site_page_list = await graph.get_list_base_site_page(site_id)
    result = []
    if base_site_page_list and base_site_page_list.value:
        for page in base_site_page_list.value:
            result.append({'id': page.id, 'name': page.name})
    
    return result


async def main():
    config = configparser.ConfigParser()
    config.read(['config.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    try:
        pages = await get_base_site_pages(graph=graph)
        print(f'There are {len(pages)} pages found.')

        for page in pages:
            print(f'Processing {page['name']}')
            filename = page['name'].split('.aspx')[0] + '.json'
            content = await get_page_content(graph=graph, site_id=site_id, page_id=page['id'])
            with open(os.path.join('data', filename), 'w') as out:
                out.write(content)

    except ODataError as odata_error:
        print(odata_error.error.code, odata_error.error.message)

if __name__ == '__main__':
    asyncio.run(main())