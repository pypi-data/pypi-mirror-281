from .api import _get_bundles, _get_choice
from typing import List, Dict, Union

class _Product:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
            
def bundles(bundles: List[str]) -> Dict[str, _Product]:
    """
    Retrieves bundle information from Humble Bundle.

    Args:
        bundles (list of str): A list of bundle names to retrieve (e.g., ['books','games','software']).

    Returns:
        dict: A dictionary where keys are bundle names and values are `_Product` instances.
            Each `_Product` instance contains the following attributes:
            - type (str)
            - product_url (str)
            - high_res_tile_image (str)
            - tile_logo (str)
            - detailed_marketing_blurb (str)
            - short_marketing_blurb (str)
            - tile_name (str)
            - tile_short_name (str)
            - start_date (str)
            - end_date (str)
            - bundles_sold (float)
            - highlights (str)
            
        Example Usage:
        bundles = humblebundle.get.bundles('games')
        print(bundles['bundlename'].product_url)
    """
    for bundle in bundles:
        bundle = bundle.lower()
        data = _get_bundles(bundle) or []
        products = data[0].get('products')
        lst = []
        
        for product in products:
            dct = {}
            dct['type'] = product.get('tile_stamp')
            dct['product_url'] = f"https://www.humblebundle.com{product.get('product_url')}"
            dct['high_res_tile_image'] = product.get('high_res_tile_image')
            dct['tile_logo'] = product.get('tile_logo')
            dct['detailed_marketing_blurb'] = product.get('detailed_marketing_blurb')
            dct['short_marketing_blurb'] = product.get('short_marketing_blurb')
            dct['tile_name'] = product.get('tile_name')
            dct['tile_short_name'] = product.get('tile_short_name')
            dct['start_date'] = product.get('start_date|datetime')
            dct['end_date'] = product.get('end_date|datetime')
            dct['bundles_sold'] = product.get('bundles_sold|decimal')
            dct['highlights'] = product.get('highlights')

            lst.append((product.get('machine_name'), dct))

    instances = {}
    for name, kwargs in lst:
        instances[name] = _Product(name, **kwargs)
        
    return instances

def choices(month: str, year: int) -> Dict[str, _Product]:
    """
    Retrieves Humble Choice products from Humble Bundle for a given month and year.

    Args:
        month (str): The month of the choices to retrieve (e.g., 'january', 'february', 'march').
        year (int): The year of the choices.

    Returns:
        Dict[str, _Product]: A dictionary where keys are machine names and values are `_Product` instances.
            Each `_Product` instance contains the following attributes:
            - title (str)
            - parent_url (str)
            - product_url (str)
            - developers (List[str])
            - media (List[str])
            - genres (List[str])
            - delivery_methods (List[str])
            
        Example Usage:
        games = humblebundle.get.choices('january',2024)
        print(games['gameename'].product_url)
    """
    url = f"https://www.humblebundle.com/membership/{month}-{year}"
    data = _get_choice(month, year) or {}
    products = data.get('game_data')
    lst = []
    
    for _, product in products.items():
        dct = {}
        dct['title'] = product.get('title')
        dct['parent_url'] = url
        dct['product_url'] = f"{url}/{product.get('display_item_machine_name')}"
        dct['developers'] = product.get('developers')
        dct['media'] = product.get('carousel_content')
        dct['genres'] = product.get('genres')
        dct['delivery_methods'] = product.get('delivery_methods')
        
        lst.append((product.get('display_item_machine_name'), dct))

    instances = {}
    for name, kwargs in lst:
        instances[name] = _Product(name, **kwargs)
        
    return instances