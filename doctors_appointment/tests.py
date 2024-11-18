from django.test import TestCase
from doctors_appointment.models import Appointment
import datetime

from django.utils import timezone

# convert_date, convert_time

class AppointmentTests(TestCase):
    """ Tests for Appointment model. """ 

    def setUp(self):
        """ Секция Arrange. """
        self.past_appointment = Appointment.objects.create(
            doctor="Dr. House",
            date=timezone.now().date() - datetime.timedelta(days=1),
            time=(timezone.now() - datetime.timedelta(hours=1)).time(),
            address="Test Address",
            office_number="101",
            health_troubles="Cough",
            report="Past appointment report",
        )

        self.future_appointment = Appointment.objects.create(
            doctor="Dr. Strange",
            date=timezone.now().date() + datetime.timedelta(days=1),
            time=(timezone.now() + datetime.timedelta(hours=2)).time(),
            address="Test Address",
            office_number="102",
            health_troubles="Headache",
            report="..., ..., ..., ..., ...",
        )
    
    def test_appointment_over(self):
        """Тестирование метода is_appointment_over == True"""
        self.assertTrue(self.past_appointment.is_appointment_over) # Совмещенная секция Act и Assert
        
    
    def test_appointment_not_over(self):
        """Тестирование метода is_appointment_over == False"""
        self.assertFalse(self.future_appointment.is_appointment_over)

    def test_report_was_added(self):
        """ Тестирование метода is_report_was_added == True """
        self.assertTrue(self.past_appointment.is_report_was_added)
    
    def test_report_was_not_added(self):
        """ Тестирование метода is_report_was_added == False """
        self.assertTrue(self.future_appointment.is_report_was_added)
