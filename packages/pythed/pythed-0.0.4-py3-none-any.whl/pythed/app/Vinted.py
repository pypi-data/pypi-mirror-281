from pythed.app.utils import cookies
from pythed.app.api.items import search, similar_items, get_item_details
from pythed.app.api.brand import get_brands, filter_brand, get_multiple_brands
from pythed.app.api.users import get_user_info, get_user_reviews
from pythed.app.api.shipping_details import get_shipping_details 
from pythed.app.api.sizes import get_all_sizes
from pythed.app.api.status import get_all_status

class Vinted:
    def __init__(self):
        """Initialize the Vinted object with authentication cookies."""
        self.auth_cookie = cookies.load_auth_cookie()  # [0] - Cookie name ||| [1] - Cookie value
        self.cookies = {self.auth_cookie[0]: self.auth_cookie[1]}
        
    def search_items(self, page: int = 1, perPage: int = 20, search_text: str = None, size_ids: list = None, brand_ids: list = None, status_ids: list = None, price_from: str = None, price_to: str = None) -> list:
        """
        Search items based on various parameters.
        
        :param page: The page number of the search results (default is 1).
        :param perPage: The number of items per page (default is 20).
        :param search_text: The text to search for.
        :param size_ids: A list of size IDs to filter the search.
        :param brand_ids: A list of brand IDs to filter the search.
        :param status_ids: A list of status IDs to filter the search.
        :param price_from: Minimum price to filter the search.
        :param price_to: Maximum price to filter the search.
        :return: A list of search results.
        """
        kwargs = {
            "page": page,
            "per_page": perPage,
            "search_text": search_text,
            "size_ids": size_ids,
            "brand_ids": brand_ids,
            "status_ids": status_ids,
            "price_from": price_from,
            "price_to": price_to
        }
        return search(self.cookies, **kwargs)
    
    def similar_items(self, item_id: str) -> list:
        """
        Get similar items based on a given item ID.
        
        :param item_id: The ID of the item to find similar items for.
        :return: A list of similar items.
        """
        return similar_items(self.cookies, item_id=item_id)["items"]
    
    def get_all_brands(self) -> list:
        """
        Get a list of all brands.
        
        :return: A list of all brands.
        """
        return get_brands()
    
    def get_brand(self, brand_id: int = None, brand_name: str = None, is_luxury: bool = None, requires_authenticity_check: bool = None) -> list:
        """
        Filter brands based on various criteria.
        
        :param brand_id: The ID of the brand.
        :param brand_name: The name of the brand.
        :param is_luxury: Whether the brand is considered luxury.
        :param requires_authenticity_check: Whether the brand requires authenticity check.
        :return: A list of brands matching the criteria.
        """
        return filter_brand(brand_id, brand_name, is_luxury, requires_authenticity_check)
    
    def get_brands(self, brand_names: list = [str]) -> list:
        """
        Get multiple brands by their names.
        
        :param brand_names: A list of brand names to fetch.
        :return: A list of brands matching the names.
        """
        return get_multiple_brands(names=brand_names)
    
    def get_user_info(self, user_id: str) -> list:
        """
        Get public information of a user.
        
        :param user_id: The ID of the user.
        :return: A list of user information.
        """
        return get_user_info(self.cookies, user_id=user_id)
    
    def get_shipping_details(self, item_id: int) -> list:
        """
        Get shipping details for a specific item.
        
        :param item_id: The ID of the item.
        :return: A list of shipping details.
        """
        return get_shipping_details(self.cookies, item_id=item_id)
    
    def get_item_details(self, item_id: int) -> list:
        """
        Get detailed information about an item.
        
        :param item_id: The ID of the item.
        :return: A list of item details.
        """
        return get_item_details(self.cookies, item_id=item_id)
    
    def get_user_reviews(self, user_id: str) -> list:
        """
        Get reviews for a specific user.
        
        :param user_id: The ID of the user.
        :return: A list of user reviews.
        """
        return get_user_reviews(self.cookies, user_id=user_id)

    def get_all_status(self) -> list:
        """Returns all elements used to qualify the condition in which an item is"""
        
        return get_all_status()
    
    def get_all_sizes(self) -> list:
        """Returns all sizes"""

        return get_all_sizes()