# Generated by Django 4.2.11 on 2024-03-12 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0076_alter_actor_options_alter_college_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'default_permissions': {'change', 'delete', 'view', 'add', 'control'}, 'ordering': ['pk']},
        ),
    ]
