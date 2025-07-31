from tortoise import fields, models

class Delta(models.Model):
    estado = fields.IntField()  
    nombre = fields.CharField(max_length=100)  
    razon = fields.CharField(max_length=5000)  

    class Meta:
        table = "delta" 

    def __str__(self):
        return f"Delta {self.nombre} ({self.estado})"
