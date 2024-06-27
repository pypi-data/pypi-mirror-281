import requests
import json

def _get_bundles(bundle):
    url = f"https://www.humblebundle.com/{bundle}"
    response = requests.get(url)
    content = response.text
    start_index = content.find('<script id="landingPage-json-data" type="application/json">')
    start_index += len('<script id="landingPage-json-data" type="application/json">')
    end_index = content.find('</script>', start_index)
    json_data = content[start_index:end_index]
    json_loaded = json.loads(json_data)
    bundle_data = json_loaded['data'][bundle]['mosaic']
    return(bundle_data)

def _get_choice(month, year):
    url = f"https://www.humblebundle.com/membership/{month}-{year}"
    response = requests.get(url)
    content = response.text
    start_index = content.find('<script id="webpack-monthly-product-data" type="application/json">')
    start_index += len('<script id="webpack-monthly-product-data" type="application/json">')
    end_index = content.find('</script>', start_index)
    json_data = content[start_index:end_index]
    json_loaded = json.loads(json_data)
    choice_data = json_loaded['contentChoiceOptions']['contentChoiceData']
    return(choice_data)

def _get_bundle_games(url):
    response = requests.get(url)
    content = response.text
    start_index = content.find('<script id="webpack-bundle-page-data" type="application/json">')
    start_index += len('<script id="webpack-bundle-page-data" type="application/json">')
    end_index = content.find('</script>', start_index)
    json_data = content[start_index:end_index]
    json_loaded = json.loads(json_data)
    choice_data = json_loaded['bundleData']
    return(choice_data)