from django.contrib import admin
from councilmatic.subscriptions import models

#class KeywordInline(admin.StackedInline):
#    model = KeywordSubscription
#    extra = 3

#class CouncilmemberInline(admin.StackedInline):
#    model = CouncilMemberSubscription
#    extra = 3

#class SubscriptionAdmin(admin.ModelAdmin):
#    inlines = [KeywordInline, CouncilmemberInline]

#class LegActionInline(admin.StackedInline):
#    model = LegAction
#    extra = 1

class ContentFeedParameterInline(admin.StackedInline):
    model = models.ContentFeedParameter
    extra = 0

class ContentFeedRecordAdmin(admin.ModelAdmin):
    inlines = [ContentFeedParameterInline]
    
    def queryset(self, request):
        return models.ContentFeedRecord.objects.prefetch_related('feed_params')

class SubscriptionDispatchRecordInline(admin.TabularInline):
    model = models.SubscriptionDispatchRecord
    extra = 0

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'last_sent']
    inlines = [SubscriptionDispatchRecordInline]
    
    def queryset(self, request):
        return models.Subscription.objects.select_related('feed_record').prefetch_related('feed_record__feed_params')

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'last_login']


admin.site.register(models.Subscription, SubscriptionAdmin)
admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.ContentFeedRecord, ContentFeedRecordAdmin)

#admin.site.register(models.SearchSubscription)
#admin.site.register(models.EmailChannel)
#admin.site.register(models.RssChannel)
#admin.site.register(models.SmsChannel)
