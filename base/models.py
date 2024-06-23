from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Base(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Loan(Base):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Customer(Base):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    loans = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='user_loan')
    total_loan_amount = models.IntegerField(default=0)
    already_paid = models.IntegerField(default=0)
    have_to_paid = models.IntegerField(default=0)
    dp = models.FileField(upload_to='dp', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name




class Document(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='customer-documents')




class Payment(Base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount} by {self.customer.name} on {self.payment_date}"


    
class TotalLoan(Base):
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.amount)

class TotalTake(Base):
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.amount)




@receiver(post_save, sender=Customer)
def after_creating(sender, instance, created, **kwargs):
    if created:
        loan_amount = instance.total_loan_amount
        TotalLoan.objects.create(amount=loan_amount)
    else:
        TotalTake.objects.create(amount=instance.already_paid)