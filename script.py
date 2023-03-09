import json
import httpx
from itertools import chain

def AddNanny(nanny, city):
    # URL de l'API pour ajouter une nouvelle nounou
    url = "http://127.0.0.1:8000/api/nannies/create"
    # Création de la charge utile pour la requête POST
    payload = {
                "city": city,
                "full_name": list(nanny.keys())[0],
                "home_number": list(nanny.values())[0]['home'],
                "mobile_number": list(nanny.values())[0]['mobile'],
                "email": list(nanny.values())[0]['email'],
                "adress": list(nanny.values())[0]['adress'],
                "nb_places": list(nanny.values())[0]['nb_places']
                }
    # Envoi de la requête POST avec la charge utile
    response = httpx.post(url, json=payload)
    return response


def AddMam(mam):
    # URL de l'API pour ajouter une nouvelle mam
    url = "http://127.0.0.1:8000/api/mams/create"
    # Création de la charge utile pour la requête POST
    payload = {
        "city": list(mam.values())[0]['city'],
        "name": list(mam.keys())[0],
        "phone": list(mam.values())[0]['phone'],
        "email": list(mam.values())[0]['email'],
        "adress": list(mam.values())[0]['adress'],
        "nb_nannies": list(mam.values())[0]['nb_nannies'],
        "nannies_list": list(mam.values())[0]['nannies_list']
    }
    # Envoi de la requête POST avec la charge utile
    response = httpx.post(url, json=payload)
    return response


# Charger le fichier JSON avec les données des listes d'assistants maternels à domicile
with open('files/grand_nannies.json', 'r') as file:
    nannies_data = json.load(file)
    # Aplatir la liste des données des assistantes maternelles à domicile
    flat_list_nannies = list(chain(*nannies_data))
    # Filtrer les éléments qui sont des dictionnaires
    nannies_list = [item for item in flat_list_nannies if isinstance(item, dict)]
    # Parcourir la liste des nourrices
    for nanny in nannies_list:
        city = ""
        # Trouver la ville associée à la nourrice
        if nanny in flat_list_nannies:
            index = flat_list_nannies.index(nanny)
            items = flat_list_nannies[:index]
            # Parcourir la liste de la fin jusqu'à la deuxième position
            for i in range(len(items)-1, 0, -1):
                if isinstance(items[i], str):
                    city = items[i-1]
                    break

        # # Ajouter la nounou
        # AddNanny(nanny, city)

# Charger le fichier JSON avec les données des assistantes maternelles en MAM
with open('files/grand_mam.json', 'r') as file:
    mam_data = json.load(file)
    # Parcourir la liste des assistantes maternelles en MAM
    # for mam in mam_data:
    #     # Ajouter l'assistante maternelle en MAM
    #     AddMam(mam)

    

# print(response.json())
# print(response.status_code)