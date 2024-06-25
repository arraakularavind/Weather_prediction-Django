from django.db import models

# Create your models here.
class Weather(models.Model):
   city=models.CharField(max_length=100)
   temperature=models.FloatField()
   Feeling_temp=models.FloatField(null=True)
   Min_temp=models.FloatField(null=True)
   Max_temp=models.FloatField(null=True)
   description=models.CharField(max_length=100,null=True)
   icon=models.CharField(max_length=10,null=True)
   humidity=models.IntegerField(null=True)
   wind_speed=models.FloatField(null=True)
   wind_direction=models.IntegerField(null=True)
   uv_index=models.FloatField(null=True)
   air_quality=models.FloatField(null=True)
   date_time=models.DateTimeField(auto_now_add=True)

   def __str__(self):
     return f"{self.city}-{self.date_time}"
        
