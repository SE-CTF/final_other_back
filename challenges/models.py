from django.db import models


class Challenge(models.Model):
    CATEGORY_CHOICES = (
        ('crypto', 'Cryptography'),
        ('cracking', 'Cracking'),
        ('network', 'Network'),
        ('forensics', 'Forensics'),
        ('stegano', 'Steganography')
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=False)
    score = models.IntegerField(blank=False)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, blank=False, default=CATEGORY_CHOICES[0])
    flag = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.title


class Hint(models.Model):
    description = models.TextField()
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='hints')

    def __str__(self):
        return self.description
