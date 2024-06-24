# Generated by Django 4.2.11 on 2024-05-13 12:26

from django.db import migrations, models


def update_project_visibility(apps, schema_editor):
    CitizenProject = apps.get_model("djangoldp_energiepartagee", "CitizenProject")
    CommunicationProfile = apps.get_model(
        "djangoldp_energiepartagee", "CommunicationProfile"
    )
    for project in CitizenProject.objects.all():
        try:
            communication_profile = CommunicationProfile.objects.get(
                citizen_project=project
            )
            if communication_profile:
                project.visible = (
                    communication_profile.is_public and project.status == "published"
                )
                project.save()
        except CommunicationProfile.DoesNotExist:
            continue


def update_production_site_visibility(apps, schema_editor):
    ProductionSite = apps.get_model("djangoldp_energiepartagee", "ProductionSite")
    for production_site in ProductionSite.objects.all():
        production_site.visible = production_site.citizen_project.visible
        production_site.save()


class Migration(migrations.Migration):

    dependencies = [
        (
            "djangoldp_energiepartagee",
            "0116_partnerlinktype_alter_partnerlink_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="citizenproject",
            name="visible",
            field=models.BooleanField(
                blank=True,
                default=False,
                null=True,
                verbose_name="Visible sur la carte",
            ),
        ),
        migrations.AddField(
            model_name="productionsite",
            name="visible",
            field=models.BooleanField(
                blank=True,
                default=False,
                null=True,
                verbose_name="Visible sur la carte",
            ),
        ),
        migrations.RunPython(update_project_visibility),
        migrations.RunPython(update_production_site_visibility),
    ]
