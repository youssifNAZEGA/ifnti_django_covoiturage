from covoiturage.models import Trajet
import pytest

def test_covoiturage_d_un_trajet(db):
    trajet = Trajet.objects.create(
        conducteur="affo",
        ville_depart="sokode",
        ville_arrivee="lome",
        date_depart="2026-10-18",
        heure_depart="18:00",
        places=4,
        prix_place=4000,
    )

    assert trajet.conducteur
    assert trajet.ville_depart
    assert trajet.ville_arrivee
    assert trajet.date_depart
    assert trajet.heure_depart
    assert trajet.places
    assert trajet.prix_place


def test_si_trajet_sans_place_renvoyer_une_exeption(db):

    with pytest.raises(Exception):
        trajet = Trajet.objects.create(
            conducteur="affo",
            ville_depart="sokode",
            ville_arrivee="lome",
            date_depart="2026-10-18",
            heure_depart="18:00",
            places=0,
            prix_place=3000,
        )


def test_trajet_affiche_depart_arriver_date(db):

    trajet = Trajet.objects.create(
        conducteur="affo",
        ville_depart="sokode",
        ville_arrivee="lome",
        date_depart="2026-10-18",
        heure_depart="18:00",
        places=0,
        prix_place=3000,
    )

    assert str(trajet) == "sokode - lome le 2026-10-18 "
    
    
def test_creer_une_reservation_avec_info_ratacher_a_un_trajet(db):
    trajet = Trajet.objects.create(
        conducteur="affo",
        ville_depart="sokode",
        ville_arrivee="lome",
        date_depart="2026-10-18",
        heure_depart="18:00",
        places=5,
        prix_place=3000,
    )

    reservation = Reservation.objects.create(
        nom="affo",
        nbr_place=2,
        trajet=trajet,
    )

    assert reservation.trajet.ville_depart == "sokode"
    assert reservation.trajet.ville_arrivee == "lome"
    assert reservation.trajet.date_depart == "2026-10-18"
    assert reservation.trajet.heure_depart == "18:00"
    assert reservation.nbr_place == 2
    assert reservation.nom == "affo"   