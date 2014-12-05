from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.admin import CommentsAdmin

from .models import ThreadedComment

class ThreadedCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'title', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
    )

    list_display = ('comment', 'user', 'content_type', 'object_pk',
                    'ip_address', 'submit_date', 'is_public', 'is_removed')
    search_fields = ('comment', 'user__username', 'user_name',
                     'user_email', 'user_url', 'ip_address')
    # raw_id_fields = ("parent",)

admin.site.register(ThreadedComment, ThreadedCommentsAdmin)
