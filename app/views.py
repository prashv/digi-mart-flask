from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from app.models import Product, Review

products = Blueprint('products',__name__, template_folder='templates')


class ListView(MethodView):

    def get(self):
        products = Product.objects.all()
        return render_template('products/list.html', products=products)


class DetailView(MethodView):

    form = model_form(Review, exclude=['created_at'])

    def get_context(self, slug):
        product = Product.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "product": product,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('products/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            review = Review()
            form.populate_obj(review)

            product = context.get('product')
            product.reviews.append(review)
            product.save()

            return redirect(url_for('products.detail', slug=slug))
        return render_template('products/detail.html', **context)


# Register the urls
products.add_url_rule('/', view_func=ListView.as_view('list'))
products.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
