from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class NannyModel(models.Model):
    id = fields.IntField(pk=True)
    city = fields.CharField(max_length=250)
    full_name = fields.CharField(max_length=250)
    home_number = fields.CharField(max_length=250)
    mobile_number = fields.CharField(max_length=250)
    email = fields.CharField(max_length=250)
    adress = fields.CharField(max_length=250)
    nb_places = fields.IntField(max_lenght=2)


    class PydanticMeta:
        pass


class MamModel(models.Model):
    id = fields.IntField(pk=True)
    city = fields.CharField(max_length=250)
    name = fields.CharField(max_length=250)
    phone = fields.CharField(max_length=250)
    email = fields.CharField(max_length=250)
    adress = fields.CharField(max_length=250)
    nb_nannies = fields.IntField(max_lenght=2)
    nannies_list = fields.JSONField()


    class PydanticMeta:
        pass

NannyModel_pydantic = pydantic_model_creator(NannyModel, name="NannyName")
NannyModelIn_pydantic = pydantic_model_creator(NannyModel, name="NannyIn", exclude_readonly = True)

MamModel_pydantic = pydantic_model_creator(MamModel, name="MamName")
MamModelIn_pydantic = pydantic_model_creator(MamModel, name="MamIn", exclude_readonly = True)
# Le paramètre exclude_readonly=True spécifie que le modèle TodoIn_pydantic ne doit pas inclure le champ id, car il s'agit d'un champ en lecture seule (il est généré automatiquement par la base de données et ne doit pas être modifié par l'utilisateur).