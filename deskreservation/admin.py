from django.contrib import admin
from django.core.management import call_command

from .models import Desk, DeskReservation


@admin.action(description='Generate desk usage report')
def generate_desk_usage_report(modeladmin, request, queryset):
    call_command('generate_desk_usage_report')
generate_desk_usage_report.acts_on_all = True


class AllowActsOnAllActionsModelAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            action_acts_on_all = action.acts_on_all
        except (KeyError, AttributeError):
            action_acts_on_all = False

        if action_acts_on_all:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME,
                        self.model.objects.values_list('id', flat=True))
            request.POST = post

        return admin.ModelAdmin.changelist_view(self, request, extra_context)
    
    # def changelist_view(self, request, extra_context=None):
    #     if 'action' in request.POST and request.POST['action'] == 'generate_desk_usage_report':
    #         if not request.POST.getlist(ACTION_CHECKBOX_NAME):
    #             post = request.POST.copy()
    #             for u in MyModel.objects.all():
    #                 post.update({ACTION_CHECKBOX_NAME: str(u.id)})
    #             request._set_post(post)
    #     return super(MyModelAdmin, self).changelist_view(request, extra_context)


@admin.register(Desk)
class DeskAdmin(AllowActsOnAllActionsModelAdmin):
    list_display = ("pk", "building", "floor", "number", "lead", "ergonomic")
    list_filter = ("building", "floor", "lead", "ergonomic")
    actions = [generate_desk_usage_report]


@admin.register(DeskReservation)
class DeskReservationAdmin(AllowActsOnAllActionsModelAdmin):
    list_display = ("pk", "employee", "desk", "check_in", "check_out")
    search_fields = ("employee__user__username", )
    list_filter = ("desk__building", "desk__floor", "desk__number")
    fields = ("employee", "desk", "check_in", "check_out")
    readonly_fields = ("check_in",)
    actions = [generate_desk_usage_report]