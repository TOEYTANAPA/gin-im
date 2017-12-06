# in project/app/context_processors.py
from mainapp.models import Profile

def profile(request):
	profile_picture=""
	try :
		profile_picture = Profile.objects.get(user=request.user).picture.url
	except:
		pass
	return {'profile': profile_picture} # of course some filter here