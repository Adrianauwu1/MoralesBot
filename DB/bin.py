from tortoise import fields, models

class Bin(models.Model):
    bin = fields.BigIntField()  
    baned = fields.BooleanField()  

    class Meta:
        table = "bin"  

    def __str__(self):
        return f"Bin {self.bin} (Banned: {self.baned})"
