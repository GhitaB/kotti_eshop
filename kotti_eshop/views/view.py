# -*- coding: utf-8 -*-
from kotti_settings.util import get_setting
from pyramid.exceptions import PredicateMismatch
from pyramid.view import view_config


@view_config(name='shopping_cart', permission='view',
             renderer='kotti_eshop:templates/shopping-cart.pt')
def shopping_cart(self, request):
    """ Shopping cart view
    """
    if not self.backend_products:
        raise PredicateMismatch()
    else:
        backend_product = self.backend_products[0]
    if request.user:
        logged_in_user = request.user.name
    else:
        logged_in_user = ''
    return {'logged_in_user': logged_in_user,
            'backend_product': backend_product}


@view_config(name='shop_admin', permission='view',
             renderer='kotti_eshop:templates/shop-admin-view.pt')
def shop_admin_view(self):
    """ Shop administration panel
    """
    return {'shop_products_per_page': get_setting('shop_products_per_page'),
            'shop_currency': get_setting('shop_currency'),
            'products': []}


@view_config(name='shop_view', permission='view',
             renderer='kotti_eshop:templates/shop-view.pt')
def shop_view(self):
    """ Shop view
    """
    return {'shop_products_per_page': get_setting('shop_products_per_page'),
            'shop_currency': get_setting('shop_currency'),
            'products': []}
