"""
Export MSISDNs of SMS-opted-in users who did no activity in the past 30 days.
"""

from django.core.management.base import BaseCommand

from datetime import date, timedelta
from activity.models import UserActivity
from foundry.models import Member

class Command(BaseCommand):
    def handle(self, *args, **options):
        # get members who are opted in to SMS but haven't logged in for 30 days
        relevant_members = set(
                [member.mobile_number for member in Member.objects.filter(
                    receive_sms=True).exclude(
                        last_login__gte=date.today() + timedelta(-30))])
        self.stderr.write('Opted in members: %u\n' % 
                len(relevant_members))

        activities_last30 = UserActivity.objects.filter(
                created__gte=date.today() + timedelta(-30))
        self.stderr.write('Activity records: %u\n' % len(activities_last30))
        for a in activities_last30:
            msisdn = a.user.member.mobile_number
            if msisdn in relevant_members:
                relevant_members.remove(msisdn)

        self.stderr.write('Opted in inactive members: %u\n' % 
                len(relevant_members))
        for msisdn in list(relevant_members):
            print msisdn
