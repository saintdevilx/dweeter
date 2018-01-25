from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import dweet_manager


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follower_count = models.IntegerField(default=0)
	following_count = models.IntegerField(default=0)
	dweet_count = models.IntegerField(default=0)

	def __str__(self):
		return "%s's profile"%self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Dweet(models.Model):
	""" Dweet - """
	# text length restricted to 150 chars
	dweet_text = models.CharField(max_length = 150)  
	
	# no of likes
	likes_count = models.IntegerField(default=0,blank=True)	
	
	#no of replied
	replies_count = models.IntegerField(default=0,blank=True) 

 	# reply of the dweet 	
	parent = models.ForeignKey( 'self', null=True ,blank=True ) 

	#user
	user = models.ForeignKey(User, blank=True)

	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%s"%self.dweet_text

	def save(self,*args, **kwargs):
		is_new =True if not self.id else False
		super(Dweet,self).save()

		if is_new:
			if self.parent:
				self.parent.replies_count +=1
				self.parent.save()			
			dweet_manager.add_dweet_to_follower( self)
			dweet_manager.update_dweet_count(self)




class Like(models.Model):
	""" Dweet Like """
	#dweet liked
	dweet = models.ForeignKey(Dweet )
	#liked by user
	user = models.ForeignKey(User, blank=True)

	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "like to %s by %s"%(dweet,user)

	def save(self,*args,**kwargs):
		is_new =True if not self.id else False
		super(Like,self).save(*args,**kwargs)
		if is_new:
			dweet_manager.add_like(self)


class Follower(models.Model):
	followee = models.ForeignKey(User, related_name='followee')
	follower = models.ForeignKey(User, related_name='follower',blank=True)
	confirm = models.BooleanField(default=False,blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		super(Follower,self).save(*args, **kwargs)
		dweet_manager.add_follower(self)


class TimelineDweet(models.Model):
	user = models.ForeignKey(User)
	dweet = models.ForeignKey(Dweet)
