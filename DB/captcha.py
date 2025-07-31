from tortoise import fields, models

class Captcha(models.Model):
    captcha_id = fields.IntField(pk=True, auto_increment=True)  
    user_id = fields.BigIntField()  
    captcha_text = fields.CharField(max_length=255)  
    captcha_image = fields.CharField(max_length=255) 
    captcha_status = fields.IntField()  
    timestamp = fields.DatetimeField()  

    class Meta:
        table = "captcha" 

    def __str__(self):
        return f"Captcha {self.captcha_id} (User {self.user_id})"
