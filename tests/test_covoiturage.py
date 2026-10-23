from django.db import IntegrityError
from django.core.exceptions import ValidationError
from covoiturage.models import Trajet,Reservation
import pytest

@pytest.fixture
def trajet_valide(db):
    return Trajet.objects.create(
        conducteur="Ali",
        ville_depart="Sokodé",
        ville_arrivee="Lomé",
        date_depart="2026-10-18",
        heure_depart="18:00",
        nbr_place=3,
        prix_place=10000
    )

def test_covoiturage_d_un_trajet(db):
    
    assert trajet_valide.conducteur
    assert trajet_valide.ville_depart
    assert trajet_valide.ville_arrivee
    assert trajet_valide.date_depart
    assert trajet_valide.heure_depart
    assert trajet_valide.places
    assert trajet_valide.prix_place


def test_si_trajet_sans_place_renvoyer_une_exeption(db):
    trajet_invalide=Trajet.objects.create(
        conducteur="Ali",
        ville_depart="Sokodé",
        ville_arrivee="Lomé",
        date_depart="2026-10-18",
        heure_depart="18:00",
        nbr_place=0,
        prix_place=10000
    )
    with pytest.raises(ValidationError):
        trajet_invalide.full_clean()
        trajet_valide.save()


def test_trajet_affiche_depart_arriver_date(db):

    assert str(trajet_valide) == "sokode - lome le 2026-10-18 à 18:00 "
    
    
def test_creer_une_reservation_avec_info_ratacher_a_un_trajet(db):

    reservation = Reservation.objects.create(
        passager="affo",
        nbr_place=2,
        trajet=trajet_valide,
    )

    assert reservation.trajet_valide.ville_depart == "sokode"
    assert reservation.trajet_valide.ville_arrivee == "lome"
    assert reservation.trajet_valide.date_depart == "2026-10-18"
    assert reservation.trajet_valide.heure_depart == "18:00"
    assert reservation.nbr_place == 2
    assert reservation.passager == "affo"   


def test_affichage_d_une_reservation(db):
    
    reservation=Reservation.object.create(
        passager="Youssif",
        nbr_place=2,
        trajet=trajet_valide
    )

    assert str(reservation) == "Youssif : 2 places."

def test_un_passager_ne_reserve_pas_deux_fois_le_meme_trajet(db):
    Reservation.object.create(
        passager="Youssif",
        nbr_place=1,
        trajet=trajet_valide
    )

    second_res=Reservation(
        passager="Youssif",
        nbr_place=1,
        trajet=trajet_valide
    )

    with pytest.raises(IntegrityError):
        second_res.save()