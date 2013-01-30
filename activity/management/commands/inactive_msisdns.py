"""
Export MSISDNs of SMS-opted-in users who did no activity in the past 30 days.
"""

from django.core.management.base import BaseCommand

from datetime import date, timedelta
from activity.models import UserActivity
from foundry.models import Member

DAYS = 30

class Command(BaseCommand):
    def handle(self, *args, **options):
        # get members who are opted in to SMS but haven't logged in for 30 days
        relevant_members = Member.objects.filter(receive_sms=True).exclude(
                last_login__gte=date.today() + timedelta(-DAYS))
        self.stderr.write('Opted in members: %u\n' % 
                relevant_members.count())
        relevant_msisdns = [x[0] for x in relevant_members.values_list(
            'mobile_number')]

        # get activities in the last 30 days
        recent_activities = UserActivity.objects.filter(
                created__gte=date.today() + timedelta(-DAYS))
        self.stderr.write('Activity records: %u\n' % recent_activities.count())
        active_msisdns = [x[0] for x in recent_activities.values_list(
            'user__member__mobile_number')]
        for msisdn in active_msisdns:
            if msisdn in relevant_msisdns:
                relevant_msisdns.remove(msisdn)

        self.stderr.write('Opted in inactive msisdns: %u\n' % 
                len(relevant_msisdns))
        for msisdn in relevant_msisdns:
            print msisdn
