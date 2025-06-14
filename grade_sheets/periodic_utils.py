from django.conf import settings
import os
import time
import logging
import pythoncom
from docxtpl import DocxTemplate
from docx2pdf import convert
from PyPDF2 import PdfMerger
from grade_sheets.helpers import get_grade_sheet_data
from students.models import Student
from enrollment.models import Enrollment

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration
TEMPLATE_PATH = os.path.join(settings.MEDIA_ROOT, "templates", "periodic_card.docx")
OUTPUT_DIR = os.path.join(settings.MEDIA_ROOT, "output_gradesheets")

def generate_periodic_gradesheet_pdf(level_id, student_id=None):
    """
    Generate Periodic_card PDFs for students in the given level_id or a single student_id.
    Each card is on a single sheet. Returns a list of PDF paths or a merged PDF for by-level printing.
    """
    try:
        logger.debug(f"Starting Periodic_card PDF generation for level_id={level_id}, student_id={student_id}")
        # Create output directory
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            logger.info(f"Created output directory: {OUTPUT_DIR}")

        # Verify permissions
        if not os.access(OUTPUT_DIR, os.W_OK):
            raise PermissionError(f"No write permission for {OUTPUT_DIR}")

        # Verify template
        if not os.path.exists(TEMPLATE_PATH):
            raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}")
        logger.info(f"Using template: {TEMPLATE_PATH}")

        # Query students
        pdf_paths = []
        if student_id:
            logger.debug(f"Querying single student: {student_id}")
            student = Student.objects.get(id=student_id)
            enrollments = Enrollment.objects.filter(student_id=student_id, level_id=level_id)
            students = [student] if enrollments.exists() else []
        else:
            logger.debug(f"Querying all students for level: {level_id}")
            enrollments = Enrollment.objects.filter(level_id=level_id).select_related("student")
            students = [enrollment.student for enrollment in enrollments]

        if not students:
            logger.warning(f"No students found for level_id: {level_id}, student_id: {student_id}")
            return pdf_paths

        # Generate PDF for each student
        for student in students:
            logger.debug(f"Processing student: {student.id}")
            student_data = get_grade_sheet_data(student.id, level_id)
            logger.info(f"Prepared data for student: {student_data['name']}")

            # Generate .docx and PDF
            student_name = student_data["name"].replace(" ", "_")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            docx_path = os.path.join(OUTPUT_DIR, f"periodic_card_{student_name}_{timestamp}.docx")
            pdf_path = os.path.join(OUTPUT_DIR, f"periodic_card_{student_name}_{timestamp}.pdf")
            logger.debug(f"Output paths: docx={docx_path}, pdf={pdf_path}")

            # Verify write permission
            if os.path.exists(docx_path) and not os.access(docx_path, os.W_OK):
                raise PermissionError(f"No write permission for {docx_path}")

            # Render template
            logger.debug("Rendering template")
            template = DocxTemplate(TEMPLATE_PATH)
            template.render(student_data)
            template.save(docx_path)
            logger.info(f"Saved .docx: {docx_path}")

            # Verify .docx
            if not os.path.exists(docx_path):
                raise FileNotFoundError(f"Failed to create .docx at {docx_path}")
            if os.path.getsize(docx_path) == 0:
                raise ValueError(f"Generated .docx is empty: {docx_path}")

            # Convert to PDF
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    pythoncom.CoInitialize()
                    logger.debug(f"Attempt {attempt + 1}: Converting {docx_path} to {pdf_path}")
                    convert(docx_path, pdf_path)
                    logger.info(f"Converted to PDF: {pdf_path}")
                    break
                except Exception as e:
                    logger.error(f"PDF conversion attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        raise Exception(f"PDF conversion failed after {max_retries} attempts: {str(e)}")
                    time.sleep(2)
                finally:
                    pythoncom.CoUninitialize()

            # Verify PDF
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF generation failed for {pdf_path}")
            if os.path.getsize(pdf_path) == 0:
                raise ValueError(f"Generated PDF is empty: {pdf_path}")

            # Clean up .docx
            try:
                os.remove(docx_path)
                logger.info(f"Cleaned up .docx: {docx_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up .docx: {str(e)}")

            pdf_paths.append(pdf_path)

        # Merge PDFs for by-level printing
        if not student_id and pdf_paths:
            merged_pdf_path = os.path.join(OUTPUT_DIR, f"periodic_cards_level_{level_id}_{timestamp}.pdf")
            merger = PdfMerger()
            for pdf_path in pdf_paths:
                merger.append(pdf_path)
            merger.write(merged_pdf_path)
            merger.close()
            logger.info(f"Merged PDFs into: {merged_pdf_path}")

            # Verify merged PDF
            if not os.path.exists(merged_pdf_path):
                raise FileNotFoundError(f"Merged PDF not created: {merged_pdf_path}")
            if os.path.getsize(merged_pdf_path) == 0:
                raise ValueError(f"Merged PDF is empty: {merged_pdf_path}")

            # Clean up individual PDFs
            for pdf_path in pdf_paths:
                try:
                    os.remove(pdf_path)
                    logger.info(f"Cleaned up individual PDF: {pdf_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up PDF: {str(e)}")

            return [merged_pdf_path]

        return pdf_paths

    except Exception as e:
        logger.error(f"Error generating Periodic_card PDF: {str(e)}")
        raise Exception(f"Error generating Periodic_card PDF: {str(e)}")