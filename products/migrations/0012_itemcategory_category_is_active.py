# Generated by Django 5.0.2 on 2024-02-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_supply_revision_supply'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategory',
            name='category_is_active',
            field=models.BooleanField(default=False),
        ),
    ]
