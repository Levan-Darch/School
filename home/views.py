from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import InfoPulse, TeacherInfo, TopStudent, SchoolService, CollaborationRequest, \
    Student
from .serializers import InfoPulseSerializer, TeacherInfoSerializer, TopStudentSerializer, SchoolServiceSerializer, \
    CollaborationRequestSerializer, StudentSerializer, GradeClassSerializer, ShowStudentsSerializer, \
    ShowServiceSerializer, ShowCollaborationRequestSerializer, CreateInfoPulseSerializer, CreateTeacherSerializer, \
    CreateTopStudentSerializers, ShowStudentListForTupStudentSerializer, ShowTopStudentsSerializer, \
    SendSMSToOneSerializer, SendSMSByGradeSerializer, SendSMSByClassSerializer, SendSMSAllSerializer, ShowGradeClass, \
    SchoolServiceSearchSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .utils import send_sms
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, login
import logging
from django.contrib.auth import logout
from itsdangerous import URLSafeSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.

class HomeView(View):
    def get(self, request):
        return HttpResponse("this is home page")


def encode_credentials(username, password):
    s = URLSafeSerializer('your-secret-key')
    token = s.dumps({'username': username, 'password': password})
    return token


logger = logging.getLogger(__name__)


class LoginView(APIView):
    def __init__(self):
        self.logger = logger

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            self.logger.info(f'enter username {username}.')
            request.session['logged_in'] = True
            request.session['username'] = username

            token = encode_credentials(username, password)

            return Response({'message': 'logged in successfully', 'status': request.user.is_authenticated,
                             'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Username or password is invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'you have successfully logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'you haven't logged in'}, status=status.HTTP_401_UNAUTHORIZED)


class InfoPulsePagination(PageNumberPagination):
    page_size = 100000


class InfoPulseListView(ListAPIView):
    queryset = InfoPulse.objects.all()
    serializer_class = InfoPulseSerializer
    pagination_class = InfoPulsePagination


class TeacherInfoDetailView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = TeacherInfo.objects.all()
        serializer = TeacherInfoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopStudentsDetailView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = TopStudent.objects.all()
        serializer = TopStudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SchoolServiceView(APIView):
    def post(self, request, my_format=None):
        serializer = SchoolServiceSerializer(data=request.data)

        if serializer.is_valid():
            school_service = SchoolService(
                fullname=serializer.validated_data['fullname'],
                contact_number=serializer.validated_data['contactNumber'],
                neighbourhood=serializer.validated_data['neighbourhood'],
                alley=serializer.validated_data['alley'],
                street=serializer.validated_data['street']
            )
            school_service.save()

            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
class CollaborationRequestView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = CollaborationRequest.objects.all()
        serializer = CollaborationRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CollaborationRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class CollaborationRequestView(APIView):

    def post(self, request, my_format=None):
        serializer = CollaborationRequestSerializer(data=request.data)

        if serializer.is_valid():
            collaboration_request = CollaborationRequest(
                parent_fullname=serializer.validated_data['parentFullname'],
                student_fullname=serializer.validated_data['studentFullname'],
                collaboration_type=serializer.validated_data['collaborationType'],
                field=serializer.validated_data['field'],
                contact_number=serializer.validated_data['contactNumber']
            )
            collaboration_request.save()

            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = Student(
                student_fullname=serializer.validated_data['studentFullname'],
                family_order=serializer.validated_data['familyOrder'],
                grade=serializer.validated_data['grade'],
                class_number=serializer.validated_data['classNumber'],
                health_status=serializer.validated_data['healthStatus'],
                father_fullname=serializer.validated_data['fatherFullname'],
                mother_fullname=serializer.validated_data['motherFullname'],
                father_job=serializer.validated_data['fatherJob'],
                mother_job=serializer.validated_data['motherJob'],
                father_phone_number=serializer.validated_data['fatherPhoneNumber'],
                mother_phone_number=serializer.validated_data['motherPhoneNumber'],
                Insurance_type=serializer.validated_data['InsuranceType']
            )
            student.save()

            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
class SendSMSView(APIView):

    def get(self, request):
        unique_grades = Student.objects.values('grade').distinct()
        unique_class_numbers = Student.objects.values('class_number').distinct()

        grade_class_data = []

        for grade in unique_grades:
            for class_number in unique_class_numbers:
                grade_class_data.append({
                    'grade': grade['grade'],
                    'class_number': class_number['class_number']
                })

        # ارسال اطلاعات به عنوان پاسخ API
        serializer = ShowGradeClass(grade_class_data, many=True)
        return Response(serializer.data)

    def post(self, request, my_format=None):
        serializer = SendSMSToOneSerializer(data=request.data)
        if serializer.is_valid():
            student_fullname = serializer.validated_data['studentFullname']
            text = serializer.validated_data['text']

            student = Student.objects.get(student_fullname=student_fullname)
            father_phone_number = student.father_phone_number
            mother_phone_number = student.mother_phone_number

            send_sms(father_phone_number, text)

            send_sms(mother_phone_number, text)

            return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)
        print(222222)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class SendSMSView(APIView):
    def get(self, request):
        student_ids = Student.objects.values_list('id', flat=True)
        return Response({'student_ids': list(student_ids)})

    def post(self, request, my_format=None):
        serializer = SendSMSToOneSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data['id']
            text = serializer.validated_data['text']

            # تبدیل student_id به Integer
            try:
                student_id = int(student_id)
            except ValueError:
                return Response({'message': 'Student ID must be a number'}, status=status.HTTP_400_BAD_REQUEST)

            student = get_object_or_404(Student, pk=student_id)

            father_phone_number = student.father_phone_number
            mother_phone_number = student.mother_phone_number

            send_sms(father_phone_number, text)

            send_sms(mother_phone_number, text)

            return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendSMSByGradeView(APIView):
    serializer_class = SendSMSByGradeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            grade_name = serializer.validated_data['grade']
            sms_text = serializer.validated_data['text']

            students = Student.objects.filter(grade=grade_name)

            if students.exists():
                for student in students:
                    send_sms(student.father_phone_number, sms_text)
                    send_sms(student.mother_phone_number, sms_text)
                return Response({'message': 'Successfull'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToAllView(APIView):
    serializer_class = SendSMSAllSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sms_text = serializer.validated_data['text']

            students = Student.objects.all()

            for student in students:
                send_sms(student.father_phone_number, sms_text)
                send_sms(student.mother_phone_number, sms_text)

            return Response({'message': 'successful'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendToClassView(APIView):
    serializer_class = SendSMSByClassSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            grade = serializer.validated_data['grade']
            class_number = serializer.validated_data['classNumber']
            sms_text = serializer.validated_data['text']

            students = Student.objects.filter(grade=grade, class_number=class_number)

            if students.exists():
                for student in students:
                    send_sms(student.father_phone_number, sms_text)
                    send_sms(student.mother_phone_number, sms_text)
                return Response({'message': 'successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentInfoView(View):

    def get(self, request):
        students = Student.objects.all()
        return render(request, 'home/student_info.html', {'students': students})


class GradeClassAPIView(APIView):

    def get(self, request, my_format=None):
        data = {
            "grade": dict(Student.GRADE_CHOICES),
            "class_number": dict(Student.CLASS_NUMBER_CHOICES)
        }
        serializer = GradeClassSerializer(data)
        return Response(serializer.data)


class ShowStudentsInfo(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = ShowStudentsSerializer(students, many=True)
        return Response(serializer.data)


class ShowServiceInfo(APIView):

    def get(self, request):
        service = SchoolService.objects.all()
        serializer = ShowServiceSerializer(service, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class ShowCollaborationRequest(APIView):

    def get(self, request):
        collaboration_request = CollaborationRequest.objects.all()
        serializer = ShowCollaborationRequestSerializer(collaboration_request, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class CreateInfoPulse(APIView):

    def post(self, request):
        serializer = CreateInfoPulseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        print(1)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTeachers(APIView):

    def post(self, request):
        serializer = CreateTeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        print(1)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTopStudent(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = ShowStudentListForTupStudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateTopStudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Informations saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowTopStudents(APIView):

    def get(self, request):
        students = TopStudent.objects.all()
        serializer = ShowTopStudentsSerializer(students, many=True)
        return Response(serializer.data)


class StatusView(APIView):
    def get(self, request, my_format=None):
        if request.user.is_authenticated:
            logged_in_status = True
        else:
            logged_in_status = False

        return Response({'logged_in': logged_in_status})


class Test(APIView):
    def get(self, request):
        print(request.session.get('logged_in'))
        logged_in = request.session.get('logged_in')
        if logged_in:
            username = request.session.get('username')
            print(username)
            return Response({'message': f'User {username} has logged in', 'status': request.user.is_authenticated},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'The user is not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)


class InfoPulseDetail(APIView):
    def get(self, request, post_id):
        news_post = InfoPulse.objects.get(pk=post_id)
        serializer = InfoPulseSerializer(news_post)
        return Response(serializer.data)


class NeighbourhoodSearch(APIView):
    def post(self, request, *args, **kwargs):
        neighbourhood = request.data.get('neighbourhood')

        if not neighbourhood:
            return Response({'message': 'Please enter the neighborhood.'}, status=status.HTTP_400_BAD_REQUEST)

        schools = SchoolService.objects.filter(neighbourhood=neighbourhood)
        serializer = SchoolServiceSearchSerializer(schools, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowClassNumbers(APIView):
    def get(self, request):
        class_number_choices = [
            {choice[0]: choice[0]}
            for choice in Student.CLASS_NUMBER_CHOICES
        ]
        return Response(class_number_choices)

