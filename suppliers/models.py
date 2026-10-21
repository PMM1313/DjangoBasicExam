


from django.db import models


class Supplier(models.Model): # dostavchik za inventory
    name = models.CharField(max_length=150, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    # maybe more categories like website ...

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

