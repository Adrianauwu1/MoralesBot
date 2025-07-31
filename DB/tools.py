from tortoise import fields, models

class Tool(models.Model):
    name = fields.CharField(max_length=200)     
    comand = fields.CharField(max_length=200)   
    status = fields.IntField()  
    razon = fields.CharField(max_length=200, null=True)  
    review = fields.CharField(max_length=200, null=True)  
    type = fields.CharField(max_length=200)  

    class Meta:
        table = "tools"     

    def __str__(self):
        return f"Tool {self.name} ({self.type})"
