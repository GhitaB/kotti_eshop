from kotti.resources import DBSession
from kotti_eshop.resources import BackendProduct
from pyramid.exceptions import PredicateMismatch
from pyramid.view import view_config


@view_config(name='shopping_cart', permission='view',
             renderer='kotti_eshop:templates/shopping-cart.pt')
def shopping_cart(context, request):
    """ Shopping cart view
    """

    has_backend_products = DBSession.query(BackendProduct.id).count()

    if not has_backend_products:
        raise PredicateMismatch()

    backend_product = None
    if context.backend_products:
        backend_product = context.backend_products[0]

    if request.user:
        logged_in_user = request.user.name
    else:
        logged_in_user = ''

    return {'logged_in_user': logged_in_user,
            'backend_product': backend_product}


@view_config(name='shop_view', permission='view',
             renderer='kotti_eshop:templates/shop-view.pt')
def shop_view(self):
    """ Shop view
    """
    return {}
