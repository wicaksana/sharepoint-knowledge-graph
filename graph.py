from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from msgraph.graph_service_client import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.sites.sites_request_builder import SitesRequestBuilder
from msgraph.generated.sites.item.pages.graph_site_page.graph_site_page_request_builder import GraphSitePageRequestBuilder

class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.app_client = GraphServiceClient(self.client_credential)

    async def get_app_only_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)

        return access_token.token
    
    async def get_users(self):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            select=['displayName', 'id', 'mail'],
            top=25,
            orderby=['displayName']
        )

        request_config = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        users = await self.app_client.users.get(request_configuration=request_config)

        return users
    
    async def get_sites(self):
        query_params = SitesRequestBuilder.SitesRequestBuilderGetQueryParameters(
            select=['siteCollection','webUrl'],
            filter='siteCollection/root ne null'
        )

        request_configuration = SitesRequestBuilder.SitesRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        sites = await self.app_client.sites.get(request_configuration=request_configuration)

        return sites
    
    async def list_all_sites(self):
        result = await self.app_client.sites.get()
        return result
    
    async def get_site_by_id(self):
        id = 'd4782aca-aacc-4f4f-a6d1-af9e0f41c4be'
        result = await self.app_client.sites.by_site_id(id).get()

        return result

    async def get_list_base_site_page(self, site_id):
        """
        Get the collection of `baseSitePage` objects from the site pages list in a site. 
        Reference: https://learn.microsoft.com/en-us/graph/api/basesitepage-list?view=graph-rest-1.0&tabs=python
        """
        result = await self.app_client.sites.by_site_id(site_id).pages.get()
        return result
    
    async def get_list_site_pages(self, site_id):
        result = await self.app_client.sites.by_site_id(site_id).pages.graph_site_page.get()
        return result
    

    async def get_page_content(self, site_id, page_id):
        """Get page content, including canvasLayout"""
        query_params = GraphSitePageRequestBuilder.GraphSitePageRequestBuilderGetQueryParameters(
            expand=['canvasLayout']
        )

        request_config = GraphSitePageRequestBuilder.GraphSitePageRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        result = await self.app_client.sites.by_site_id(site_id).pages.by_base_site_page_id(page_id).graph_site_page.get(request_configuration=request_config)
        return result