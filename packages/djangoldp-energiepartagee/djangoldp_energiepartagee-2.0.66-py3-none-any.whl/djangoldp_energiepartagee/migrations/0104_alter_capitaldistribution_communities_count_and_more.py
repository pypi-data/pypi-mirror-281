# Generated by Django 4.2.7 on 2024-05-05 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0103_remove_capitaldistribution_individuals_capital_resident_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitaldistribution',
            name='communities_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de collectivités'),
        ),
        migrations.AlterField(
            model_name='capitaldistribution',
            name='individuals_count',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'actionnaires personnes physiques"),
        ),
        migrations.AlterField(
            model_name='capitaldistribution',
            name='individuals_count_resident',
            field=models.IntegerField(blank=True, null=True, verbose_name="Nombre d'actionnaires résidents"),
        ),
        migrations.AlterField(
            model_name='capitaldistribution',
            name='neighboring_communities_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nombre de collectivités résidentes'),
        ),
    ]
