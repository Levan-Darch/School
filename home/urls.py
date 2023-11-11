from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/infopulse/', InfoPulseListView.as_view(), name='news_api'),
    path('api/infopulse/<int:post_id>/', InfoPulseDetail.as_view(), name='news_post'),
    path('api/v1/teachers/', TeacherInfoDetailView.as_view(), name='teachers_api'),
    path('api/v1/top_students/', TopStudentsDetailView.as_view(), name='top_students_api'),
    path('api/v1/school_service/', SchoolServiceView.as_view(), name='school_service_api'),
    path('api/v1/collaboration_request/', CollaborationRequestView.as_view(), name='collaboration_request_api'),
    path('api/v1/student/', StudentView.as_view(), name='student_api'),
    path('api/v1/grades_and_classes/', GradeClassAPIView.as_view(), name='grades_and_classes_api'),
    path('api/v1/student_info/', StudentInfoView.as_view(), name='student_info'),
    path('api/v1/send_sms/', SendSMSView.as_view(), name='send_sms'),
    path('api/v1/send_sms_to_grade/', SendSMSByGradeView.as_view(), name='send_sms_by_grade'),
    path('api/v1/send_to_all/', SendToAllView.as_view(), name='send_to_all'),
    path('api/v1/send_to_class/', SendToClassView.as_view(), name='send_to_class'),
    path('api/v1/show_students/', ShowStudentsInfo.as_view(), name='show_students'),
    path('api/v1/show_service/', ShowServiceInfo.as_view(), name='show_service'),
    path('api/v1/show_collaboration_request/', ShowCollaborationRequest.as_view(), name='show_collaboration_request'),
    path('api/v1/show_top_students/', ShowTopStudents.as_view(), name='show_top_students'),
    path('api/v1/show_class_numbers/', ShowClassNumbers.as_view(), name='show_class_numbers'),
    path('api/v1/create_infopulse/', CreateInfoPulse.as_view(), name='create_info_pulse'),
    path('api/v1/create_teachers/', CreateTeachers.as_view(), name='create_teachers'),
    path('api/v1/create_topstudent/', CreateTopStudent.as_view(), name='create_top_student'),
    path('api/v1/neighbourhood_search/', NeighbourhoodSearch.as_view(), name='neighbourhood_search'),
    path('api/v1/n2571', LoginView.as_view(), name='login'),
    path('api/v1/n2571_logout', LogoutView.as_view(), name='logout'),
    path('api/v1/status/', StatusView.as_view(), name="status"),
    path('test/', Test.as_view(), name="test"),
]
