from django.contrib import admin

# Register your models here.
from minder.models import Chore, ChoreOwner, ChoreCompleted 
from django import forms


class ChoreChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.chore_name


class ChoreOwnerForm(forms.ModelForm):
    chore = ChoreChoiceField(queryset=Chore.objects.all())
    class Meta:
        model = Chore


class ChoreAdmin(admin.ModelAdmin):
    list_display = ('chore_name', 'chore_value',) 
admin.site.register(Chore, ChoreAdmin)


class ChoreOwnerAdmin(admin.ModelAdmin):
    form = ChoreOwnerForm
    def chore_name(obj):
        return obj.chore.chore_name
    def owner_name(obj):
        return obj.owner.username
    list_display = (owner_name, chore_name, 'owner',)
admin.site.register(ChoreOwner, ChoreOwnerAdmin)


class ChoreCompletedAdmin(admin.ModelAdmin):
    list_display = ('chore', 'complete_date',)
admin.site.register(ChoreCompleted, ChoreCompletedAdmin)

