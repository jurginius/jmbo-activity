from django.conf import settings

from django.utils.translation import ugettext_lazy as _


ACTIVITY_SIGNED_UP = 0
ACTIVITY_LOGGED_IN = 1
ACTIVITY_SENT_OFF_SITE_INVITE = 2
ACTIVITY_SENT_FRIEND_REQUEST = 3
ACTIVITY_ACCEPTED_FRIEND_REQUEST = 4
ACTIVITY_ESTABLISHED_FRIENDSHIP = 5
ACTIVITY_DECLINED_FRIENDSHIP = 6
ACTIVITY_REVOKED_FRIENDSHIP = 7
ACTIVITY_EARNED_BADGE = 8
ACTIVITY_POSTED = 9
ACTIVITY_UPLOADED_IMAGE = 10
ACTIVITY_COMMENTED = 11
ACTIVITY_LIKED = 12
ACTIVITY_UPDATED_AVATAR = 13
ACTIVITY_UPDATED_PROFILE = 14
ACTIVITY_SENT_MESSAGE = 15
ACTIVITY_SOCIAL_SHARE = 16
ACTIVITY_POLL_VOTE = 17

ACTIVITY_CHOICES = (('Jmbo', (
        (ACTIVITY_SIGNED_UP, _('Signed up')),
        (ACTIVITY_LOGGED_IN, _('Logged in')),
        (ACTIVITY_SENT_OFF_SITE_INVITE, _('Sent an off-site invite')),
        (ACTIVITY_SENT_FRIEND_REQUEST, _('Sent friend request')),
        (ACTIVITY_ACCEPTED_FRIEND_REQUEST, _('Accepted friend request')),
        (ACTIVITY_ESTABLISHED_FRIENDSHIP, _('Established friendship')),
        (ACTIVITY_DECLINED_FRIENDSHIP, _('Declined friendship')),
        (ACTIVITY_REVOKED_FRIENDSHIP, _('Revoked friendship')),
        (ACTIVITY_EARNED_BADGE, _('Earned badge')),
        (ACTIVITY_POSTED, _('Added a blog post')),
        (ACTIVITY_UPLOADED_IMAGE, _('Uploaded Image')),
        (ACTIVITY_COMMENTED, _('Added a comment')),
        (ACTIVITY_LIKED, _('Liked')),
        (ACTIVITY_UPDATED_AVATAR, _('Updated your avatar')),
        (ACTIVITY_UPDATED_PROFILE, _('Updated your profile')),
        (ACTIVITY_SENT_MESSAGE, _('Sent a message')),
        (ACTIVITY_SOCIAL_SHARE, _('Shared via social a network')),
        (ACTIVITY_POLL_VOTE, _('Voted in a poll')),
    )
),)

# add activity constants in other apps
if hasattr(settings, 'ACTIVITY_APPS'):
    vals = dict(ACTIVITY_CHOICES[0][1])
    for app in settings.ACTIVITY_APPS:
        module = __import__("%s.constants" % app)
        module = getattr(module, "constants")
        for ac in module.ACTIVITY_CHOICES:
            if ac[0] in vals:
                raise ValueError("(%d, %s) clashes with (%d, %s)" % (ac[0], unicode(ac[1]), ac[0], unicode(vals[ac[0]])))
            vals[ac[0]] = ac[1]
        ACTIVITY_CHOICES += ((app.capitalize(), module.ACTIVITY_CHOICES),)
