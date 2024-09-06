from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'unit_price', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'date', 'customer_name', 'invoice_details']

    def create(self, validated_data):
        # Extract the nested invoice details data
        invoice_details_data = validated_data.pop('invoice_details', [])
        # Create the Invoice object
        invoice = Invoice.objects.create(**validated_data)
        # Create each InvoiceDetail object and associate it with the newly created Invoice
        for detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        # Extract nested invoice details data
        invoice_details_data = validated_data.pop('invoice_details', [])

        # Update Invoice instance fields
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        # Update or create each invoice detail
        existing_detail_ids = [detail.id for detail in instance.invoice_details.all()]
        new_detail_ids = [item.get('id') for item in invoice_details_data if item.get('id') is not None]

        # Remove details not included in the updated data
        for detail_id in existing_detail_ids:
            if detail_id not in new_detail_ids:
                InvoiceDetail.objects.filter(id=detail_id, invoice=instance).delete()

        # Process each detail in the input data
        for detail_data in invoice_details_data:
            detail_id = detail_data.get('id', None)
            if detail_id and InvoiceDetail.objects.filter(id=detail_id, invoice=instance).exists():
                # Update existing details
                detail = InvoiceDetail.objects.get(id=detail_id, invoice=instance)
                detail.description = detail_data.get('description', detail.description)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                detail.price = detail_data.get('price', detail.price)
                detail.save()
            else:
                # Create new details
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
