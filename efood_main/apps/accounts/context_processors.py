from django.conf import settings

from .models import UserProfile


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:  # noqa: E722
        user_profile = None
    return dict(user_profile=user_profile)


def get_google_api(request):
    return {"GOOGLE_MAP_API": settings.GOOGLE_MAP_API}
