from django.contrib import admin
from adminpanel.models import LogEntry, LogAction, LogCategory, ReportCategory, Report, Suggestions, Votes

class ReportAdmin(admin.ModelAdmin):
    list_display = ('category', 'relate', 'relate_comment', 'user', 'date', 'verified')
    list_filter = ('category', 'relate', 'relate_comment', 'user', 'date', 'verified')
    fieldsets = (
    (None, {'fields': ('user', 'category')}),
    ('Contents', {'fields': ('contents',)}),
    ('Related to', {'fields': ('relate', 'relate_comment')}),
    ('Was verified by helper?', {'fields': ('verified',)})
    )
    # readonly_fields = ('user', 'category', 'contents', 'relate', 'relate_comment')
    ordering = ('date', 'verified')

admin.site.register(LogEntry)

admin.site.register(LogAction)

admin.site.register(LogCategory)

admin.site.register(ReportCategory)

admin.site.register(Report, ReportAdmin)

admin.site.register(Suggestions)

admin.site.register(Votes)
