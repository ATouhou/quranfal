from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def login_callback(sender, user, request, **kwargs):
    # logger = logging.getLogger(__name__)
    # logger.info("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
    print("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
    request.session['learning'] = True
    request.session['display_word_meanings'] = False



@receiver(user_logged_out)
def logout_callback(sender, user, request, **kwargs):
    # logger = logging.getLogger(__name__)
    # logger.info("user logged out: %s at %s" % (user, request.META['REMOTE_ADDR']))
    print("user logged out: %s at %s" % (user, request.META['REMOTE_ADDR']))
