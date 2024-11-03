import os
import pandas as pd 
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.parse import urlparse, urljoin


def get_text_from_people(web_part)->str:
    """
    Process webpart with type `7f718435-ee4d-431c-bdbf-9c4ff326f46e`
    """
    processed_content = web_part['data']['serverProcessedContent']
    persons = web_part['data']['properties']['persons']
    spt = processed_content['searchablePlainTexts']

    text = []

    # title
    title = text.append(next(item['value'] for item in processed_content['searchablePlainTexts'] if item['key'] == 'title'))
    if title:
        text.append(title)
    # Augment persons data
    for idx, person in enumerate(persons):
        person['name'] = next(item['value'] for item in spt if item['key'] == f'persons[{str(idx)}].name')
        person['email'] = next(item['value'] for item in spt if item['key'] == f'persons[{idx}].email')
 
    text += [f'name: {person["name"]}, role: {person["role"]}, email: {person["email"]}' for person in persons]

    return '\n'.join(text)


if __name__== '__main__':
    test = {'id': '8f3ae7cc-325f-407e-b7e5-751148da890b',
        '@odata.type': '#microsoft.graph.standardWebPart',
        'data': {'dataVersion': '1.4',
        'description': 'Display selected people and their profiles',
        'serverProcessedContent': {'htmlStrings': [],
        'imageSources': [],
        'links': [],
        'searchablePlainTexts': [{'key': 'persons[0].name',
            'value': 'Muhammad Arif Wicaksana'},
            {'key': 'persons[1].name', 'value': 'Pramoedya Toer'},
            {'key': 'persons[0].email', 'value': 'arif@muarwi.onmicrosoft.com'}]},
        'title': 'People',
        'properties': {'layout': 1,
        'title': '',
        'persons@odata.type': '#Collection(graph.Json)',
        'persons': [{'id': 'i:0#.f|membership|arif@muarwi.onmicrosoft.com',
            'role': 'Head of Product',
            'firstName': '',
            'lastName': '',
            'upn': '',
            'phone': '',
            'sip': '',
            'department': ''},
            {'id': 'i:0#.f|membership|pram@muarwi.onmicrosoft.com',
            'email': '',
            'role': 'Product Manager',
            'firstName': '',
            'lastName': '',
            'upn': '',
            'phone': '',
            'sip': '',
            'department': ''}]}},
        'webPartType': '7f718435-ee4d-431c-bdbf-9c4ff326f46e'
        }
    get_text_from_people(test)