from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import profile
from django.core.mail import send_mail
from django.conf import settings

#receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profiles = profile.objects.create(
            user=user,
            username=user.username,
            email = user.email,
            name = user.first_name,
        )
        subject ='welcome to DevSearch' 
        message ='We are glad you are here!' 
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profiles.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    print ('user updated!')
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteuser(sender, instance, **kwargs):
    print ('user deleted!')
    user = instance.user
    user.delete() 

post_save.connect(CreateProfile,sender=User)
post_save.connect(updateUser,sender=profile)
post_delete.connect(deleteuser, sender=profile)