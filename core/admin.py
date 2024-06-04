from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullName')

admin.site.register(UserProfile, ProfileAdmin)


class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', )


class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', )


class FeesHeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'batch', 'department', 'session')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall')

class HallAdmin(admin.ModelAdmin):
    list_display = ('name', )

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'feeshead', 'amount')

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'student')

class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'session', 'batch','department', 'fullName',)


# Register your models here.
admin.site.register(FeesHead, FeesHeadAdmin)
admin.site.register(StudentFees, StudentFeeAdmin)
admin.site.register(DormitoryApplications, ApplicationFormAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Semester, SemesterAdmin)

'''
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullName', 'phone')
    
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')
       
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', )

class StockAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'tradePrice', 'mrp', 'entryDate', 'expirationDate')
   
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplier', 'entryDate' )
     
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'tradePrice')
     
class SaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'totalPrice', 'date', 'status')
       
class RefundAdmin(admin.ModelAdmin):
    list_display = ('sale', 'user', 'saleDetail', 'quantity', 'date',)
      
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity')

class DueAdmin(admin.ModelAdmin):
    list_display = ('sale', 'customer', 'dueAmount', 'date')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'streetAddress', 'city', )
    
class DueCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'due', 'amount',  'date')

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail, PurchaseDetailAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Refund, RefundAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)
admin.site.register(Due, DueAdmin)
admin.site.register(DueCollection, DueCollectionAdmin)
'''