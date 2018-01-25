class DweetManager:

	def __init__(self):
		pass

	def add_dweet_to_follower(self, dweet):
		from .models import TimelineDweet
		followers = self.get_users_follower(dweet.user)

		timeline =[ TimelineDweet(dweet=dweet, user = follower.follower)  for follower in followers]
		#add dweet to poster timeline as well
		timeline.append( TimelineDweet(dweet=dweet, user=dweet.user) )

		TimelineDweet.objects.bulk_create(timeline)

	def get_users_follower(self,user):
		from .models import Follower
		return Follower.objects.filter(followee = user)

	def add_follower(self,follow):
		follower = follow.follower
		followee = follow.followee

		#update follower count for user followed 
		self.update_follower(followee)
		#update following count user following
		self.update_following(follower)

		from .models import Dweet, TimelineDweet

		dweets = Dweet.objects.filter(user = followee)
		# Add all the dweets of followee to follower timeline
		timeline=[ TimelineDweet(dweet=dweet, user=follower) for dweet in dweets]

		TimelineDweet.objects.bulk_create( timeline )

	def update_follower(self,followee, count=1):
		""" update follower count when user has new follower"""
		profile = followee.userprofile
		profile.follower_count+= count
		profile.save()

	def update_following(self,follower, count=1):
		""" update following count when user follow someone"""
		profile =follower.userprofile
		profile.following_count+= count
		profile.save()		

	def get_user_dweet(self,user):
		return Dweet.objects.filter().order_by('-created')

	def add_like(self,like, count=1):
		"""  """
		like.dweet.likes_count +=count
		like.dweet.save()

	def update_dweet_count(self, dweet):
		""" update dweet count when user add new dweet  """
		profile = dweet.user.userprofile
		profile.dweet_count +=1
		profile.save()


class TimelineManager:
	""" Timeline manager to populate timeline for a user  """
	def get_timeline_dweet(self,user,dweet_id=None):
		from .models import TimelineDweet
		timeline = TimelineDweet.objects
		timeline = timeline.filter(dweet__parent_id = dweet_id) if dweet_id else timeline		
		return timeline.filter(user=user).order_by('-dweet__created')

dweet_manager = DweetManager()