"""Script to verify the products in the Mercado Livre API."""
from .product_manager import ProductManager
import asyncio as aio


class ProductVerification:
    product_manager: ProductManager

    def __init__(self, access_token: str, products_ids: list[str] = []) -> None:
        """
        Initializes the product verification.
        :param access_token: Access token to the Mercado Livre API.
        :param products_ids: List of products IDs to verify
        """
        self.product_manager = ProductManager(access_token)
        self.products_ids = products_ids
    
    def verify_state_products(self, filter: list[str] = ['active']) -> dict:
        """
        Verify the products in the Mercado Livre API.
        :param filter: List of states to filter the products.
        :return: Count of products in each state.
        """
        tasks = [self.product_manager.get_product(product_id) for product_id in self.products_ids]
        products = aio.run(aio.gather(*tasks))

        count = {
            'active': 0,
            'inactive': 0,
            'closed': 0,
            'review': 0
        }
        for product in products:
            for state in filter:
                if product.status == state:
                    count[state] += 1
                    break

        return count

    def verify_products_in_oficial_store(self, oficial_store_id: str) -> dict:
        """
        Verify the products in the oficial store in the Mercado Livre API.
        :param oficial_store_id: ID of the oficial store.
        :return: Count of products in the oficial store and not in the oficial store.
        """
        tasks = [self.product_manager.get_product(product_id) for product_id in self.products_ids]
        products = aio.run(aio.gather(*tasks))

        count = {
            'count_ads_in_oficial_store': 0,
            'ads_in_oficial_store': [],
            'count_ads_not_in_oficial_store': 0,
            'ads_not_in_oficial_store': []
        }
        for product in products:
            if product.official_store_id == oficial_store_id:
                count['count_ads_in_oficial_store'] += 1
                count['ads_in_oficial_store'].append(product.id)
                continue

            count['count_ads_not_in_oficial_store'] += 1
            count['ads_not_in_oficial_store'].append(product.id)

        return count
