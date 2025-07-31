from tortoise import fields, models

class Grupo(models.Model):
    group_id = fields.BigIntField()     
    autorizado = fields.IntField()      
    name = fields.CharField(max_length=800)  
    username = fields.CharField(max_length=800)  
    Inicio = fields.CharField(max_length=200)  
    Fin = fields.CharField(max_length=200)  
    userid = fields.BigIntField()  
    level = fields.CharField(max_length=45)  

    class Meta:
        table = "grupos"    

    def __str__(self):
        return f"Grupo {self.group_id} ({self.name})"
