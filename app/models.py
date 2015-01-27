import datetime
from flask import url_for
from app import db

class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email_id = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=20, required=True)
    username = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)

    def get_absolute_url(self):
        return url_for('user', kwargs={"slug":self.slug})

    def __unicode__(self):
        return self.username

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class Product(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    brand = db.StringField(max_length=255, required=True)
    product = db.StringField(max_length=255, required=True)
    sub_product = db.StringField(max_length=255, required=True)
    barcode = db.StringField(max_length=255, required=True)
    variant = db.StringField(max_length=255, required=True)
    category = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    reviews = db.ListField(db.EmbeddedDocumentField('Review'))

    def get_absolute_url(self):
        return url_for('product', kwargs={"slug":self.slug})

    def __unicode__(self):
        return self.product

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class Review(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Review", required=True)
    username = db.StringField(verbose_name="Username", max_length=255, required=True)
