from rest_framework import serializers
from .models import InfoPulse, TeacherInfo, TopStudent, SchoolService, CollaborationRequest, Student


class InfoPulseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoPulse
        fields = '__all__'


class TeacherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherInfo
        fields = '__all__'


class TopStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopStudent
        fields = '__all__'


class SchoolServiceSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=50)
    contactNumber = serializers.CharField(max_length=15)
    neighbourhood = serializers.CharField(max_length=50)
    alley = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=50)


class CollaborationRequestSerializer(serializers.Serializer):
    parentFullname = serializers.CharField(max_length=255)
    studentFullname = serializers.CharField(max_length=255)
    collaborationType = serializers.CharField(max_length=100)
    field = serializers.CharField(max_length=255)
    contactNumber = serializers.CharField(max_length=15)


class StudentSerializer(serializers.Serializer):
    studentFullname = serializers.CharField(max_length=255)
    familyOrder = serializers.CharField(max_length=50)
    grade = serializers.CharField(max_length=50)
    classNumber = serializers.CharField(max_length=50)
    healthStatus = serializers.CharField(max_length=None)
    fatherFullname = serializers.CharField(max_length=50)
    motherFullname = serializers.CharField(max_length=50)
    fatherJob = serializers.CharField(max_length=50)
    motherJob = serializers.CharField(max_length=50)
    fatherPhoneNumber = serializers.CharField(max_length=50)
    motherPhoneNumber = serializers.CharField(max_length=50)
    InsuranceType = serializers.CharField(max_length=50)


class GradeClassSerializer(serializers.Serializer):
    grade = serializers.DictField(
        child=serializers.CharField()
    )
    class_number = serializers.DictField(
        child=serializers.CharField()
    )


class ShowStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ShowServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolService
        fields = '__all__'


class ShowCollaborationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaborationRequest
        fields = '__all__'


class CreateInfoPulseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoPulse
        fields = '__all__'


class CreateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherInfo
        fields = '__all__'


class CreateTopStudentSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()

    def create(self, validated_data):
        student_id = validated_data.pop('id')
        student = Student.objects.get(pk=student_id)
        grade = student.grade
        classroom = student.class_number
        validated_data['grade'] = grade
        validated_data['classroom'] = classroom
        validated_data['fullname'] = student
        return TopStudent.objects.create(**validated_data)


class ShowStudentListForTupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_fullname', 'grade', 'class_number']


class ShowTopStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopStudent
        fields = '__all__'


class SendSMSToOneSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    text = serializers.CharField(max_length=160)


class SendSMSByGradeSerializer(serializers.Serializer):
    grade = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=160)


class SendSMSByClassSerializer(serializers.Serializer):
    grade = serializers.CharField(max_length=50)
    classNumber = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=160)


class SendSMSAllSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=160)


class ShowGradeClass(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('grade', 'class_number')

class SchoolServiceSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolService
        fields = ('fullname', 'contact_number', 'neighbourhood', 'alley', 'street')
