from django.db import models


class Persona(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    is_on_vacation = models.BooleanField(default=False)

    def __str__(self):
        return self.name
