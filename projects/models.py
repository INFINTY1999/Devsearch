from django.db import models
import uuid
from users.models import profile
from django.db.models.deletion import CASCADE                 
# Create your models here.

class project (models.Model):
    owner = models.ForeignKey(profile,on_delete=CASCADE,null=True, blank=True)
    Title = models.CharField(max_length=200)
    Discription= models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True,default='default.jpg')
    Demo_link = models.CharField(max_length=2000,null=True,blank=True)
    Source_link = models.CharField(max_length=2000,null=True,blank=True)
    Tags = models.ManyToManyField('Tag',blank=True)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self) :
        return self.Title
    
    class Meta :
        ordering = ['-vote_ratio','-vote_total']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__Id',flat=True)
        return queryset

    @property
    def getvotecount(self):
        Reviews = self.review_set.all()
        upvalue = Reviews.filter(value='up').count()
        totalvotes = Reviews.count()
        ratio = (upvalue/totalvotes)*100
        self.vote_total = totalvotes
        self.vote_ratio = ratio
        
        self.save()


class Review (models.Model):
    Vote_Type = (
        ('up' , 'up vote'),
        ('down' , 'down vote'),
    )
    owner = models.ForeignKey(profile,on_delete=CASCADE,null=True, blank=True)
    project = models.ForeignKey(project, on_delete=CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200,choices=Vote_Type)
    Created = models.DateTimeField(auto_now_add=True)
    Id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta :
        unique_together = [['owner','project']]
    
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    Created = models.DateTimeField(auto_now_add=True)
    Id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return self.name

