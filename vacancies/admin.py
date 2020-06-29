from django.contrib import admin

from .models import Company, Specialty, Vacancy, Application


class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'location', 'logo', 'description', 'employee_count', 'employer')
    readonly_fields = ('employer',)

    def employer(self, obj):
        return obj.owner.username


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Application, ApplicationAdmin)

