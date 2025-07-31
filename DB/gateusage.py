from tortoise import fields, models

class GateUsage(models.Model):
    gate = fields.ForeignKeyField("models.Gates", related_name="usos", on_delete=fields.CASCADE)
    date = fields.DateField(auto_now_add=True)  
    count = fields.IntField(default=0)      

    class Meta:
        table = "gate_usage"
        unique_together = ("gate", "date")  
