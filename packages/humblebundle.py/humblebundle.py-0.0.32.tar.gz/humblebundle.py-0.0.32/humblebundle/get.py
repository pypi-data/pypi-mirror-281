from .api import _get_bundles, _get_choice

class _Product:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
            
def bundles(bundles : list):
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

def choices(month : str, year : int):
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