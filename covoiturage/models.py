from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class Trajet(models.Model):
    conducteur = models.CharField(max_length=100)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    # Stockés sous forme de chaînes comme défini dans votre fixture
    date_depart = models.CharField(max_length=10)  # Ex: "2026-11-14"
    heure_depart = models.CharField(max_length=5)   # Ex: "07:00"
    
    # Validateur de bas niveau Django pour interdire < 1 place
    nbr_place = models.IntegerField(validators=[MinValueValidator(1)])
    prix_place = models.IntegerField() # En francs CFA

    def __str__(self):
        # Conversion de la chaîne "2026-11-14" en objet date pour la formater en "14/11/2026"
        date_obj = datetime.strptime(self.date_depart, "%Y-%m-%d")
        date_formatee = date_obj.strftime("%d/%m/%Y")
        return f"{self.ville_depart} → {self.ville_arrivee}, le {date_formatee} à {self.heure_depart}."


class Reservation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="reservations")
    passager = models.CharField(max_length=100)
    nbr_place = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # CONTRAINTE UNIQUE DE BAS NIVEAU : Empêche un passager de dupliquer sa réservation sur un même trajet
        unique_together = ('trajet', 'passager')

    def __str__(self):
        return f"{self.passager} : {self.nbr_place} places."
