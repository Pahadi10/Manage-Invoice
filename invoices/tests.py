from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):

    def setUp(self):
        self.invoice = Invoice.objects.create(date='2024-09-01', customer_name='John Doe')
        self.invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Item 1', quantity=2, unit_price=10.00, price=20.00)

    def test_create_invoice(self):
        data = {
            'date': '2024-09-01',
            'customer_name': 'Nitesh Sir',
            'invoice_details': [
                {'description': 'Item 2', 'quantity': 3, 'unit_price': 15.00, 'price': 45.00},
            ]
        }
        response = self.client.post(reverse('invoice-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invoices(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice(self):
        data = {
            'date': '2024-09-01',
            'customer_name': 'Sharma Rohit',
            'invoice_details': [
                {'id': self.invoice_detail.id, 'description': 'Updated Item', 'quantity': 2, 'unit_price': 10.00, 'price': 20.00},
            ]
        }
        response = self.client.put(reverse('invoice-detail', kwargs={'pk': self.invoice.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_invoice(self):
        response = self.client.delete(reverse('invoice-detail', kwargs={'pk': self.invoice.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
