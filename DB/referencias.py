from tortoise import fields, models

class Referencia(models.Model):
    USERID = fields.CharField(max_length=400)
    USERNAME = fields.CharField(max_length=400)
    NICK = fields.CharField(max_length=400)
    FILE_ID = fields.CharField(max_length=400)
    RANDOM = fields.CharField(max_length=400)
    MENSAJE = fields.CharField(max_length=400)

    class Meta:
        table = "Referencias"   

    def __str__(self):
        return f"Referencia {self.ID} ({self.USERNAME})"
