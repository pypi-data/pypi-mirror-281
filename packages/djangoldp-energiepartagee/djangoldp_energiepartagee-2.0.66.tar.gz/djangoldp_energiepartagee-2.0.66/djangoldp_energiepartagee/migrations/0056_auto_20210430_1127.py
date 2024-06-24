# Generated by Django 2.2.19 on 2021-04-30 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0055_auto_20210421_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrationstep',
            name='adhliststep',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Non inscrit sur liste Adh'),
        ),
        migrations.AlterField(
            model_name='integrationstep',
            name='adhspacestep',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Non inscrit sur espace Adh'),
        ),
        migrations.AlterField(
            model_name='integrationstep',
            name='packagestep',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Colis accueil à envoyer'),
        ),
        migrations.AlterField(
            model_name='integrationstep',
            name='regionalliststep',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Non inscrit sur liste régional'),
        ),
    ]
