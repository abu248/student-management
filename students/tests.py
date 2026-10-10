from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase
from django.urls import reverse

from .models import Course, Student


class StudentPageTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        user_model.objects.create_user(username='testuser', password='test-password-123')
        self.client.login(username='testuser', password='test-password-123')
        self.course = Course.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(
            roll_number='S-001',
            first_name='Alex',
            last_name='Morgan',
            email='alex@example.com',
            gender='O',
            date_of_birth=date(2005, 6, 15),
            course=self.course,
        )

    def test_dashboard_displays_summary_and_recent_student(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'welcome-panel')
        self.assertContains(response, 'Alex Morgan')
        self.assertContains(response, 'Computer Science')

    def test_student_pages_render_their_expected_content(self):
        pages = (
            (reverse('student_list'), 'DIRECTORY'),
            (reverse('student_create'), 'Add Student'),
            (reverse('student_update', args=[self.student.pk]), 'Edit Student'),
            (reverse('student_detail', args=[self.student.pk]), 'STUDENT PROFILE'),
            (reverse('student_delete', args=[self.student.pk]), 'CONFIRM ACTION'),
        )

        for url, expected_content in pages:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_content)

    def test_login_page_renders_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')


class BootstrapAdminCommandTests(TestCase):
    def test_bootstrap_admin_creates_superuser_without_resetting_existing_password(self):
        credentials = {
            'DJANGO_SUPERUSER_USERNAME': 'siteadmin',
            'DJANGO_SUPERUSER_EMAIL': 'admin@example.com',
            'DJANGO_SUPERUSER_PASSWORD': 'initial-test-password-123',
        }
        user_model = get_user_model()
        with patch.dict('os.environ', credentials):
            call_command('bootstrap_admin')
            user = user_model.objects.get(username='siteadmin')
            user.set_password('changed-test-password-456')
            user.save()

            call_command('bootstrap_admin')

        user.refresh_from_db()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('changed-test-password-456'))

    def test_bootstrap_admin_rejects_partial_credentials(self):
        with patch.dict('os.environ', {'DJANGO_SUPERUSER_USERNAME': 'siteadmin'}):
            with self.assertRaises(CommandError):
                call_command('bootstrap_admin')
