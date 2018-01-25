from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dweet ,Like, TimelineDweet,Follower,UserProfile
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

	first_name = serializers.CharField(max_length=20,required=True)
	last_name = serializers.CharField(max_length=20, required=True)
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
	username = serializers.CharField(
		validators=[UniqueValidator(queryset=User.objects.all())]
	)
	password = serializers.CharField(min_length=8)

	def __init__(self,*args,**kwargs):
		fields = kwargs.get('fields')
		if fields:
			kwargs.pop('fields')
		super(UserSerializer,self).__init__(*args,**kwargs)
		
		if fields:
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


	class Meta:
		model = User
		fields = ('id','first_name','last_name','username','password','email')



class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(fields=['id','first_name','last_name','username'])
	class Meta:
		model = UserProfile
		fields= ('user','follower_count','following_count','dweet_count')


class DweetSerializer(serializers.ModelSerializer):
	user = UserSerializer(fields=['id','first_name','last_name','username'], read_only=True)
	class Meta:
		model = Dweet
		fields = ('dweet_text','user','likes_count','replies_count','created','parent','id')


	def create(self, valid_data):
		return Dweet.objects.create(**valid_data)

	def add_reply(self,valid_data):
		return Dweet.objects.create(**valid_data)


class TimelineDweetSerializer(serializers.Serializer):
	dweet = DweetSerializer( read_only=True)
	user = UserSerializer(fields=['id','first_name','last_name','username'])
	class Meta:
		model = TimelineDweet
		fields =('dweet','user')

		
class FollowerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Follower
		fields = ('followee','follower')

class LikeSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Like
		fields = ('dweet','user')

	def create(self,valid_data):
		obj,status = Like.objects.get_or_create( **valid_data )
		return obj