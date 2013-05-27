from django.contrib import admin

from activity import models

admin.site.register(models.PointsActivity)
admin.site.register(models.UserActivity)
admin.site.register(models.BadgeGreyImage)
admin.site.register(models.Badge)



class MemberBadgeAdmin(admin.ModelAdmin):
    raw_id_fields = ('member',)

admin.site.register(models.MemberBadge, MemberBadgeAdmin)
