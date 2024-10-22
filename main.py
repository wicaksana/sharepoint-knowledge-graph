import asyncio
import json
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
from kiota_serialization_json.json_serialization_writer import JsonSerializationWriter
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory

site_id = 'd4782aca-aacc-4f4f-a6d1-af9e0f41c4be'
page_id = 'fc8157b4-cb7f-482e-8afb-800688fd8ee8'

async def display_access_token(graph: Graph):
    token = await graph.get_app_only_token()
    print(f'App-only token: {token}\n')

async def list_users(graph: Graph):
    users_page = await graph.get_users()

    if users_page and users_page.value:
        for user in users_page.value:
            print(f'User: {user.display_name}')
            print(f'ID: {user.id}')
            print(f'Email: {user.mail}')
        
        # if @odata.nextLink is present
        more_available = users_page.odata_next_link is not None
        print(f'\nMore users available? {more_available}\n')

async def list_sites(graph: Graph):
    sites = await graph.get_sites()

    if sites and sites.value:
        for site in sites.value:
            print(f'URL: {site.web_url}')
            print(f'Hostname: {site.site_collection.hostname}')
            print(f'Root: {site.site_collection.root}')

async def list_all_sites(graph: Graph):
    print('getting all sites..')
    result = await graph.list_all_sites()
    print(f'result value: {result.value}')
    if result and result.value:
        for res in result.value:
            print(f'Name: {res.name}')
            print(f'URL: {res.url}')

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

async def get_page_content(graph: Graph):
    """TODO use this."""
    result = await graph.get_page_content(site_id, page_id)
    # print(f'result: \n{result}')
    writer = JsonSerializationWriterFactory().get_serialization_writer('application/json')
    result.serialize(writer=writer)
    result_str = writer.get_serialized_content()

    result_obj = json.loads(result_str)

    print(json.dumps(result_obj, indent=2))

async def get_base_site_pages(graph: Graph):
    result = await graph.get_list_base_site_page(site_id)
    if result and result.value:
        for res in result.value:
            print(f'baseSitePage: {res.id}')


async def main():
    config = configparser.ConfigParser()
    config.read(['config.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    try:
        # await display_access_token(graph=graph)
        # await list_users(graph=graph)
        # await list_sites(graph=graph)
        # await list_all_sites(graph=graph)
        # await get_site_by_id(graph=graph)
        # await get_base_site_page(graph=graph)
        # await get_all_pages(graph=graph)
        await get_page_content(graph=graph)
        # await get_base_site_pages(graph=graph)
    except ODataError as odata_error:
        print(odata_error.error.code, odata_error.error.message)

if __name__ == '__main__':
    asyncio.run(main())