from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all() 
