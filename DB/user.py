from tortoise import fields, models
 
class User(models.Model):
    userid = fields.BigIntField(pk=True)    
    role = fields.CharField(max_length=400, null=True)  
    username = fields.CharField(max_length=800, null=True)  
    credits = fields.IntField(default=0)  
    antispam = fields.IntField(default=0)  
    DInicio = fields.CharField(max_length=400, null=True)  
    DFinal = fields.CharField(max_length=400, null=True)  
    DRegistro = fields.CharField(max_length=400, null=True)  
    last_message = fields.DatetimeField(null=True)  
    firstname = fields.CharField(max_length=800, null=True)  
    baned = fields.BooleanField(default=False)      
    apodo = fields.CharField(max_length=500, null=True)  
    razon = fields.CharField(max_length=500, null=True)  
    total_messages = fields.IntField(default=0)  
    nivel = fields.CharField(max_length=45, null=True)  
    cc_count = fields.IntField(default=0)  
    cc_count_limit = fields.IntField(default=0)  
    language = fields.CharField(max_length=400, null=True, default='es') 
    
    class Meta:
        table = "persons"   

    def __str__(self):
        return f"User {self.userid} ({self.username})"
