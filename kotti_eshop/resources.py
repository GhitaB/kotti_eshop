# -*- coding: utf-8 -*-

from kotti_eshop import _
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Base
from kotti.resources import Content
from kotti.resources import DBSession
from kotti.resources import Image
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from zope.interface import implements


shopproduct_productmaterials_table = Table(
    'shopproduct_productmaterials', Base.metadata,
    Column('shopproduct_id', Integer, ForeignKey("shopproduct.id"),
           primary_key=True),
    Column('productmaterial_id', Integer, ForeignKey("productmaterial.id"),
           primary_key=True)
)

shopproduct_producttopics_table = Table(
    'shopproduct_producttopics', Base.metadata,
    Column('shopproduct_id', Integer, ForeignKey("shopproduct.id"),
           primary_key=True),
    Column('producttopic_id', Integer, ForeignKey("producttopic.id"),
           primary_key=True)
)

shopproduct_productcategories_table = Table(
    'shopproduct_productcategories', Base.metadata,
    Column('shopproduct_id', Integer, ForeignKey("shopproduct.id"),
           primary_key=True),
    Column('productcategory_id', Integer, ForeignKey("productcategory.id"),
           primary_key=True)
)

shopproduct_productages_table = Table(
    'shopproduct_productages', Base.metadata,
    Column('shopproduct_id', Integer, ForeignKey("shopproduct.id"),
           primary_key=True),
    Column('productage_id', Integer, ForeignKey("productage.id"),
           primary_key=True)
)


def _categorization_find_or_create(factory, kw):
    with DBSession.no_autoflush:
        keyword = factory.query.filter_by(title=kw).first()
    if keyword is None:
        keyword = factory(title=kw)
        DBSession.add(keyword)
    return keyword


class ProductCategory(Base):
    """ A shop_product can be saved in one or more product_categories
    """
    __tablename__ = 'productcategory'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512), nullable=False)

    def __init__(self, title):
        self.title = title

    shopproducts = relationship(
        'ShopProduct',
        secondary=shopproduct_productcategories_table,
        backref="shopproduct_categories")


class ProductMaterial(Base):
    """ A shop_product can be made of one ore more product_materials
    """
    __tablename__ = 'productmaterial'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512), nullable=False)

    shopproducts = relationship(
        'ShopProduct',
        secondary=shopproduct_productmaterials_table,
        backref="shopproduct_materials")

    def __init__(self, title):
        self.title = title


class ProductTopic(Base):
    """ A shop_product can be added in one ore more product_topics
    """
    __tablename__ = 'producttopic'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512), nullable=False)

    shopproducts = relationship(
        'ShopProduct',
        secondary=shopproduct_producttopics_table,
        backref="shopproduct_topics")

    def __init__(self, title):
        self.title = title


class ProductAge(Base):
    """ A shop_product can be recommended for one ore more product_ages
    """
    __tablename__ = 'productage'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(512), nullable=False)

    def __init__(self, title):
        self.title = title

    shopproducts = relationship(
        'ShopProduct',
        secondary=shopproduct_productages_table,
        backref="shopproduct_ages")


class ProductImage(Image):
    """ An image added to a product """

    __tablename__ = 'productimage'

    # add your columns
    id = Column(Integer, ForeignKey('images.id'), primary_key=True)

    type_info = Image.type_info.copy(
        name=u'ProductImage',
        title=_(u'ProductImage'),
        add_view=u'add_image',
        addable_to=[u'ShopProduct'],
    )

    def __init__(self, **kwargs):
        super(ProductImage, self).__init__(**kwargs)


