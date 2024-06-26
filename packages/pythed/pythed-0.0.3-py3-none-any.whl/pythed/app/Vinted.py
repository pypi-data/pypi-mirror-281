from pythed.app.utils import cookies
from pythed.app.api.items import search, similar_items, get_item_details
from pythed.app.api.brand import get_brands, filter_brand 
from pythed.app.api.users import get_user_info, get_user_reviews
from pythed.app.api.shipping_details import get_shipping_details 

class Vinted():
    def __init__(self):
        self.auth_cookie = cookies.load_auth_cookie() # [0] - Cookie name ||| [1] - Cookie value
        self.cookies = {self.auth_cookie[0]: self.auth_cookie[1]}
        
    def search_items(self, page: int = 1, perPage: int = 20, search_text: str = None, size_ids: list = None, brand_ids: list = None, status_ids: list = None) -> list:
        kwargs = {
            "page": page,
            "per_page": perPage,
            "search_text": search_text,
            "size_ids": size_ids,
            "brand_ids": brand_ids,
            "status_ids": status_ids
        }
        
        return search(self.cookies, **kwargs)
    
    def similar_items(self, item_id: str) -> list:
        return similar_items(self.cookies, item_id=item_id)["items"]
    
    def get_all_brands(self) -> list:
        return get_brands()
    
    def get_brand(self, brand_id:int=None, brand_name:str=None, is_luxury:bool=None, requires_authenticity_check:bool=None) -> list:
        return filter_brand(brand_id, brand_name, is_luxury, requires_authenticity_check)
    
    def get_user_info(self, user_id: str) -> list:
        return get_user_info(self.cookies, user_id=user_id)
    
    def get_shipping_details(self, item_id: str) -> list:
        return get_shipping_details(self.cookies, item_id=item_id)
    
    def get_item_details(self, item_id: str) -> list:
        return get_item_details(self.cookies, item_id=item_id)
        
    def get_user_reviews(self, user_id: str) -> list:
        return get_user_reviews(self.cookies, user_id=user_id)