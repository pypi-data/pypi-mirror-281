# Generated by Django 2.2.24 on 2022-02-03 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0063_auto_20220128_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='djangoldp_energiepartagee.Actor', verbose_name='Acteur'),
        ),
        migrations.AlterField(
            model_name='relatedactor',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='djangoldp_energiepartagee.Actor', verbose_name='Acteur'),
        ),
        migrations.AlterField(
            model_name='relatedactor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
