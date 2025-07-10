import requests
from django.db import transaction, models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from HallManagementSystem.settings import SSLCOMMERZ_STORE_ID, SSLCOMMERZ_STORE_PASSWORD
from core.api.permissions import IsStudent
from core.api.serializer import CreateSSLCommerzCheckoutSessionSerializer, SSLCommerzCheckoutSessionResponseSerializer, \
    SSLCommerzCaptureSerializer, SSLCommerzValidationResponseSerializer
from core.models import SSLCommerzSession, Student, FeeTransaction, StudentFees, Payment_Status


class CreateSSLCommerzCheckoutSessionView(APIView):
    """
    API endpoint for creating a new SSLCommerz checkout session
    """

    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CreateSSLCommerzCheckoutSessionSerializer

    @extend_schema(
        request=CreateSSLCommerzCheckoutSessionSerializer,
        responses={
            200: OpenApiResponse(
                response=SSLCommerzCheckoutSessionResponseSerializer,
                description="Checkout session created successfully"
            ),
            400: OpenApiResponse(
                description="Bad request",
                examples=[
                    OpenApiExample(
                        'SSLCommerz Error',
                        value={'error': 'Invalid request'},
                        status_codes=['400']
                    )
                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            with transaction.atomic():
                user = request.user
                student = Student.objects.get(userprofile__user=user)
                amount = StudentFees.objects.filter(
                    student=student,
                    paymentStatus=Payment_Status.UNPAID
                ).aggregate(total=models.Sum('amount'))['total'] or 0
                currency = "BDT"

                if not amount or amount <= 0:
                    return Response({'error': _("Invalid product price")}, status=status.HTTP_400_BAD_REQUEST)

                sslcommerz_session = SSLCommerzSession.objects.create(
                    student=student,
                    currency_type=currency,
                    currency_amount=amount
                )

                # Prepare SSLCommerz request data
                post_data = {
                    "store_id": SSLCOMMERZ_STORE_ID,
                    "store_passwd": SSLCOMMERZ_STORE_PASSWORD,

                    "total_amount": amount,
                    "currency": currency,

                    "tran_id": sslcommerz_session.transaction_id,
                    "product_category": "education",

                    "success_url": request.build_absolute_uri(reverse("sslcommerz-capture")),
                    "fail_url": request.build_absolute_uri(reverse("sslcommerz-capture")),
                    "cancel_url": request.build_absolute_uri(reverse("sslcommerz-capture")),

                    "multi_card_name": data.get('multi_card_name', ''),

                    "emi_option": 0,

                    "cus_name": student.fullName,
                    "cus_email": student.email,
                    "cus_add1": "",
                    "cus_city": "",
                    "cus_postcode": "",
                    "cus_country": "Bangladesh",
                    "cus_phone": str(student.phone),

                    "shipping_method": "NO",

                    "num_of_item": 1,
                    "product_name": "Hall Fee",
                    "product_profile": "general",
                }

                # Make API request to SSLCommerz
                sslcommerz_api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
                response = requests.post(sslcommerz_api_url, data=post_data)
                response_data = response.json()

                if response_data.get("status") != "SUCCESS":
                    error_reason = response_data.get('failed_reason', 'Unknown error')
                    raise ValueError(f"Payment initiation failed: {error_reason}")

                # Validate and prepare response
                response_serializer = SSLCommerzCheckoutSessionResponseSerializer(data={
                    'transaction_id': sslcommerz_session.transaction_id,
                    'gateway_page_url': response_data.get("GatewayPageURL"),
                    'redirect_gateway_url': response_data.get("redirectGatewayURL"),
                    'all_gateway_urls': response_data.get("desc"),
                })
                response_serializer.is_valid(raise_exception=True)

                # Update transaction with session data
                sslcommerz_session.session_key = response_data.get("sessionkey")
                sslcommerz_session.status = SSLCommerzSession.SSLCommerzTransactionStatus.UNATTEMPTED
                sslcommerz_session.save()

                return Response(response_serializer.data, status=status.HTTP_200_OK)

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
        except Student.DoesNotExist:
            return Response(
                {'error': _("Student not found")},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error occurred: {e}")
            return Response(
                {'error': _("Internal server error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SSLCommerzPaymentCaptureView(APIView):
    """
    Handles Payment Capture or IPN from SSLCOMMERZ and validates the transaction
    using the SSLCOMMERZ Validation API.
    """

    permission_classes = []
    serializer_class = SSLCommerzCaptureSerializer

    def post(self, request, *args, **kwargs):
        try:
            # Step 1: Validate IPN data from SSLCOMMERZ
            ipn_serializer = self.serializer_class(data=request.data)
            ipn_serializer.is_valid(raise_exception=True)
            ipn_data = ipn_serializer.validated_data

            # Step 2: Fetch sslcommerz_session from DB
            tran_id = ipn_data.get("tran_id")
            sslcommerz_session = SSLCommerzSession.objects.get(transaction_id=tran_id)

            # Step 3(Invalid): Manage Unsuccessful Transaction
            if ipn_data.get("status") != SSLCommerzSession.SSLCommerzTransactionStatus.VALID:
                sslcommerz_session.status = ipn_data.get("status")
                # sslcommerz_session.validated_on = ipn_data.get("tran_date")

                sslcommerz_session.verify_sign = ipn_data.get('verify_sign')
                sslcommerz_session.verify_key = ipn_data.get('verify_key')

                sslcommerz_session.save()

                return Response(status=status.HTTP_200_OK)

            # Step 3(Valid): Prepare Validation API request to SSLCOMMERZ
            params = {
                "val_id": ipn_data.get('val_id'),
                "store_id": SSLCOMMERZ_STORE_ID,
                "store_passwd": SSLCOMMERZ_STORE_PASSWORD,
            }

            validation_url = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"
            response = requests.get(validation_url, params=params)
            if response.status_code != status.HTTP_200_OK:
                return Response(
                    {"error": _("Failed to validate transaction with SSLCOMMERZ")},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Step 4: Validate the response data from SSLCOMMERZ validation API
            validation_serializer = SSLCommerzValidationResponseSerializer(data=response.json())
            validation_serializer.is_valid(raise_exception=False)
            validation_data = validation_serializer.validated_data

            if validation_data.get('status') not in [
                SSLCommerzValidationResponseSerializer.SSLCommerzValidationStatus.VALID,
                SSLCommerzValidationResponseSerializer.SSLCommerzValidationStatus.VALIDATED
            ]:
                return Response({"error": _("Transaction is not valid")}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                # Step 5: Verify amount and currency match the transaction record
                if (validation_data.get('currency_amount') is not None
                        and sslcommerz_session.currency_amount != validation_data.get('currency_amount')):
                    return Response({"error": _("Amount mismatch")}, status=status.HTTP_400_BAD_REQUEST)

                if (validation_data.get('currency_type') != ""
                        and sslcommerz_session.currency_type != validation_data.get('currency_type')):
                    return Response({"error": _("Currency mismatch")}, status=status.HTTP_400_BAD_REQUEST)

                # Step 6: Create FeeTransaction and Update sslcommerz_session record
                unpaid_fees = StudentFees.objects.filter(
                    student=sslcommerz_session.student,
                    paymentStatus=Payment_Status.UNPAID
                )
                fee_transaction, created = FeeTransaction.objects.get_or_create(
                    transaction_id=sslcommerz_session.transaction_id,
                    defaults={
                        'student': sslcommerz_session.student,
                        'paid_amount': sslcommerz_session.currency_amount,
                        'transaction_date': validation_data.get('tran_date'),
                    }
                )
                if created:
                    fee_transaction.student_fee.set(unpaid_fees)
                    unpaid_fees.update(paymentStatus=Payment_Status.PAID)

                sslcommerz_session.validation_id = validation_data.get('val_id')
                sslcommerz_session.fee_transaction = fee_transaction

                # Transaction status and dates
                sslcommerz_session.status = ipn_data.get('status')
                sslcommerz_session.validated_on = timezone.now()

                # Amount and currency information
                sslcommerz_session.currency = validation_data.get('currency')
                sslcommerz_session.amount = validation_data.get('amount')
                sslcommerz_session.store_amount = validation_data.get('store_amount')

                # Payment method details
                sslcommerz_session.card_type = validation_data.get('card_type')
                sslcommerz_session.card_no = validation_data.get('card_no')
                sslcommerz_session.card_brand = validation_data.get('card_brand')
                sslcommerz_session.card_issuer = validation_data.get('card_issuer')
                sslcommerz_session.card_issuer_country = validation_data.get('card_issuer_country')
                sslcommerz_session.card_issuer_country_code = validation_data.get('card_issuer_country_code')
                sslcommerz_session.bank_tran_id = validation_data.get('bank_tran_id')

                # Security and validation
                sslcommerz_session.verify_sign = ipn_data.get('verify_sign')
                sslcommerz_session.verify_key = ipn_data.get('verify_key')

                # Risk assessment
                sslcommerz_session.risk_level = validation_data.get('risk_level')
                sslcommerz_session.risk_title = validation_data.get('risk_title')

                sslcommerz_session.save()

                return Response(status=status.HTTP_200_OK)

        except SSLCommerzSession.DoesNotExist:
            return Response(
                {"error": _("Transaction not found in the system")},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print("Error in SSLCommerz IPN Listener:", e)
            return Response(
                {"error": _("Internal server error")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
