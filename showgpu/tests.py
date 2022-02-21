from django.test import Client,TestCase
from django.urls import reverse
from .models import GPU_Type,GPU

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


    def test_code_generation(self):
        self.assertEqual(f'{self.gpu_type.code}', 'rtx3060ti')
    
    def test_profit(self):
        self.assertEqual(f'{self.gpu_type.day_profit}', '0')
        self.assertEqual(f'{self.gpu_type.month_profit}', '0')

    def test_primary_token(self):
        self.assertEqual(f'{self.gpu_type.primary_token}', 'eth')

class GPU_Test(TestCase):
    def setUp(self):
        self.gpu = GPU.objects.create(
            title='RTX 3060 Ti lalala',
            price=45000,
            payback=400,
        )
    def test_gpu_listing(self):
        self.assertEqual(f'{self.gpu.title}', 'RTX 3060 Ti lalala')
        self.assertEqual(f'{self.gpu.price}', '45000')
        self.assertEqual(f'{self.gpu.payback}', '400')

    