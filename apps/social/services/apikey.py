from apps.social.models import Apikey
from datetime import datetime

def set_api_key(user):
    """
    This function sets api_key for a user
    :param user: user models
    """
    key = str(user.username)+str(datetime.now())