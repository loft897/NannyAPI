from typing import Union
# importation des modules nécessaires
from fastapi import FastAPI, HTTPException
from typing import Optional
from typing import List
import uvicorn
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel
from models import NannyModel, NannyModel_pydantic, NannyModelIn_pydantic, MamModel, MamModel_pydantic, MamModelIn_pydantic

# création d'une classe pour un message qui sera retourné dans les réponses
class Message(BaseModel):
    message : str

# initialisation de l'application FastAPI
app = FastAPI()

# route pour un message de bienvenue à l'adresse racine
welcome_message = 'Bienvenue sur Nanny! Entrer /api ou /api/nannies pour avoir tous les assistants maternels à domicile ou /api/mams pour avoir tous les assistants maternels en mam'
@app.get("/")
async def Welcome():
    return welcome_message


# route pour un message de bienvenue à l'adresse racine
@app.get("/api")
async def Welcome_api():
    return {"Bienvenue sur la Nanny API"}




@app.get("/api/nannies")
async def get_nannies(id: Union[int, None] = None, city: Union[str, None] = None):
    if id is not None:
        # récupération de l'objet dans la base de données à partir de son id
        nanny = await NannyModelIn_pydantic.from_queryset_single(NannyModel.get(id=id))
        if nanny is not None:
            # Retourne la représentation en Pydantic de l'objet récupéré avec l'id donné
            return nanny
        else:
            # Retourne une erreur 404 si l'id ne correspond à aucune nounou dans la base de données
            raise HTTPNotFoundError(detail="Nanny not found")

    elif city is not None:
        # Initialisation d'une liste vide pour stocker les nounous de la ville donnée
        nannies = []
        # Itération sur toutes les instances de la classe NannyModel
        for nanny in await NannyModelIn_pydantic.from_queryset(NannyModel.all()):
            # Vérification si la ville donnée correspond à la ville de la nounou
            if f'{city}'.upper() == nanny.city:
                # Ajout de la nounou à la liste des nounous de la ville donnée
                nannies.append(nanny)
        # Renvoi de la liste des nounous de la ville donnée
        return nannies

    else:
        # Si ni l'id ni la ville n'ont été spécifiés, retourne toutes les nounous sous forme de liste
        nannies = await NannyModelIn_pydantic.from_queryset(NannyModel.all())
        return nannies


# route pour créer une nouvelle nounou
@app.post("/api/nannies/create", response_model=NannyModel_pydantic)
async def create(nanny: NannyModelIn_pydantic):
    # création d'un objet dans la base de données à partir des données reçues dans la requête
    obj = await NannyModel.create(**nanny.dict(exclude_unset=True))
    # retourne une représentation en Pydantic de l'objet créé
    return await NannyModel_pydantic.from_tortoise_orm(obj)

# route pour mettre à jour les infos d'une nounou
@app.put("/api/nannies/{id}", response_model=NannyModel_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_nanny(id: int, nanny: NannyModelIn_pydantic):
    # mise à jour de l'objet dans la base de données à partir de son id et des données reçues dans la requête
    await NannyModel.filter(id = id).update(**nanny.dict(exclude_unset=True))
    # récupération de l'objet mis à jour et retourne une représentation en Pydantic de l'objet récupéré
    print(await NannyModel_pydantic.from_queryset_single(NannyModel.get(id = id)))

# route pour supprimer une nounou
@app.delete("/api/nannies/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_nanny(id: int):
    # récupération de l'objet à supprimer dans la base de données à partir de son id
    delete_obj = await NannyModel.filter(id=id).first()
    # si aucun objet n'a été trouvé, retourne une exception
    if not delete_obj:
        raise HTTPException(status_code=404, detail="Nanny not found in DB")
    # sinon, supprime l'objet et retourne un message de succès
    await delete_obj.delete()
    return Message(message="Successfully deleted")





@app.get("/api/mams")
async def get_mams(id: Union[int, None] = None, city: Union[str, None] = None):
    if id:
        # récupération de l'objet dans la base de données à partir de son id et retourne une représentation en Pydantic de l'objet récupéré
        return await MamModelIn_pydantic.from_queryset_single(MamModel.get(id=id))
    elif city:
        # Initialisation d'une liste vide pour stocker les mams de la ville donnée
        mams = []
        # Itération sur toutes les instances de la classe MamModel
        for mam in await MamModelIn_pydantic.from_queryset(MamModel.all()):
            # Vérification si la ville donnée correspond à la ville de la mam
            if f'{city}'.upper() == mam.city:
                # Ajout de la mam à la liste des mams de la ville donnée
                mams.append(mam)
        # Renvoi de la liste des mams de la ville donnée
        return mams
    else:
        # Si ni l'id ni la ville n'ont été spécifiés, ron retourne toute la liste
        return await MamModelIn_pydantic.from_queryset(MamModel.all())


# route pour créer une nouvelle mam
@app.post("/api/mams/create", response_model=MamModel_pydantic)
async def create(mam: MamModelIn_pydantic):
    # création d'un objet dans la base de données à partir des données reçues dans la requête
    obj = await MamModel.create(**mam.dict(exclude_unset=True))
    # retourne une représentation en Pydantic de l'objet créé
    return await MamModel_pydantic.from_tortoise_orm(obj)

# route pour mettre à jour les infos d'une mam
@app.put("/api/mams/{id}", response_model=MamModel_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_mam(id: int, mam: MamModelIn_pydantic):
    # mise à jour de l'objet dans la base de données à partir de son id et des données reçues dans la requête
    await MamModel.filter(id = id).update(**mam.dict(exclude_unset=True))
    # récupération de l'objet mis à jour et retourne une représentation en Pydantic de l'objet récupéré
    print(await MamModel_pydantic.from_queryset_single(MamModel.get(id = id)))

# route pour supprimer une nounou
@app.delete("/api/mams/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_mam(id: int):
    # récupération de l'objet à supprimer dans la base de données à partir de son id
    delete_obj = await MamModel.filter(id=id).first()
    # si aucun objet n'a été trouvé, retourne une exception
    if not delete_obj:
        raise HTTPException(status_code=404, detail="mam not found in DB")
    # sinon, supprime l'objet et retourne un message de succès
    await delete_obj.delete()
    return Message(message="Successfully deleted")




# configuration de la base de données à l'aide de Tortoise ORM
register_tortoise(
    app,
    db_url="sqlite://store.db", # URL de la base de données SQLite
    modules={'models': ['models']}, # spécification des modèles de la base de données
    generate_schemas=True, # génération automatique des schémas de la base de données
    add_exception_handlers=True # ajout des gestionnaires d'exceptions pour une meilleure gestion des erreurs
)


 