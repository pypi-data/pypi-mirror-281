# Generated by Django 4.2.11 on 2024-05-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("djangoldp_energiepartagee", "0119_sapermission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productionsite",
            name="total_development_budget",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=50,
                null=True,
                verbose_name="Budget total de développement",
            ),
        ),
        migrations.AlterField(
            model_name="productionsite",
            name="total_investment_budget",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=50,
                null=True,
                verbose_name="Budget total d'investissement",
            ),
        ),
    ]
