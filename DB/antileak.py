from tortoise import fields, models

class Antileak(models.Model):
    userid = fields.BigIntField()  
    cc = fields.CharField(max_length=45)  
    mes = fields.CharField(max_length=45)  
    ano = fields.CharField(max_length=45)  
    total = fields.CharField(max_length=45)  

    class Meta:
        table = "antileak"  

    def __str__(self):
        return f"Antileak {self.userid} - {self.total}"
