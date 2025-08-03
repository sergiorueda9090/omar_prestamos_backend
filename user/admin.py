from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from user.models                import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields':('username','password')}),
        ('Informacion Personal',{'fields':('first_name','last_name','email')})
    )
