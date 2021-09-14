from django.contrib import admin

# http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/
from django.core.paginator import Paginator
from django.core.cache import cache

from private_chat.models import PrivateChat, PrivateMessage


class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'first', 'second']
    search_fields = ['id', 'first', 'second']

    class Meta:
        model = PrivateChat


admin.site.register(PrivateChat, PrivateChatAdmin)


class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'chat', 'timestamp']
    list_filter = ['user', 'chat', 'timestamp']
    search_fields = ['user__username', 'content']
    readonly_fields = ['id', 'user', 'chat', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = PrivateMessage

admin.site.register(PrivateMessage, PrivateMessageAdmin)