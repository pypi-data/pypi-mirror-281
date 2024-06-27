"""Modelo de produto do Mercado Livre"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class ValueStruct(BaseModel):
    """Estrutura de valor de um atributo de um produto do Mercado Livre"""
    number: int
    unit: str

class Value(BaseModel):
    """Valor de um atributo de um produto do Mercado Livre"""
    id: Optional[str]
    name: str
    struct: Optional[ValueStruct]

class SaleTerm(BaseModel):
    """Termos de venda de um produto do Mercado Livre"""
    id: str
    name: str
    value_id: Optional[str]
    value_name: str
    value_struct: Optional[ValueStruct]
    values: List[Value]
    value_type: str

class Picture(BaseModel):
    """Imagem de um produto do Mercado Livre"""
    id: str
    url: str
    secure_url: str
    size: str
    max_size: str
    quality: str

class Shipping(BaseModel):
    """Informações de envio do produto do Mercado Livre"""
    mode: str
    methods: List[str]
    tags: List[str]
    dimensions: Optional[str]
    local_pick_up: bool
    free_shipping: bool
    logistic_type: str
    store_pick_up: bool

class Address(BaseModel):
    """Endereço do vendedor do Mercado Livre"""
    id: Optional[int]
    comment: str
    address_line: str
    zip_code: str
    city: Dict[str, str]
    state: Dict[str, str]
    country: Dict[str, str]
    search_location: Dict[str, Dict[str, str]]
    latitude: float
    longitude: float

class Attribute(BaseModel):
    """Atributos de um produto do Mercado Livre"""
    id: str
    name: str
    value_id: Optional[str]
    value_name: str
    values: List[Value]
    value_type: str

class ProductAd(BaseModel):
    """Modelo de produto do Mercado Livre"""
    id: str
    site_id: str
    title: str
    seller_id: int
    category_id: str
    user_product_id: Optional[str]
    official_store_id: Optional[str]
    price: float
    base_price: float
    original_price: Optional[float]
    inventory_id: Optional[str]
    currency_id: str
    initial_quantity: int
    available_quantity: int
    sold_quantity: int
    sale_terms: List[SaleTerm]
    buying_mode: str
    listing_type_id: str
    start_time: str
    stop_time: str
    end_time: str
    expiration_time: str
    condition: str
    permalink: str
    thumbnail_id: str
    thumbnail: str
    pictures: List[Picture]
    video_id: Optional[str]
    descriptions: List[str]
    accepts_mercadopago: bool
    non_mercado_pago_payment_methods: List[str]
    shipping: Shipping
    international_delivery_mode: str
    seller_address: Address
    seller_contact: Optional[str]
    location: Optional[Dict[str, str]]
    geolocation: Dict[str, float]
    coverage_areas: List[str]
    attributes: List[Attribute]
    warnings: List[str]
    listing_source: str
    variations: List[str]
    status: str
    sub_status: List[str]
    tags: List[str]
    warranty: str
    catalog_product_id: Optional[str]
    domain_id: str
    seller_custom_field: str
    parent_item_id: Optional[str]
    differential_pricing: Optional[str]
    deal_ids: List[str]
    automatic_relist: bool
    date_created: str
    last_updated: str
    health: float
    catalog_listing: bool
    item_relations: List[str]
    channels: List[str]

class ProductCreate(BaseModel):
    """Criação de um produto do Mercado Livre"""
    title: str = Field(..., title='Título do produto')
    category_id: str = Field(..., title='ID da categoria do produto')
    price: float = Field(..., title='Preço do produto')
    currency_id: str = Field(..., title='ID da moeda do produto')
    available_quantity: int = Field(..., title='Quantidade disponível do produto')
    buying_mode: str = Field(..., title='Modo de compra do produto')
    listing_type_id: str = Field(..., title='ID do tipo de anúncio do produto')
    condition: str = Field(..., title='Condição do produto')
    description: str = Field(..., title='Descrição do produto')
    video_id: Optional[str] = Field(None, title='ID do vídeo do produto')
    warranty: str = Field(..., title='Garantia do produto')
    pictures: List[str] = Field(..., title='Lista de URLs das imagens do produto')
    attributes: List[Attribute] = Field(..., title='Lista de atributos do produto')
    shipping: Shipping = Field(..., title='Informações de envio do produto')
    seller_custom_field: str = Field(..., title='Campo personalizado do vendedor')
    automatic_relist: bool = Field(..., title='Indica se produto será republicado automaticamente')
    catalog_product_id: Optional[str] = Field(None, title='ID do produto no catálogo')
    parent_item_id: Optional[str] = Field(None, title='ID do item pai')
    deal_ids: List[str] = Field(..., title='Lista de IDs de ofertas')
    price: float = Field(..., title='Preço do produto')
    currency_id: str = Field(..., title='ID da moeda do produto')
    available_quantity: int = Field(..., title='Quantidade disponível do produto')
    buying_mode: str = Field(..., title='Modo de compra do produto')
    listing_type_id: str = Field(..., title='ID do tipo de anúncio do produto')
    condition: str = Field(..., title='Condição do produto')
    description: str = Field(..., title='Descrição do produto')
    video_id: Optional[str] = Field(None, title='ID do vídeo do produto')
    warranty: str

class ProductUpdate(BaseModel):
    """Atualização de um produto do Mercado Livre"""
    status: Optional[str] = Field(None, title='Status do produto')
    price: Optional[float] = Field(None, title='Preço do produto')
    available_quantity: Optional[int] = Field(None, title='Quantidade disponível do produto')
    images: Optional[List[Picture]] = Field(None, title='Lista de URLs das imagens do produto')
    attributes: Optional[List[Attribute]] = Field(None, title='Lista de atributos do produto')

class Snapshot(BaseModel):
    """Informações da imagem da descrição do produto do Mercado Livre"""
    url: str
    width: int
    height: int
    status: str

class ProductDescription(BaseModel):
    """Descrição de um produto do Mercado Livre"""
    text: str = Field(..., title='Descrição do produto')
    plain_text: str = Field(..., title='Descrição do produto em texto puro')
    last_updated: str = Field(..., title='Data da última atualização da descrição')
    date_created: str = Field(..., title='Data de criação da descrição')
    snapshot: Snapshot = Field(..., title='Informações da imagem da descrição')
