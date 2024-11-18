from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from medicine.models import Medicine
from django.utils import timezone
from datetime import timedelta

class MedicineScenarioTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_registers_creates_updates_and_deletes_medicine(self):
        """Тестирование полного сценария: регистрация, создание лекарства, изменение и удаление."""
        # Логинимся
        self.client.login(username='testuser', password='testpass')

        # 1. Создание лекарства
        create_medicine_data = {
            'title': 'Аспирин',
            'end_date': (timezone.now() + timedelta(days=5)).date(),
            'today': 0,
            'amount_per_day': 2,
            'dosage': '1 таблетка',
            'comments': 'Принимать после  еды'
        }
        response = self.client.post(reverse('medicine:add_medicine'), create_medicine_data)
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после создания
        self.assertTrue(Medicine.objects.filter(title='Аспирин', patient=self.user).exists())  # Проверяем, что лекарство создано

        # Получаем созданное лекрство для дальнейших тестов.
        medicine = Medicine.objects.get(title='Аспирин', patient=self.user)

        # 2. Обновление количества принятого сегодня (increment)
        response = self.client.post(reverse('medicine:update_medicine', args=[medicine.id, 'increment']))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'new_today': 1, 'amount_per_day': 2})

        # Проверяем, что коичество принято сегодня обновилось
        medicine.refresh_from_db()
        self.assertEqual(medicine.today, 1)

        # 3. Уменьшение количества принятого сегодня (decrement)
        response = self.client.post(reverse('medicine:update_medicine', args=[medicine.id, 'decrement']))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'new_today': 0, 'amount_per_day': 2})

        # Проверяем, что количество принято сегодня уменьшилось
        medicine.refresh_from_db()
        self.assertEqual(medicine.today, 0)
        