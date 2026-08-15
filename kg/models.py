from django.db import models

# Create your tests here.
class Review(models.Model):
    RATING_CHOICES = [
        (0, 'No Review Yet'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    comment = models.TextField()
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or self.post.title} - {self.rating} Review"


class NeedHelp(models.Model):
    sender_name = models.CharField('full name', max_length=100)
    email_adress = models.EmailField(max_length=50)
    message = models.TextField()
    subject = models.CharField(max_length=100)
    
    def __str__(self):
        return self.sender_name
    
class Developers(models.Model):
    name = models.CharField(max_length=150, unique=True)
    remark = models.CharField(max_length=20, choices=[('regularized', 'Regularized'),('not-regularized', 'Not Regularized'), ('recent', 'New')], default='recent')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
       return self.name

class Site(models.Model):
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.TextField()
    lga = models.CharField(max_length=50)
    remark = models.CharField(max_length=50, default=None)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
       return self.name
