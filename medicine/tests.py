from django.test import TestCase
from medicine.models import Medicine
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import timedelta

class MedicineTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')

        self.active_medicine = Medicine.objects.create(
            patient=self.user,
            title="Аспирин",
            end_date=timezone.now().date() + timedelta(days=1), 
            today=1,
            amount_per_day=2,
            dosage="1 таблетка",
            comments="Принимать после еды"
        )

        self.ended_medicine = Medicine.objects.create(
            patient=self.user,
            title="Антибиотик",
            end_date=timezone.now().date() - timedelta(days=1),
            today=2,
            amount_per_day=2,
            dosage="2 капсулы",
            comments="Принимать с едой"
        )

    def test_medicine_over(self):
        """Тестирование метода is_medicine_over == True"""
        self.assertTrue(self.ended_medicine.is_medicine_over)

    def test_medicine_not_over(self):
        """Тестирование метода is_medicine_over == False"""
        self.assertFalse(self.active_medicine.is_medicine_over)

    def test_clean_raises_validation_error(self):
        """Тестирование метода clean на валидацию поля today."""
        medicine = Medicine(
            title="Парацетамол",
            end_date=timezone.now().date(),
            today=3,  # Невалидно
            amount_per_day=2,
            dosage="1 таблетка",
            comments="Пить перед сном"
        )

        with self.assertRaises(ValidationError) as context:
            medicine.full_clean()
        
        self.assertIn('today', context.exception.message_dict)
        self.assertEqual(context.exception.message_dict['today'][0], 'Значение должно быть не больше 2')
