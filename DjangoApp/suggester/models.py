from django.db import models

class Suggestion(models.Model):
    THAI =  'TH'
    CHINESE = 'CN'
    INDONESIAN = 'ID'
    JAPANESE = 'JP'
    MALAY = 'MY'
    INDIAN = 'IN'
    WESTERN = 'WS'
    DESSERT = 'DS'
    BRUNCH = 'BR'
    FASTFOOD = 'FF'
    KOREAN = 'KR'
    NOTYPE = 'NT'

    CHOICES = (
    (THAI, 'Thai'),
    (CHINESE, 'Chinese'),
    (INDONESIAN, 'Indonesian'),
    (JAPANESE, 'Japanese'),
    (MALAY, 'Malay'),
    (INDIAN, 'Indian'),
    (WESTERN, 'Western'),
    (DESSERT, 'Dessert'),
    (BRUNCH, 'Brunch'),
    (FASTFOOD, 'Fast Food'),
    (KOREAN, 'Korean'),
    (NOTYPE, 'No Type'),
    )

    # Django already defines an automatic incrementing number for primary key, if no field is defined as a primary key
    restaurant_name = models.TextField()
    has_visited = models.BooleanField()
    cuisine_type = models.TextField(choices=CHOICES, default=NOTYPE)

    def __str__(self):
        return self.restaurant_name
