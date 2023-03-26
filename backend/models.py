from django.db import models

from users_app.models import User



class Event(models.Model):
    date = models.DateTimeField(
        auto_now_add=True
    )
    # event = models.TextField(
    #     null=True,
    #     max_length=500,
    # )
    hours = models.IntegerField(
        default=0,
        null=True,
    )
    minutes = models.IntegerField(
        default=0,
        null=True,
    )
    visits = models.IntegerField(
        default=0,
        null=True,
    )
    publications = models.IntegerField(
        default=0,
        null=True,
    )
    films = models.IntegerField(
        default=0,
        null=True,
    )
    studies = models.IntegerField(
        default=0,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    # result = models.IntegerField(
    #     default=0,
    #     null=True,
    # )

    def __str__(self) -> str:
        return str(self.date)[:16] 



class EventsHistory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    event = models.TextField(
        null=True,
        max_length=500,
    )
    hours = models.IntegerField(
        default=0,
    )
    minutes = models.IntegerField(
        default=0,
    )
    visits = models.IntegerField(
        default=0,
    )
    publications = models.IntegerField(
        default=0,
    )
    films = models.IntegerField(
        default=0,
    )
    studies = models.IntegerField(
        default=0,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    month = models.ForeignKey(
        'Months',
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.date)[:16]


class HoursResult(models.Model):
    date = models.CharField(
        null=True,
        max_length=20,
    )
    hours = models.IntegerField(
        default=0,
    )
    minutes = models.IntegerField(
        default=0,
    )
    visits = models.IntegerField(
        default=0,
    )
    publications = models.IntegerField(
        default=0,
    )
    films = models.IntegerField(
        default=0,
    )
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     null=True,
    # )

    def __str__(self) -> str:
        return str(self.hours) or ' '


class Months(models.Model):
    date = models.CharField(
        null=True,
        max_length=20,
    )
    hours = models.IntegerField(
        default=0,
    )
    minutes = models.IntegerField(
        default=0,
    )
    visits = models.IntegerField(
        default=0,
    )
    publications = models.IntegerField(
        default=0,
    )
    films = models.IntegerField(
        default=0,
    )
    studies = models.IntegerField(
        default=0,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )  

    def __str__(self) -> str:
        return str(self.id)    


class Image (models.Model):
    name = models.CharField(
        max_length=20,
        null=True,
    )  
    image = models.ImageField(
        upload_to=('maps')
    )  

    def __str__(self) -> str:
        return str(self.name) 


class Calendar(models.Model):
    date = models.CharField(
        max_length=20,
        null=True,
    )  
    action = models.CharField(
        max_length=200,
        null=True,
    )
    person = models.CharField(
        max_length=200,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    ) 
    congregation = models.CharField(
        max_length=30,
        null=True,
    )
    time = models.CharField(
        max_length=30,
        null=True,
    )
    at_time = models.CharField(
        max_length=30,
        null=True,
    )
    groupe = models.CharField(
        max_length=5,
        null=True,
    )
    icon = models.CharField(
        max_length=30,
        null=True,
    )
    topic = models.CharField(
        max_length=26,
        null=True,
    )
    place = models.CharField(
        max_length=26,
        null=True,
    )


    def __str__(self) -> str:
        return str(self.date)
    
class PlacesStand(models.Model):
    name = models.CharField(
        max_length=26,
        null=True,
    )
    congregation = models.CharField(
        max_length=50,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.id)