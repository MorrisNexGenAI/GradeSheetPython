# SchoolGradesSystem
**Student Grade Sheet System - Full Documentation**

---

## 📄 Overview

A web-based student grading and enrollment system designed for Bomi Junior High School. Built with Django REST Framework for the backend and React + TypeScript with TailwindCSS for the frontend.

---

## ⚖️ Backend (Django + DRF)

### Models:

1. **Student**

```python
first_name: CharField
last_name: CharField
gender: CharField (choices: M, F, O)
dob: DateField
created_at: DateTimeField (auto)
```

2. **Enrollment**

```python
student: ForeignKey(Student)
level: CharField
academic_year: CharField
term: CharField
```

> Additional models like `Subject`, `Grade`, and `Level` will be included as needed.

### API Endpoints (via DRF ViewSets + Routers):

* `GET /api/students/` - List students

* `POST /api/students/` - Add student

* `PUT /api/students/<id>/` - Update student

* `DELETE /api/students/<id>/` - Delete student

* `GET /api/enrollments/` - List enrollments

* `POST /api/enrollments/` - Add enrollment

* `PUT /api/enrollments/<id>/` - Update enrollment

* `DELETE /api/enrollments/<id>/` - Delete enrollment

### Setup:

```bash
pip install django djangorestframework
python manage.py makemigrations && migrate
python manage.py runserver
```

---

## 🔧 Frontend (React + TypeScript + TailwindCSS)

### Folder Structure:

```
src/
├── components/
│   └── StudentForm.tsx
│   └── EnrollmentForm.tsx
├── features/
│   └── students/
│       └── studentSlice.ts
│       └── useStudents.ts
│   └── enrollments/
│       └── enrollmentSlice.ts
│       └── useEnrollments.ts
├── pages/
│   └── StudentsPage.tsx
│   └── EnrollmentsPage.tsx
├── types/
│   └── student.ts
│   └── enrollment.ts
```

### State Management:

* **Redux Toolkit** manages `students` and `enrollments` slices.
* Async thunks (`createAsyncThunk`) used for CRUD operations.

### API Config:

```ts
const API_URL = import.meta.env.VITE_API_URL;
```

### Components:

* `StudentForm.tsx`: Form for adding/editing student data
* `EnrollmentForm.tsx`: Form for enrolling students in levels
* `StudentsPage.tsx`: Lists students, links to edit
* `EnrollmentsPage.tsx`: Lists enrollments, allows filtering/editing

---

## 🦾 Data Flow (Student Example)

1. User submits form in `StudentForm.tsx`
2. Triggers `addStudent(formData)` from `useStudents.ts`
3. Dispatches `addStudent` thunk in `studentSlice.ts`
4. POST to Django API at `/api/students/`
5. Response updates Redux state and re-renders UI

---

## 📌 Deployment (Local Dev)

### Backend:

* Run with `python manage.py runserver`
* Make sure CORS is enabled for frontend

### Frontend:

* Start dev server with `npm run dev`
* Connects to backend via `VITE_API_URL`

### Environment:

```
.env
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## ✅ Next Milestones

*

---

## 🚀 Vision

This system is meant to automate grading and enrollment workflows, reduce paper handling, and support school administrators with clean digital records. Easily extendable and maintained with professional practices.

---

*End of documentation (v1)*
# GradeSheetPython
# GradeSheetPython
# GradeSheetPython
