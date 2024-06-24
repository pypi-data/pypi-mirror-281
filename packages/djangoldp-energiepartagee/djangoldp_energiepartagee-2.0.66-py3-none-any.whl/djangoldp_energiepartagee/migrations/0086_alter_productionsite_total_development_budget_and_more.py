# Generated by Django 4.2.7 on 2024-04-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0085_citizenproject_wp_project_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionsite',
            name='total_development_budget',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Budget total de développement'),
        ),
        migrations.AlterField(
            model_name='productionsite',
            name='total_investment_budget',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Budget total d'investissement"),
        ),
        migrations.AlterField(
            model_name='productionsite',
            name='yearly_turnover',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Chiffre d'affaire annuel"),
        ),
    ]
