import calendar

from django.db.models import Count
from django.utils import timezone
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminRadioSelect, AdminDateWidget
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf.urls.defaults import patterns

from foundry.models import Member
from activity.constants import ACTIVITY_CHOICES
from activity import models


def _get_activity_choices():
    choices = []
    for item in ACTIVITY_CHOICES:
        for choice in item[1]:
            choices.append(choice)
    return choices

class ActivityStatSelectionForm(forms.Form):
    """ form to select activity statistic to view, and for which month to view it.
    """
    activity = forms.ChoiceField(
            label=_(u"Activity Statistic"), 
            help_text=_(u"Select the activity for which you need the statistics."),
            # widget=AdminRadioSelect,
            choices=_get_activity_choices())
    date_range = forms.DateField(
            label=_(u"Month"),
            help_text=_(u"Select any date in a month. You will get the totals for the month around the date."),
            required=True,
            widget=AdminDateWidget)


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created',)
    date_hierarchy = 'created'
    list_filter = ('activity',)
    ordering = ('-created', 'activity',)

    def get_urls(self):
        """ Extend the admin urls for the UserActivity admin model
            to be able to invoke a activity statistics view  on the admin model """
        urls = super(UserActivityAdmin, self).get_urls()
        stat_urls = patterns('',
                (r'^activity_stats/$', self.admin_site.admin_view(self.activity_stats)),
        )
        return stat_urls + urls

    def activity_stats(self, request):
        if request.method == 'POST':
            form = ActivityStatSelectionForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data

                # Get the date range
                the_date = cd['date_range']
                # the_date = the_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_month = calendar.monthrange(the_date.year, the_date.month)[1]
                range_month = [
                        the_date.replace(day=1), 
                        # the_date.replace(day=end_of_month, hour=23, minute=59, second=59)
                        the_date.replace(day=end_of_month)
                    ]

                # get the selected activity records in the month range
                qs = models.UserActivity.objects.filter(activity=int(cd['activity']),
                                                 created__range=range_month).values('pk')
                # Get the pk's of each record
                ual = [itm['pk'] for itm in qs]

                # Get the members who participated in the activity, and the occurrences 
                # of participation
                qs = Member.objects.filter(useractivity__id__in=ual).values('pk')
                qs = qs.annotate(cnt=Count('useractivity'))

                # Get the max occurrences
                max_participations = 0
                for itm in qs:
                    if itm['cnt'] > max_participations:
                        max_participations = itm['cnt']

                # get the members matching the max occurrence
                max_participations_list = []
                for itm in qs:
                    if itm['cnt'] == max_participations:
                        max_participations_list.append(itm)

                # output the results
                stats = []
                for itm in max_participations_list:
                    member = Member.objects.get(pk=itm['pk'])
                    stats.append({
                        'username': member.username, 
                        'fullname': member.get_full_name(), 
                        'mobile': member.mobile_number, 
                        'total': itm['cnt']
                    })

                return render_to_response('admin/activity/useractivity/activity_stats.html',
                                          {
                                              'form': form,
                                              'stats': stats,
                                              'month': "%04d-%02d" % (the_date.year, the_date.month)
                                          },
                                          context_instance=RequestContext(request))

        else:
            form = ActivityStatSelectionForm()

        return render_to_response('admin/activity/useractivity/activity_stats.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


admin.site.register(models.UserActivity, UserActivityAdmin)

admin.site.register(models.PointsActivity)
admin.site.register(models.BadgeGreyImage)
admin.site.register(models.Badge)
admin.site.register(models.MemberBadge)
