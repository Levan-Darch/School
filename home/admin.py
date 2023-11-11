from django.contrib import admin
from .models import InfoPulse, TeacherInfo, TopStudent, SchoolService, CollaborationRequest, Student

# Register your models here.

admin.site.register(InfoPulse)
admin.site.register(TeacherInfo)
admin.site.register(SchoolService)
admin.site.register(CollaborationRequest)
admin.site.register(Student)


class TopStudentAdmin(admin.ModelAdmin):
    search_fields = ['fullname']


admin.site.register(TopStudent, TopStudentAdmin)
