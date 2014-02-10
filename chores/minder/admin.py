from django.contrib import admin

# Register your models here.
from chores.minder.models import Chore, ChoreOwner, ChoreCompleted 


class ChoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Chore, ChoreAdmin)


class ChoreOwnerAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChoreOwner, ChoreOwnerAdmin)


class ChoreCompletedAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChoreCompleted, ChoreCompletedAdmin)

