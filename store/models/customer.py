from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Unique username
    password = models.CharField(max_length=6)  # Change to allow longer passwords
    email = models.EmailField(unique=True)  # Add email field
    date_of_birth = models.DateField()  # Add date of birth field
    gender = models.CharField(max_length=10)  # Add gender field
    address = models.TextField()  # Add address field
    city = models.CharField(max_length=50)  # Add city field
    contact_no = models.CharField(max_length=15)  # Add contact number field
    paypal_id = models.CharField(max_length=100)  # Add PayPal ID field


    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(contact_no=self.contact_no):
            return True
        else:
            return False


    def __str__(self):
        return self.username
