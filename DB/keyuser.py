from tortoise import fields, models

class KeyUser(models.Model):
    user_id = fields.BigIntField()      
    key_gen = fields.CharField(max_length=800)      
    key_status = fields.CharField(max_length=800)  
    status = fields.CharField(max_length=800)  
    expiry = fields.IntField()  
    antispam = fields.IntField()  
    userid = fields.BigIntField()  

    class Meta:
        table = "key_user"      

    def __str__(self):
        return f"KeyUser {self.user_id} ({self.key_gen})"
