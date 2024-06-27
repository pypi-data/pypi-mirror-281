"""SDK do Mercado Livre para gerenciamento de produtos."""
import requests
from .product_model import ProductAd, ProductCreate, ProductUpdate, ProductDescription

class ProductManager:
    """Classe responsável por gerenciar os produtos do Mercado Livre."""
    def __init__(self, access_token: str):
        """Inicializa o gerenciador de produtos."""
        self.access_token = access_token
        self.url = 'https://api.mercadolibre.com/items'

    def get_product(self, product_id: str) -> ProductAd:
        """
        Obtém um produto do Mercado Livre.
        :param product_id: ID do produto.
        :return: Produto obtido.
        """
        response = requests.get(
            f'{self.url}/{product_id}', 
            headers={'Authorization': f'Bearer {self.access_token}'},
            timeout=30
        )
        response.raise_for_status()
        return ProductAd(**response.json())

    def create_product(self, product: ProductCreate) -> ProductAd:
        """
        Criar um produto no Mercado Livre.
        :param product: Produto a ser criado.
        :return: Produto criado.
        """
        response = requests.post(
            self.url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            json=product.model_dump(),
            timeout=30
        )
        response.raise_for_status()
        return ProductCreate(**response.json())

    def update_product(self, product_id: str, product: ProductUpdate) -> ProductAd:
        """
        Atualiza um produto no Mercado Livre.
        :param product_id: ID do produto.
        :param product: Produto a ser atualizado.
        """
        response = requests.put(
            f'{self.url}/{product_id}',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json=product.model_dump(),
            timeout=30
        )
        response.raise_for_status()
        return ProductAd(**response.json())

    def close_product(self, product_id: str) -> ProductAd:
        """
        Fecha um produto no Mercado Livre.
        :param product_id: ID do produto.
        :return: Produto fechado.
        """
        response = requests.put(
            f'{self.url}/{product_id}',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={'status': 'closed'},
            timeout=30
        )
        response.raise_for_status()
        return ProductAd(**response.json())

    def delete_product(self, product_id: str) -> ProductAd:
        """
        Exclui um produto no Mercado Livre.
        :param product_id: ID do produto.
        :return: Produto excluído.
        """
        self.close_product(product_id)
        response = requests.put(
            f'{self.url}/{product_id}',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={'deleted': True},
            timeout=30
        )
        response.raise_for_status()
        return ProductAd(**response.json())

    def get_product_description(self, product_id: str) -> ProductDescription:
        """
        Busca a descrição de um produto no Mercado Livre.
        :param product_id: ID do produto.
        :return: Descrição do produto.
        """
        response = requests.get(
            f'{self.url}/{product_id}/description',
            headers={'Authorization': f'Bearer {self.access_token}'},
            timeout=30
        )
        response.raise_for_status()
        return ProductDescription(**response.json())

    def update_product_description(
            self,product_id: str,
            description: ProductDescription) -> ProductDescription:
        """
        Atualiza a descrição de um produto no Mercado Livre.
        :param product_id: ID do produto.
        :param description: Descrição do produto.
        """
        response = requests.put(
            f'{self.url}/{product_id}/description',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json=description.model_dump(),
            timeout=30
        )
        response.raise_for_status()
        return ProductDescription(**response.json())
