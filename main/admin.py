from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author

# Define a classe de administração para o modelo CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff',  'created_at', 'updated_at')
    list_filter = ('is_staff',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',
         'birth_date', 'profile_picture', 'bio', 'sex', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )


# Registrar o modelo CustomUser e a classe de administração CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Defina a classe de administração para o modelo Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('pseudo_name', 'death_day',
                    'home_country', 'home_state', 'home_town')


# Registrar o modelo Author e a classe de administração AuthorAdmin
admin.site.register(Author, AuthorAdmin)
