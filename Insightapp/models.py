from django.db import models

# Create your models here.

class SearchHistory(models.Model):
    search_text = models.CharField(max_length=500)
    searched_at = models.DateTimeField(auto_now_add=True)
