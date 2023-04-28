from django.contrib import admin
from .models import Collection, CollectionItem, CollectionType, SiteUser, UserComment


admin.site.register(Collection)
admin.site.register(CollectionItem)
admin.site.register(CollectionType)
admin.site.register(SiteUser)
admin.site.register(UserComment)