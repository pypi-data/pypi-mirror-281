# Generated by Django 4.2.7 on 2024-04-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0086_alter_productionsite_total_development_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionsite',
            name='progress_status',
            field=models.CharField(blank=True, max_length=248, null=True, verbose_name='Progress status'),
        ),
    ]
