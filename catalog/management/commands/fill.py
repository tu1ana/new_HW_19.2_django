import json
from pathlib import Path

from django.core.management import BaseCommand

from catalog.models import Product, Category, BlogEntry


class Command(BaseCommand):

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()
        # Version.objects.all().delete()
        BlogEntry.objects.all().delete()

        filepath = Path.cwd() / 'catalog.json'
        with open(filepath, encoding='utf-8') as f:
            data_list = json.load(f)

        products_to_add = []
        categories_to_add = []
        # versions_to_add = []
        blogentries_to_add = []

        for data in data_list:
            data.pop('pk', None)
            if data['model'] == 'catalog.product':
                products_to_add.append(Product(**data['fields']))
            elif data['model'] == 'catalog.category':
                categories_to_add.append(Category(**data['fields']))
            elif data['model'] == 'catalog.blogentry':
                blogentries_to_add.append(BlogEntry(**data['fields']))

        # print(products_to_add)
        # print(categories_to_add)
        # print(versions_to_add)
        # print(blogentries_to_add)

        Product.objects.bulk_create(products_to_add)
        Category.objects.bulk_create(categories_to_add)
        # Version.objects.bulk_create(versions_to_add)
        BlogEntry.objects.bulk_create(blogentries_to_add)
