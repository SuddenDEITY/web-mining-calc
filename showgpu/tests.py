from django.test import Client,TestCase
from django.urls import reverse
from .models import GPU_Type

class GPU_Type_Test(TestCase):
    def setUp(self):
        self.gpu_type = GPU_Type.objects.create(
            name='RTX 3060 Ti',
            eth=44.00,
            ton=2200.00,
        )

    def test_gpu_type_listing(self):
        self.assertEqual(f'{self.gpu_type.name}', 'RTX 3060 Ti')
        self.assertEqual(f'{self.gpu_type.eth}', '44.0')
        self.assertEqual(f'{self.gpu_type.ton}', '2200.0')

    def test_gpu_type_list_view(self): 
        response = self.client.get(reverse('gpu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RTX 3060 Ti')
        self.assertTemplateUsed(response, 'showgpu/gpu_type_list.html')

    def test_code_generation(self):
        self.assertEqual(f'{self.gpu_type.code}', 'rtx3060ti')
    
    def test_profit(self):
        self.assertEqual(f'{self.gpu_type.day_profit}', '0')
        self.assertEqual(f'{self.gpu_type.month_profit}', '0')

    def test_primary_token(self):
        self.assertEqual(f'{self.gpu_type.primary_token}', 'eth')
