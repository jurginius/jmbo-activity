"""
Cronable script to report user activity stats broken down by month.

"""
from django.core.management.base import BaseCommand

from datetime import date
from django.db.models import Count
from activity.models import UserActivity
from activity import constants

class Command(BaseCommand):
    """
    Reports monthly activity stats
    """
    def handle(self, *args, **options):
        activities = {}
        for app in constants.ACTIVITY_CHOICES:
            activities = dict(activities.items() + 
                [(activity[0], "%s: %s" % 
                    (app[0].upper(), unicode(activity[1])))
                        for activity in app[1]])
        months = UserActivity.objects.dates('created', 'month')
        for month in months:
            qs = UserActivity.objects.filter(created__gte=month).filter(
                created__lt=date(month.year, month.month+1, month.day) 
                    if month.month < 12
                    else date(month.year+1, 1, month.day))
            res = qs.values('activity').annotate(count=Count('activity'))
            self.stdout.write('Month: %u %u\n' % (month.year, month.month))
            l = [(activities[x['activity']], x['count']) for x in res]
            l.sort()
            for activity in l:
                self.stdout.write('\t%s: %u\n' % (activity[0], activity[1]))
