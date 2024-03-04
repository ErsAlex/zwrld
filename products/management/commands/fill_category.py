from django.core.management.base import BaseCommand
from products.models import ItemCategory
import csv


class Command(BaseCommand):
    help = "initial category creation"

    def handle(self, *args, **options):
        categories = ItemCategory.objects.all()
        if categories.exists():
            self.stdout.write(self.style.SUCCESS("Categories already exist"))
        else:
            with open('products/catalog-all.csv', encoding='utf-8') as file:
                rows = csv.reader(file, delimiter=';', quotechar='"')
                models = []
                for n, category  in enumerate(rows):
                        model = ItemCategory(
                        name = "Default_category",
                        article = category[0],
                        brand = category[1].lstrip(" "),
                        pet_type = category[2],
                        product_type = category[9],
                        weight = int(category[3]),
                        is_dry = bool(int(category[4])),
                        description = category[5].lstrip(" "),
                        importance = category[6],
                        planned_amount = int(category[7]),
                        goods_by_weight = bool(int(category[8])),
                    )
                        models.append(model)
                ItemCategory.objects.bulk_create(models)
                self.stdout.write(self.style.SUCCESS("Categories created"))