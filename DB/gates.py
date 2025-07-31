from tortoise import fields, models

class Gates(models.Model):
    name = fields.CharField(max_length=800)  
    type = fields.CharField(max_length=800)  
    comand = fields.CharField(max_length=800)  
    gate_type = fields.CharField(max_length=800)  
    status = fields.IntField()  
    reviewed = fields.CharField(max_length=400, null=True)  
    razon = fields.CharField(max_length=800, null=True)  
    pasarela = fields.CharField(max_length=800, null=True)  
    creditos = fields.CharField(max_length=45, null=True)  
    plan_aceptado = fields.CharField(max_length=45, null=True)  
    num_uso = fields.BigIntField()  

    class Meta:
        table = "gates"     

    def __str__(self):
        return f"Gates {self.name} ({self.gate_type})"
