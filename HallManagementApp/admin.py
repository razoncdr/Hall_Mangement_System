from django.contrib import admin
from HallManagementApp.models import Hall, Payment, ApplicationForm, Room, Student, Session, Department, Batch


class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', )


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'batch', 'department', 'session')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall')

class HallAdmin(admin.ModelAdmin):
    list_display = ('name', )


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'student')


class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ('student', )


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount')

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ApplicationForm, ApplicationFormAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hall, HallAdmin)