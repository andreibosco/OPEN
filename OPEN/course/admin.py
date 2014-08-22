from django.contrib import admin

from OPEN.course.models import Course, Forum, Grade, UploadedFile


class CourseAdmin(admin.ModelAdmin):
    pass


class ForumAdmin(admin.ModelAdmin):
    pass


class GradeAdmin(admin.ModelAdmin):
    pass


class UploadedFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(UploadedFile, UploadedFileAdmin)
