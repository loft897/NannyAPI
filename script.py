import json
import httpx


# Charger le fichier JSON avec les données des listes d'assistants maternels a domicile
with open('files/grand_nannies.json', 'r') as file:
    nannies_data = json.load(file)
    nanny = nannies_data[0][2:][0]

    v = 0
    for i in range(len(nannies_data)):
        for j in range(len(nannies_data[i])):
            for nanny in nannies_data[i][0].keys():
                print(nanny)
                


    # print(nanny)
    # print("city : ", nannies_data[0][0])
    # print("full_name : ", list(nannies_data[0][2:][0].keys())[0])
    # print("home_number : ", list(nannies_data[0][2:][0].values())[0]['home'])
    # print("mobile_number : ", list(nannies_data[0][2:][0].values())[0]['mobile'])
    # print("email : ", list(nannies_data[0][2:][0].values())[0]['email'])
    # print("adress : ", list(nannies_data[0][2:][0].values())[0]['adress'])
    # print("nb_places : ", list(nannies_data[0][2:][0].values())[0]['nb_places'])

# Charger le fichier JSON avec les données des listes d'assistants maternels en mam
with open('files/grand_mam.json', 'r') as file:
    mam_data = json.load(file)
    mam = mam_data[0]
    

# print(response.json())
# print(response.status_code)

def AddNanny(nanny):
    url = "http://127.0.0.1:8000/api/mams/create"
    payload = {
                "city": "string",
                "full_name": "string",
                "home_number": "string",
                "mobile_number": "string",
                "email": "string",
                "adress": "string",
                "nb_places": 2147483647
}

    response = httpx.post(url, json=payload)
    return response

def AddMam(mam):
    url = "http://127.0.0.1:8000/api/mams/create"
    payload = {
        "city": list(mam.values())[0]['city'],
        "name": list(mam.keys())[0],
        "phone": list(mam.values())[0]['phone'],
        "email": list(mam.values())[0]['email'],
        "adress": list(mam.values())[0]['adress'],
        "nb_nannies": list(mam.values())[0]['nb_nannies'],
        "nannies_list": list(mam.values())[0]['nannies_list']
    }

    response = httpx.post(url, json=payload)
    return response






