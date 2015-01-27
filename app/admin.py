from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from app.auth import requires_auth
from app.models import Product, Review, User

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Product

    def get(self):
        products = self.cls.objects.all()
        return render_template('admin/list.html', products=products)


class Detail(MethodView):

    decorators = [requires_auth]
    # Map post types to models
    class_map = {
        'product': Product,
    }

    def get_context(self, slug=None):

        if slug:
            product = Product.objects.get_or_404(slug=slug)
            # Handle old posts types as well
            cls = product.__class__ if product.__class__ != Product else Product
            form_cls = model_form(cls,  exclude=('created_at', 'reviews'))
            if request.method == 'POST':
                form = form_cls(request.form, inital=product._data)
            else:
                form = form_cls(obj=product)
        else:
            # Determine which post type we need
            cls = self.class_map.get(request.args.get('type', 'product'))
            product = cls()
            form_cls = model_form(cls,  exclude=('created_at', 'reviews'))
            form = form_cls(request.form)
        context = {
            "product": product,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            product = context.get('product')
            form.populate_obj(product)
            product.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
