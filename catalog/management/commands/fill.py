from django.core.management import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('category.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_read_products():
        with open('product.json', encoding='utf-8') as json_file:
            return json.load(json_file)

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Category.truncate_table_restart_id()
        Product.objects.all().delete()

        product_list = []
        category_list = []

        for category in Command.json_read_categories():
            category_list.append(
                {"id": category['pk'], "name": category['fields']['name'],
                 "description": category['fields']['description']}
            )
        category_for_create = []

        for category_item in category_list:
            category_for_create.append(
                Category.objects.create(**category_item)
            )

        for product in Command.json_read_products():
            product_list.append(
                {"id": product['pk'], "name": product['fields']['name'],
                 "description": product['fields']['description'],
                 "picture": product['fields']['picture'],
                 "purchase_price": product['fields']['purchase_price'],
                 "category": Category.objects.get(pk=product['fields']['category']),
                 "created_at": product['fields']['created_at'],
                 "updated_at": product['fields']['updated_at']}
            )
        product_for_create = []

        for product_item in product_list:
            product_for_create.append(
                Product.objects.create(**product_item)
            )

        Category.objects.bulk_create(category_for_create)
        Product.objects.bulk_create(product_for_create)
