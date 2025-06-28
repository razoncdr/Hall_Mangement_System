from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class CreateSSLCommerzCheckoutSessionSerializer(serializers.Serializer):
    success_url = serializers.URLField(required=True)
    cancel_url = serializers.URLField(required=True)
    fail_url = serializers.URLField(required=True)


class SSLCommerzCheckoutSessionResponseSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(help_text="Unique transaction identifier")
    gateway_page_url = serializers.URLField(help_text="URL to the SSLCommerz payment gateway page")
    redirect_gateway_url = serializers.URLField(help_text="URL to redirect to the payment gateway")
    all_gateway_urls = serializers.JSONField(help_text="List of available payment gateways with their details")


class SSLCommerzIPNSerializer(serializers.Serializer):
    class SSLCommerzIPNStatus(models.TextChoices):
        VALID = 'VALID', _('Valid')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        UNATTEMPTED = 'UNATTEMPTED', _('Unattempted')
        EXPIRED = 'EXPIRED', _('Expired')

    status = serializers.ChoiceField(choices=SSLCommerzIPNStatus.choices)
    tran_date = serializers.DateTimeField()
    tran_id = serializers.CharField()
    val_id = serializers.CharField(required=False, allow_null=True)

    verify_sign = serializers.CharField()
    verify_key = serializers.CharField()


class SSLCommerzValidationResponseSerializer(serializers.Serializer):
    class SSLCommerzValidationStatus(models.TextChoices):
        VALID = 'VALID', _('Valid')
        VALIDATED = 'VALIDATED', _('Validated')
        INVALID_TRANSACTION = 'INVALID_TRANSACTION', _('Invalid Transaction')

    status = serializers.ChoiceField(choices=SSLCommerzValidationStatus.choices)
    tran_date = serializers.DateTimeField()
    tran_id = serializers.CharField()
    val_id = serializers.CharField()

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    store_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    card_type = serializers.CharField(allow_blank=True)
    card_no = serializers.CharField(allow_blank=True)

    currency = serializers.CharField(max_length=3)
    bank_tran_id = serializers.CharField(allow_blank=True)
    card_issuer = serializers.CharField(allow_blank=True)
    card_brand = serializers.CharField(allow_blank=True)
    card_issuer_country = serializers.CharField(allow_blank=True)
    card_issuer_country_code = serializers.CharField(max_length=5, allow_blank=True)

    currency_type = serializers.CharField(max_length=5, allow_blank=True)
    currency_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True
    )

    risk_level = serializers.IntegerField()
    risk_title = serializers.CharField(allow_blank=True)
