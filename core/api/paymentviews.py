import requests
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from HallManagementSystem.settings import SSLCOMMERZ_STORE_ID, SSLCOMMERZ_STORE_PASSWORD
from core.api.serializer import CreateSSLCommerzCheckoutSessionSerializer, SSLCommerzCheckoutSessionResponseSerializer, \
    SSLCommerzIPNSerializer, SSLCommerzValidationResponseSerializer
from core.models import SSLCommerzSession


class CreateSSLCommerzCheckoutSessionView(APIView):
    """
    API endpoint for creating a new SSLCommerz checkout session
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateSSLCommerzCheckoutSessionSerializer

    # @extend_schema(
    #     request=CreateSSLCommerzCheckoutSessionSerializer,
    #     responses={
    #         200: OpenApiResponse(
    #             response=SSLCommerzCheckoutSessionResponseSerializer,
    #             description="Checkout session created successfully"
    #         ),
    #         400: OpenApiResponse(
    #             description="Bad request",
    #             examples=[
    #                 OpenApiExample(
    #                     'SSLCommerz Error',
    #                     value={'error': 'Invalid request'},
    #                     status_codes=['400']
    #                 )
    #             ]
    #         ),
    #         500: OpenApiResponse(
    #             description="Server error",
    #             examples=[
    #                 OpenApiExample(
    #                     'Server Error',
    #                     value={'error': 'Internal server error'},
    #                     status_codes=['500']
    #                 )
    #             ]
    #         )
    #     },
    # )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user
        amount = 0
        currency = "BDT"

        if not amount or amount <= 0:
            return Response({'error': _("Invalid product price")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                sslcommerz_transaction = SSLCommerzSession.objects.create(
                    user=user,
                    currency_type=currency,
                    currency_amount=amount
                )

                # Prepare SSLCommerz request data
                post_data = {
                    "store_id": SSLCOMMERZ_STORE_ID,
                    "store_passwd": SSLCOMMERZ_STORE_PASSWORD,

                    "total_amount": amount,
                    "currency": currency,

                    "tran_id": sslcommerz_transaction.transaction_id,
                    "product_category": "digital",

                    "success_url": data.get('success_url'),
                    "fail_url": data.get('fail_url'),
                    "cancel_url": data.get('cancel_url'),
                    "ipn_url": request.build_absolute_uri(reverse("api:payments:v1:sslcommerz-ipn-capture")),

                    "multi_card_name": data.get('multi_card_name', ''),

                    "emi_option": 0,

                    "cus_name": f"{user.first_name} {user.last_name}",
                    "cus_email": user.email,
                    "cus_add1": "",
                    "cus_city": "",
                    "cus_postcode": "",
                    "cus_country": "Bangladesh",
                    "cus_phone": "01",

                    "shipping_method": "NO",

                    "num_of_item": 1,
                    "product_name": product.name,
                    "product_profile": "general",
                }

                # Make API request to SSLCommerz
                response = requests.post(SSLCOMMERZ_API_URL, data=post_data)
                response_data = response.json()

                if response_data.get("status") != "SUCCESS":
                    error_reason = response_data.get('failedreason', 'Unknown error')
                    raise ValueError(f"Payment initiation failed: {error_reason}")

                # Validate and prepare response
                response_serializer = SSLCommerzCheckoutSessionResponseSerializer(data={
                    'transaction_id': sslcommerz_transaction.transaction_id,
                    'gateway_page_url': response_data.get("GatewayPageURL"),
                    'redirect_gateway_url': response_data.get("redirectGatewayURL"),
                    'all_gateway_urls': response_data.get("desc"),
                })

                # Update transaction with session data
                sslcommerz_transaction.session_key = response_data.get("sessionkey")
                sslcommerz_transaction.status = SSLCommerzSession.SSLCommerzTransactionStatus.INITIATED
                sslcommerz_transaction.save()

                return Response(response_serializer.data)

        except requests.RequestException as req_err:
            return Response(
                {'error': _("Payment gateway error")},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except ValueError as val_err:
            return Response(
                {'error': str(val_err)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': _("Internal server error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SSLCommerzIPNListenerView(APIView):
    """
    Handles IPN (Instant Payment Notification) from SSLCOMMERZ and validates the transaction
    using the SSLCOMMERZ Validation API.
    """

    permission_classes = []
    serializer_class = SSLCommerzIPNSerializer

    def post(self, request, *args, **kwargs):
        # Step 1: Validate IPN data from SSLCOMMERZ
        ipn_serializer = self.serializer_class(data=request.data)
        ipn_serializer.is_valid(raise_exception=True)

        ipn_data = ipn_serializer.validated_data

        try:
            # Step 2: Fetch sslcommerz_transaction from DB
            tran_id = ipn_data.get("tran_id")
            sslcommerz_transaction = SSLCommerzSession.objects.get(transaction_id=tran_id)

            # Step 3(Invalid): Manage Unsuccessful Transaction
            if ipn_data.get("status") != SSLCommerzIPNSerializer.SSLCommerzIPNStatus.VALID:
                sslcommerz_transaction.status = ipn_data.get("status")
                sslcommerz_transaction.transaction_date = ipn_data.get("tran_date")
                sslcommerz_transaction.validated_on = timezone.now()

                sslcommerz_transaction.verify_sign = ipn_data.get('verify_sign')
                sslcommerz_transaction.verify_key = ipn_data.get('verify_key')

                sslcommerz_transaction.save()

                return Response(status=status.HTTP_200_OK)

            # Step 3(Valid): Prepare Validation API request to SSLCOMMERZ
            # validation_url = SSLCOMMERZ_VALIDATION_URL
            params = {
                "val_id": ipn_data.get('val_id'),
                "store_id": SSLCOMMERZ_STORE_ID,
                "store_passwd": SSLCOMMERZ_STORE_PASSWORD,
                "v": 1,
                "format": "json"
            }

            response = requests.get(validation_url, params=params)
            if response.status_code != status.HTTP_200_OK:
                return Response(
                    {"error": _("Failed to validate transaction with SSLCOMMERZ")},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Step 4: Validate the response data from SSLCOMMERZ validation API
            validation_serializer = SSLCommerzValidationResponseSerializer(data=response.json())
            validation_serializer.is_valid(raise_exception=True)

            validation_data = validation_serializer.validated_data

            if validation_data.get('status') not in [
                SSLCommerzValidationResponseSerializer.SSLCommerzValidationStatus.VALID,
                SSLCommerzValidationResponseSerializer.SSLCommerzValidationStatus.VALIDATED
            ]:
                return Response({"error": _("Transaction is not valid")}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # Step 5: Verify amount and currency match the transaction record
                if (validation_data.get('currency_amount') is not None
                        and sslcommerz_transaction.currency_amount != validation_data.get('currency_amount')):
                    return Response({"error": _("Amount mismatch")}, status=status.HTTP_400_BAD_REQUEST)

                if (validation_data.get('currency_type') != ""
                        and sslcommerz_transaction.currency_type != validation_data.get('currency_type')):
                    return Response({"error": _("Currency mismatch")}, status=status.HTTP_400_BAD_REQUEST)

                # Step 6: Create Sale and Update sslcommerz_transaction record
                # fee_transaction, created = FeeTransaction.objects.get_or_create(
                #
                # )

                sslcommerz_transaction.validation_id = validation_data.get('val_id')

                # Transaction status and dates
                sslcommerz_transaction.status = ipn_data.get('status')
                sslcommerz_transaction.transaction_date = validation_data.get('tran_date')
                sslcommerz_transaction.validated_on = timezone.now()

                # Amount and currency information
                sslcommerz_transaction.currency = validation_data.get('currency')
                sslcommerz_transaction.amount = validation_data.get('amount')
                sslcommerz_transaction.store_amount = validation_data.get('store_amount')

                # Payment method details
                sslcommerz_transaction.card_type = validation_data.get('card_type')
                sslcommerz_transaction.card_no = validation_data.get('card_no')
                sslcommerz_transaction.card_brand = validation_data.get('card_brand')
                sslcommerz_transaction.card_issuer = validation_data.get('card_issuer')
                sslcommerz_transaction.card_issuer_country = validation_data.get('card_issuer_country')
                sslcommerz_transaction.card_issuer_country_code = validation_data.get('card_issuer_country_code')
                sslcommerz_transaction.bank_tran_id = validation_data.get('bank_tran_id')

                # Security and validation
                sslcommerz_transaction.verify_sign = ipn_data.get('verify_sign')
                sslcommerz_transaction.verify_key = ipn_data.get('verify_key')

                # Risk assessment
                sslcommerz_transaction.risk_level = validation_data.get('risk_level')
                sslcommerz_transaction.risk_title = validation_data.get('risk_title')

                sslcommerz_transaction.save()

                return Response(status=status.HTTP_200_OK)

        except SSLCommerzSession.DoesNotExist:
            return Response(
                {"error": _("Transaction not found in the system")},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": _("Internal server error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
