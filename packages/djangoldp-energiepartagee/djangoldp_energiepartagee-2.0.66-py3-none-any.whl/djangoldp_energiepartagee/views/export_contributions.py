import csv
import validators

from django.http import HttpResponse
from djangoldp.models import Model
from rest_framework.views import APIView

from djangoldp.views import NoCSRFAuthentication


# export csv - Old button (export selected lines)
class ExportContributions(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        response = super(ExportContributions, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get("origin")
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = (
            "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        )
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response["User"] = request.user.webid()
            except AttributeError:
                pass
        return response

    def post(self, request):
        delimiter_type = ";"
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export_actors.csv"'

        writer = csv.writer(response, delimiter=delimiter_type)
        for urlid in request.data:
            # Check that the array entries are URLs
            if validators.url(urlid):
                model, instance = Model.resolve(urlid)

        if request.method == "POST" and request.data and isinstance(request.data, list):
            fields = [
                "Nom court de l'acteur",
                "Nom long de l'acteur",
                "Adresse",
                "Complément d'adresse",
                "Code Postal",
                "Ville",
                "Région",
                "Réseau Régional",
                "Collège EPA",
                "Collège RR",
                "nom représentant légal",
                "prénom représentant légal",
                "mail représentant légal",
                "téléphone représentant légal",
                "nom contact de gestion",
                "prénom contact de gestion",
                "mail contact de gestion",
                "téléphone contact de gestion",
                "Colis accueil envoyé",
                "Inscrit sur espace Adh",
                "Inscrit sur liste Adh",
                "Inscrit sur liste régional",
                "e-mail espace adhérent",
                "Catégorie de cotisant",
                "Nombre d'habitants",
                "Nombre d'employés",
                "Chiffre d'affaires",
                "SIREN ou RNA",
                "Année de cotisation",
                "Montant à payer",
                "Date de paiement",
                "Paiement reçu par",
                "Moyen de paiement",
                "Etat de la cotisation",
                "Numéro de reçu",
                "Pourcentage de ventilation",
                "Bénéficiaire de la ventilation",
                "Date de paiement de la part ventilée",
                "Numéro de facture de la ventilation",
                "Nom “Animateur régional contact”",
                "Prénom “Animateur régional contact”",
                "Type d'acteur",
                "Structure juridique",
                "Adhérent sur l’année en cours",
                "Signataire de la charte EP",
                "Visible sur la carte",
                "Adhérent depuis",
            ]
            writer.writerow(fields)

            for urlid in request.data:
                # Check that the array entries are URLs
                if validators.url(urlid):
                    model, instance = Model.resolve(urlid)
                    if instance and instance.actor:

                        if instance.actor.shortname:
                            actor_shortname = instance.actor.shortname
                        else:
                            actor_shortname = ""

                        if instance.actor.longname:
                            actor_longname = instance.actor.longname
                        else:
                            actor_longname = ""

                        if instance.actor.address:
                            actor_address = instance.actor.address
                        else:
                            actor_address = ""

                        if instance.actor.complementaddress:
                            actor_complementaddress = instance.actor.complementaddress
                        else:
                            actor_complementaddress = ""

                        if instance.actor.postcode:
                            actor_postcode = instance.actor.postcode
                        else:
                            actor_postcode = ""

                        if instance.actor.city:
                            actor_city = instance.actor.city
                        else:
                            actor_city = ""

                        if instance.actor.region.name:
                            actor_region = instance.actor.region.name
                        else:
                            actor_region = ""

                        if instance.actor.regionalnetwork.name:
                            actor_regionalnetwork = instance.actor.regionalnetwork.name
                        else:
                            actor_regionalnetwork = ""

                        if instance.actor.collegeepa:
                            collegeepa = instance.actor.collegeepa.name
                        else:
                            collegeepa = ""

                        if instance.actor.college:
                            college = instance.actor.college.name
                        else:
                            college = ""

                        legalrepresentant_last_name = ""
                        legalrepresentant_first_name = ""
                        legalrepresentant_email = ""
                        legalrepresentant_phone = ""
                        if instance.actor.legalrepresentant:
                            if instance.actor.legalrepresentant.last_name:
                                legalrepresentant_last_name = (
                                    instance.actor.legalrepresentant.last_name
                                )

                            if instance.actor.legalrepresentant.first_name:
                                legalrepresentant_first_name = (
                                    instance.actor.legalrepresentant.first_name
                                )

                            if instance.actor.legalrepresentant.email:
                                legalrepresentant_email = (
                                    instance.actor.legalrepresentant.email
                                )

                            if instance.actor.legalrepresentant.profile.phone:
                                legalrepresentant_phone = (
                                    instance.actor.legalrepresentant.profile.phone
                                )

                        managementcontact_last_name = ""
                        managementcontact_first_name = ""
                        managementcontact_email = ""
                        managementcontact_phone = ""
                        if instance.actor.managementcontact:
                            if instance.actor.managementcontact.last_name:
                                managementcontact_last_name = (
                                    instance.actor.managementcontact.last_name
                                )

                            if instance.actor.managementcontact.first_name:
                                managementcontact_first_name = (
                                    instance.actor.managementcontact.first_name
                                )

                            if instance.actor.managementcontact.email:
                                managementcontact_email = (
                                    instance.actor.managementcontact.email
                                )

                            if instance.actor.managementcontact.profile.phone:
                                managementcontact_phone = (
                                    instance.actor.managementcontact.profile.phone
                                )

                        if instance.actor.college:
                            college = instance.actor.college.name
                        else:
                            college = ""

                        packagestep = ""
                        adhspacestep = ""
                        adhliststep = ""
                        regionalliststep = ""
                        if instance.actor.integrationstep:
                            if instance.actor.integrationstep.packagestep == True:
                                packagestep = "Non"
                            else:
                                packagestep = "Oui"

                            if instance.actor.integrationstep.adhspacestep == True:
                                adhspacestep = "Non"
                            else:
                                adhspacestep = "Oui"

                            if instance.actor.integrationstep.adhliststep == True:
                                adhliststep = "Non"
                            else:
                                adhliststep = "Oui"

                            if instance.actor.integrationstep.regionalliststep == True:
                                regionalliststep = "Non"
                            else:
                                regionalliststep = "Oui"

                        if instance.paymentdate:
                            paymentdate = instance.paymentdate.strftime("%d-%m-%Y")
                        else:
                            paymentdate = ""

                        if instance.receivedby:
                            receivedby = instance.receivedby.name
                        else:
                            receivedby = ""

                        if instance.paymentmethod:
                            paymentmethod = instance.paymentmethod
                        else:
                            paymentmethod = ""

                        if instance.actor.category == "collectivite":
                            category = "Collectivités"
                        elif instance.actor.category == "porteur_dev":
                            category = "Porteurs de projet en développement"
                        elif instance.actor.category == "porteur_exploit":
                            category = "Porteurs de projet en exploitation"
                        else:
                            category = "Partenaires"

                        if instance.numberpeople:
                            numberpeople = instance.numberpeople
                        else:
                            numberpeople = ""

                        if instance.numberemployees:
                            numberemployees = instance.numberemployees
                        else:
                            numberemployees = ""

                        if instance.turnover:
                            turnover = instance.turnover
                        else:
                            turnover = ""

                        if instance.actor.siren:
                            siren = instance.actor.siren
                        else:
                            siren = ""

                        if instance.year:
                            year = instance.year
                        else:
                            year = ""

                        if instance.amount:
                            amount = instance.amount
                        else:
                            amount = ""

                        if instance.contributionstatus == "appel_a_envoye":
                            status = "Appel à envoyer"
                        elif instance.contributionstatus == "appel_ok":
                            status = "Appel envoyé"
                        elif instance.contributionstatus == "relance":
                            status = "Relancé"
                        elif instance.contributionstatus == "a_ventiler":
                            status = "A ventiler"
                        else:
                            status = "Validé"

                        if instance.paymentdate and instance.receivedby:
                            receiptnumber = (
                                str(instance.receivedby.code)
                                + "-"
                                + str(instance.year)
                                + "-"
                                + str(instance.contributionnumber)
                            )
                        else:
                            receiptnumber = ""

                        if instance.ventilationto:
                            ventilationto = instance.ventilationto.name
                        else:
                            ventilationto = ""

                        if instance.ventilationdate:
                            ventilationdate = instance.ventilationdate.strftime(
                                "%d-%m-%Y"
                            )
                        else:
                            ventilationdate = ""

                        if instance.callcontact:
                            callcontactname = instance.callcontact.last_name
                            callcontactfirstname = instance.callcontact.first_name
                        else:
                            callcontactname = ""
                            callcontactfirstname = ""

                        if instance.actor.legalstructure:
                            legalstructure = instance.actor.legalstructure.name
                        else:
                            legalstructure = ""

                        if instance.actor.adhmail:
                            adhmail = instance.actor.adhmail
                        else:
                            adhmail = ""

                        if instance.actor.actortype == "soc_citoy":
                            actortype = "Sociétés Citoyennes"
                        elif instance.actor.actortype == "collectivite":
                            actortype = "Collectivités"
                        elif instance.actor.actortype == "structure":
                            actortype = "Structures d’Accompagnement"
                        else:
                            actortype = "Partenaires"

                        if instance.actor.renewed == True:
                            renewed = "Oui"
                        elif instance.actor.renewed == False:
                            renewed = "Non"
                        else:
                            renewed = "Inconnu"

                        if instance.actor.signataire == True:
                            signataire = "Oui"
                        elif instance.actor.signataire == False:
                            signataire = "Non"
                        else:
                            signataire = "Inconnu"

                        if instance.actor.visible == True:
                            visible = "Oui"
                        else:
                            visible = "Non"

                        if instance.actor.adhesiondate:
                            adhesiondate = instance.actor.adhesiondate
                        else:
                            adhesiondate = ""

                        writer.writerow(
                            [
                                actor_shortname,
                                actor_longname,
                                actor_address,
                                actor_complementaddress,
                                actor_postcode,
                                actor_city,
                                actor_region,
                                actor_regionalnetwork,
                                collegeepa,
                                college,
                                legalrepresentant_last_name,
                                legalrepresentant_first_name,
                                legalrepresentant_email,
                                legalrepresentant_phone,
                                managementcontact_last_name,
                                managementcontact_first_name,
                                managementcontact_email,
                                managementcontact_phone,
                                packagestep,
                                adhspacestep,
                                adhliststep,
                                regionalliststep,
                                adhmail,
                                category,
                                numberpeople,
                                numberemployees,
                                turnover,
                                siren,
                                year,
                                amount,
                                paymentdate,
                                receivedby,
                                paymentmethod,
                                status,
                                receiptnumber,
                                instance.ventilationpercent,
                                ventilationto,
                                ventilationdate,
                                instance.factureventilation,
                                callcontactname,
                                callcontactfirstname,
                                actortype,
                                legalstructure,
                                renewed,
                                signataire,
                                visible,
                                adhesiondate,
                            ]
                        )

        if response:
            return response

        return HttpResponse("Not Found")