class Shop(Content):
    """ An eShop in this website
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    type_info = Content.type_info.copy(
        name=u'Shop',
        title=_(u'Shop'),
        add_view=u'add_shop',
        addable_to=['Document', ],)

    def get_all_products(self):
        """ Returns all products in this shop """
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.parent_id == self.id)
        return products

    def get_all_productcategories(self):
        """ Returns all categories items """
        categories = DBSession.query(ProductCategory)
        return categories

    def get_all_productmaterials(self):
        """ Returns all materials items """
        materials = DBSession.query(ProductMaterial)
        return materials

    def get_all_producttopics(self):
        """ Returns all topics items """
        topics = DBSession.query(ProductCategory)
        return topics

    def get_all_productages(self):
        """ Returns all ages items """
        ages = DBSession.query(ProductAge)
        return ages

    def get_products_by_category(self, category):
        """ Returns products for a given category
        """
        all_products = self.get_all_products()
        products = []
        for product in all_products:
            if category in product.categories:
                products.append(product)
        return products

    def get_products_by_topic(self, topic):
        """ Returns products for a given topic
        """
        all_products = self.get_all_products()
        products = []
        for product in all_products:
            if topic in product.topics:
                products.append(product)
        return products

    def get_products_by_material(self, material):
        """ Returns products for a given material
        """
        all_products = self.get_all_products()
        products = []
        for product in all_products:
            if material in product.materials:
                products.append(product)
        return products

    def get_products_by_age(self, age):
        """ Returns products for a given age
        """
        all_products = self.get_all_products()
        products = []
        for product in all_products:
            if age in product.ages:
                products.append(product)
        return products


class ShopOrder(Content):
    """ An order in eShop
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    # id_user -> who is the client
    # id_product or list of products?
    # id_coupon - maybe was a special offer?
    # paymethod - paypal or something
    # currency
    # amount decimal(14,3)
    # ip_address
    # pay_date
    # support_date
    # status
    # notes
    type_info = Content.type_info.copy(
        name=u'ShopOrder',
        title=_(u'ShopOrder'),
        add_view=u'add_order',
        addable_to=['Shop', ],)


class ShopClient(Content):
    """ A client for this eShop
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    # email
    # paypal_email
    # deliver_address
    # status
    # last_ip_login
    type_info = Content.type_info.copy(
        name=u'ShopClient',
        title=_(u'ShopClient'),
        add_view=u'add_client',
        addable_to=['Shop', ],)


class ShopProduct(Content):
    """ A product in this eShop
    """
    __tablename__ = 'shopproduct'

    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    price = Column(Float())
    price_offer = Column(Float())
    expires_offer_date = Column(Date())
    support_days = Column(Integer())
    featured = Column(Boolean())
    status = Column(String())

    producttopics = association_proxy(
        'shopproduct_topics',
        'title',
        creator=lambda v: _categorization_find_or_create(ProductTopic, v)
    )
    productmaterials = association_proxy(
        'shopproduct_materials',
        'title',
        creator=lambda v: _categorization_find_or_create(ProductMaterial, v)
    )
    productcategories = association_proxy(
        'shopproduct_categories',
        'title',
        creator=lambda v: _categorization_find_or_create(ProductCategory, v)
    )

    productages = association_proxy(
        'shopproduct_ages',
        'title',
        creator=lambda v: _categorization_find_or_create(ProductAge, v)
    )

    type_info = Content.type_info.copy(
        name=u'ShopProduct',
        title=_(u'ShopProduct'),
        add_view=u'add_product',
        addable_to=['Shop', ],)

    def __init__(self, **kwargs):
        super(ShopProduct, self).__init__(**kwargs)

        for attr in ['materials', 'categories', 'topics', 'ages']:
            val = kwargs.get(attr)
            if val:
                setattr(self, attr, val)

    def get_all_images(self):
        """ Returns all images added to this product """
        images = DBSession.query(Image).filter(
            Image.parent_id == self.id)

        return images


class CustomContent(Content):
    """ A custom content type. """

    implements(IDefaultWorkflow)

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    custom_attribute = Column(Unicode(1000))

    type_info = Content.type_info.copy(
        name=u'CustomContent',
        title=_(u'CustomContent'),
        add_view=u'add_custom_content',
        addable_to=[u'Document'],
        selectable_default_views=[
            ("alternative-view", _(u"Alternative view")),
        ],
    )

    def __init__(self, custom_attribute=None, **kwargs):
        """ Constructor

        :param custom_attribute: A very custom attribute
        :type custom_attribute: unicode

        :param **kwargs: Arguments that are passed to the base class(es)
        :type **kwargs: see :class:`kotti.resources.Content`
        """

        super(CustomContent, self).__init__(**kwargs)

        self.custom_attribute = custom_attribute
