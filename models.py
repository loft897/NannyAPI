from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

# Définition de la classe NannyModel héritant de la classe models.Model
class NannyModel(models.Model):
    # Définition des attributs de la classe
    id = fields.IntField(pk=True)  # Champ d'identifiant en lecture seule
    city = fields.CharField(max_length=250) # Champ pour la ville
    full_name = fields.CharField(max_length=250) # Champ pour le nom complet
    home_number = fields.CharField(max_length=250) # Champ pour le numéro de téléphone fixe
    mobile_number = fields.CharField(max_length=250) # Champ pour le numéro de téléphone portable
    email = fields.CharField(max_length=250) # Champ pour l'adresse e-mail
    adress = fields.CharField(max_length=250) # Champ pour l'adresse
    nb_places = fields.IntField(max_lenght=2) # Champ pour le nombre de places disponibles

    # Définition de la classe PydanticMeta (utilisée pour la sérialisation Pydantic)
    class PydanticMeta:
        pass

# Définition de la classe MamModel héritant de la classe models.Model
class MamModel(models.Model):
    # Définition des attributs de la classe
    id = fields.IntField(pk=True) # Champ d'identifiant en lecture seule
    city = fields.CharField(max_length=250) # Champ pour la ville
    name = fields.CharField(max_length=250) # Champ pour le nom
    phone = fields.CharField(max_length=250) # Champ pour le numéro de téléphone
    email = fields.CharField(max_length=250) # Champ pour l'adresse e-mail
    adress = fields.CharField(max_length=250) # Champ pour l'adresse
    nb_nannies = fields.IntField(max_lenght=2) # Champ pour le nombre d'assistantes maternelles
    nannies_list = fields.JSONField() # Champ pour la liste d'assistantes maternelles

    # Définition de la classe PydanticMeta (utilisée pour la sérialisation Pydantic)
    class PydanticMeta:
        pass

# Création de la classe Pydantic pour le modèle NannyModel
NannyModel_pydantic = pydantic_model_creator(NannyModel, name="NannyName")
# Création de la classe Pydantic pour l'entrée de NannyModel
NannyModelIn_pydantic = pydantic_model_creator(NannyModel, name="NannyIn", exclude_readonly=False)

# Création de la classe Pydantic pour le modèle MamModel
MamModel_pydantic = pydantic_model_creator(MamModel, name="MamName")
# Création de la classe Pydantic pour l'entrée de MamModel
MamModelIn_pydantic = pydantic_model_creator(MamModel, name="MamIn", exclude_readonly=False)
# Le paramètre exclude_readonly=True spécifie que le modèle TodoIn_pydantic ne doit pas inclure le champ id, car il s'agit d'un champ en lecture seule (il est généré automatiquement par la base de données et ne doit pas être modifié par l'utilisateur).

