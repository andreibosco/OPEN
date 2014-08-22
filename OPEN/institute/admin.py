from django.contrib import admin

from OPEN.institute.models import Institute, Discipline, SubDiscipline


class InstituteAdmin(admin.ModelAdmin):
    pass


class DisciplineAdmin(admin.ModelAdmin):
    pass


class SubDisciplineAdmin(admin.ModelAdmin):
    pass

admin.site.register(Institute, InstituteAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(SubDiscipline, SubDisciplineAdmin)


