# Generated by Django 5.0.2 on 2024-02-20 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_soldweightitemproxy_p_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solditem',
            name='item_in_storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_data', to='products.item'),
        ),
    ]