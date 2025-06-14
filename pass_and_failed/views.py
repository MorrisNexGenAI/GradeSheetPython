import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import PassFailedStatus
from .serializers import PassFailedStatusSerializer
from enrollment.models import Enrollment
from students.models import Student
from academic_years.models import AcademicYear
from grades.models import Grade
from levels.models import Level
from subjects.models import Subject

logger = logging.getLogger(__name__)

class PassFailedStatusViewSet(viewsets.ModelViewSet):
    queryset = PassFailedStatus.objects.all()
    serializer_class = PassFailedStatusSerializer

    def get_queryset(self):
        queryset = PassFailedStatus.objects.select_related('student', 'level', 'academic_year', 'enrollment')
        level_id = self.request.query_params.get('level_id')
        academic_year_name = self.request.query_params.get('academic_year')

        if level_id and academic_year_name:
            try:
                level = Level.objects.get(id=level_id)
                academic_year = AcademicYear.objects.get(name=academic_year_name)
                enrollments = Enrollment.objects.filter(
                    level=level,
                    academic_year=academic_year
                ).select_related('student')
                logger.info(f"Found {enrollments.count()} enrollments for level {level_id}, academic year {academic_year_name}")

                for enrollment in enrollments:
                    if not PassFailedStatus.objects.filter(
                        student=enrollment.student,
                        level=level,
                        academic_year=academic_year
                    ).exists():
                        grades = Grade.objects.filter(enrollment=enrollment)
                        subject_count = Subject.objects.filter(level=level).count()
                        logger.info(f"Subject count for level {level.id}: {subject_count}")
                        expected_grades = subject_count * 8 if subject_count else 1
                        grades_complete = grades.exists()
                        status = 'INCOMPLETE' if grades.count() < expected_grades else 'PENDING'
                        try:
                            PassFailedStatus.objects.create(
                                student=enrollment.student,
                                level=level,
                                academic_year=academic_year,
                                enrollment=enrollment,
                                grades_complete=grades_complete,
                                status=status,
                                template_name='pass_template.html'
                            )
                            logger.info(f"Created PassFailedStatus for student {enrollment.student.id}, level {level.id}, year {academic_year.name}")
                        except Exception as e:
                            logger.error(f"Failed to create PassFailedStatus for student {enrollment.student.id}: {str(e)}")
                queryset = queryset.filter(
                    student__in=[e.student_id for e in enrollments]
                )
            except (Level.DoesNotExist, AcademicYear.DoesNotExist) as e:
                logger.error(f"Error filtering statuses: {str(e)}")
                return PassFailedStatus.objects.none()
            except Exception as e:
                logger.error(f"Unexpected error in get_queryset: {str(e)}")
                return PassFailedStatus.objects.none()

        if level_id:
            queryset = queryset.filter(level_id=level_id)
        if academic_year_name:
            try:
                academic_year = AcademicYear.objects.get(name=academic_year_name)
                queryset = queryset.filter(academic_year=academic_year)
            except AcademicYear.DoesNotExist:
                logger.warning(f"Academic year {academic_year_name} not found")
                return PassFailedStatus.objects.none()

        return queryset

    @action(detail=True, methods=['post'], url_path='validate')
    def validate_status(self, request, pk=None):
        try:
            status_obj = self.get_object()
            status_value = request.data.get('status')
            validated_by = request.data.get('validated_by')
            if status_value not in ['PASS', 'FAIL', 'CONDITIONAL', 'PENDING', 'INCOMPLETE']:
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            if not status_obj.grades_complete and status_value in ['PASS', 'FAIL', 'CONDITIONAL']:
                return Response({"error": "Grades incomplete"}, status=status.HTTP_200_OK)
            status_obj.status = status_value
            status_obj.validated_by = validated_by
            status_obj.save()
            serializer = self.get_serializer(status_obj)
            logger.info(f"Status validated: {status_obj.id} as {status_value}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error validating status {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='promote')
    def promote_student(self, request, pk=None):
        try:
            with transaction.atomic():
                status_obj = self.get_object()
                level_id = request.data.get('level_id')
                role = request.data.get('role')
                
                if not role or role != 'admin':
                    return Response({"error": "Unauthorized role"}, status=status.HTTP_403_FORBIDDEN)
                
                if not level_id:
                    return Response({"error": "Level ID required"}, status=status.HTTP_400_BAD_REQUEST)
                
                if status_obj.status not in ['PASS', 'CONDITIONAL']:
                    return Response({"error": "Student must have PASS or CONDITIONAL status to promote"}, status=status.HTTP_400_BAD_REQUEST)
                
                current_level = Level.objects.get(id=level_id)
                next_level = Level.objects.filter(order__gt=current_level.order).order_by('order').first()
                if not next_level:
                    return Response({"error": "No higher level available"}, status=status.HTTP_400_BAD_REQUEST)

                current_enrollment = Enrollment.objects.filter(
                    student=status_obj.student,
                    level_id=level_id,
                    academic_year=status_obj.academic_year
                ).first()
                
                if not current_enrollment:
                    return Response({"error": "Current enrollment not found"}, status=status.HTTP_404_NOT_FOUND)

                Enrollment.objects.create(
                    student=status_obj.student,
                    level=next_level,
                    academic_year=status_obj.academic_year,
                    enrollment_date=status_obj.academic_year.start_date,
                    status='ENROLLED'
                )
                
                current_enrollment.status = 'PROMOTED'
                current_enrollment.save()
                
                logger.info(f"Student {status_obj.student.id} promoted from level {current_level.id} to {next_level.id}")
                return Response({
                    "message": f"Student promoted to {next_level.name}",
                    "new_level_id": next_level.id
                })
        except Level as eNotExist:
            logger.error(f"Level {level_id} not found")
            return Response({"error": "Level not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error promoting student {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)