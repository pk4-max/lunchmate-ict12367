from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar       = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio          = models.TextField(blank=True)
    display_name = models.CharField(max_length=100, blank=True, verbose_name='ชื่อที่แสดงในโพสต์')

    def __str__(self):
        return self.display_name or self.user.username

class LunchPost(models.Model):
    MEAL_CHOICES = [
        ('เช้า', 'เช้า'),
        ('กลางวัน', 'กลางวัน'),
        ('เย็น', 'เย็น'),
        ('ดึก', 'ดึก'),
    ]
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image       = models.ImageField(upload_to='posts/', blank=True, null=True)
    name        = models.CharField(max_length=100)
    restaurant  = models.CharField(max_length=200)
    area        = models.CharField(max_length=200, blank=True)
    meal        = models.CharField(max_length=20, choices=MEAL_CHOICES, default='กลางวัน')
    time        = models.CharField(max_length=10)
    slots       = models.IntegerField(default=4)
    joined      = models.IntegerField(default=1)
    note        = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant} — {self.name}"

    class Meta:
        ordering = ['-created_at']