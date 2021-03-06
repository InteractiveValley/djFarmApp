# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Direction, CustomUser, ScheduledOrder, Question, ConektaUser, Rating, Inapam, TokenPhone, Reminder
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from usuarios.forms import CustomUserChangeForm, CustomUserCreationForm
from django_summernote.admin import SummernoteModelAdmin


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'cell', 'inapam',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'cell', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


class DirectionAdmin(admin.ModelAdmin):
    list_display = ('location', 'direction', 'user', 'active',)
    search_fields = ('location', 'street', 'colony', 'postal_code', 'delegation_municipaly',
                     'user__email', 'user__first_name', 'user__last_name')
    ordering = ('created',)


admin.site.register(Direction, DirectionAdmin)


class ScheduledOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'period', 'days', 'times', 'date_next', 'date_ends',
                    'canceled_for_user', 'canceled_for_system',)
    search_fields = ('product__name', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('date_next', 'date_ends', 'canceled_for_user', 'canceled_for_system',)


admin.site.register(ScheduledOrder, ScheduledOrderAdmin)


class QuestionAdmin(SummernoteModelAdmin):
    list_display = ('order', 'question', 'ask',)


admin.site.register(Question, QuestionAdmin)


class ConektaUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'conekta_user',)


admin.site.register(ConektaUser, ConektaUserAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'created',)


admin.site.register(Rating, RatingAdmin)


class InapamAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'active')


admin.site.register(Inapam, InapamAdmin)


class TokenPhoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created')


admin.site.register(TokenPhone, TokenPhoneAdmin)


class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        'user','title', 'message', 'time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','active')

admin.site.register(Reminder, ReminderAdmin)
