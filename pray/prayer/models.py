from django.db import models

# Create your models here.
class Prayer(models.Model):
	prayer_id = models.BigAutoField(primary_key=True,unique=True)
	prayer_title = models.CharField(max_length=100, blank=False, null=False)
	prayer_request_date = models.DateTimeField(null=False)
	prayer_description = models.CharField(max_length=1000,null=False)
	prayer_count = models.IntegerField(null=False)
