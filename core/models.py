import random
import secrets
import string
import uuid
from enum import Enum

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STATUS = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

Transaction_Type = (
    ('cash', 'Cash'),
    ('bkash', 'Bkash'),
    ('rocket', 'Rocket'),
    ('nagad', 'Nagad'),
)


class Payment_Status(Enum):
    PAID = 'P'
    UNPAID = 'U'


class Semester_Status(Enum):
    Semester_1 = '1-1'
    Semester_2 = '1-2'
    Semester_3 = '2-1'
    Semester_4 = '2-2'
    Semester_5 = '3-1'
    Semester_6 = '3-2'
    Semester_7 = '4-1'
    Semester_8 = '4-2'


class Application_Status(Enum):
    Pending = 'pending'
    Approved = 'approved'
    Rejected = 'rejected'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='userprofile'
    )
    fullName = models.CharField(max_length=400, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    entryDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullName


class Hall(models.Model):
    name = models.CharField(max_length=50)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.RESTRICT)
    name = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=10, decimal_places=0)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name} ({self.hall})"


class Batch(models.Model):
    name = models.CharField(max_length=50)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    name = models.CharField(max_length=100)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"


class Session(models.Model):
    name = models.CharField(max_length=50)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"


class Semester(models.Model):
    name = models.CharField(max_length=50)

    # Add other attributes as needed
    def __str__(self):
        return f"{self.name}"


class DormitoryApplications(models.Model):
    # Add fields for application details
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(default=secrets.token_urlsafe, max_length=64, unique=True)
    session = models.ForeignKey(Session, on_delete=models.RESTRICT)
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    semester = EnumChoiceField(Semester_Status, default=Semester_Status.Semester_1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    preferred_room = models.ForeignKey(Room, on_delete=models.RESTRICT, blank=True, null=True)

    registration_number = models.CharField(max_length=20)
    fullName = models.CharField(max_length=400)
    birthDate = models.DateField()
    gender = models.CharField(choices=GENDER, max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='ApplicationImages')
    idCardPicture = models.ImageField(upload_to='ApplicationImages', blank=True, null=True)
    # medical_certificate = models.ImageField(upload_to='ApplicationImages')

    guardian_name = models.CharField(max_length=400)
    guardian_relation = models.CharField(max_length=400)
    guardian_phone = PhoneNumberField()
    guardian_address = models.CharField(max_length=400)

    application_status = EnumChoiceField(Application_Status, default=Application_Status.Pending)
    application_date = models.DateTimeField()
    remarks = models.TextField()
    review_date = models.DateTimeField(blank=True, null=True)


class Student(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    userprofile = models.OneToOneField(
        UserProfile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='student'
    )

    session = models.ForeignKey(Session, on_delete=models.RESTRICT)
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    semester = EnumChoiceField(Semester_Status, default=Semester_Status.Semester_1)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)

    registration_number = models.CharField(max_length=20)
    fullName = models.CharField(max_length=400)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=20)
    phone = PhoneNumberField()
    email = models.EmailField()
    picture = models.ImageField(upload_to='ApplicationImages')
    idCardPicture = models.ImageField(upload_to='ApplicationImages', blank=True, null=True)

    guardian_name = models.CharField(max_length=400)
    guardian_relation = models.CharField(max_length=400)
    guardian_phone = PhoneNumberField()
    guardian_address = models.CharField(max_length=400)

    status = models.CharField(choices=STATUS, max_length=20)

    # Add other attributes related to a student

    def __str__(self):
        return f"{self.fullName} ({self.registration_number})"


class FeesHead(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.amount})"


class StudentFees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    feeshead = models.ForeignKey(FeesHead, on_delete=models.RESTRICT)
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentStatus = EnumChoiceField(Payment_Status, default=Payment_Status.UNPAID)
    entryuser = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    entryDate = models.DateTimeField(null=True, blank=True)


class FeeTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='fee_transactions')
    student_fee = models.ManyToManyField('StudentFees', related_name='fee_transactions')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=255,
        unique=True
    )
    transactionDetails = models.TextField()
    transaction_date = models.DateTimeField(
        verbose_name=_('transaction date'),
        blank=True,
        null=True,
        help_text=_('Payment completion timestamp')
    )


class SSLCommerzSession(models.Model):
    class SSLCommerzTransactionStatus(models.TextChoices):
        """
        UNATTEMPTED: Customer did not choose to pay any channel.
        VALID: A successful transaction.
        FAILED: Transaction is declined by the customer's Issuer Bank.
        CANCELLED: Transaction is canceled by the customer.
        EXPIRED: Payment Timeout.
        """
        VALID = 'VALID', _('Valid')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        UNATTEMPTED = 'UNATTEMPTED', _('Unattempted')
        EXPIRED = 'EXPIRED', _('Expired')

    # Core transaction identifiers
    session_key = models.CharField(
        verbose_name=_('session key'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('SSLCOMMERZ session identifier for transaction tracking')
    )
    validation_id = models.CharField(
        verbose_name=_('validation id'),
        max_length=255,
        blank=True,
        help_text=_('SSLCOMMERZ validation identifier')
    )
    transaction_id = models.CharField(
        verbose_name=_('transaction id'),
        max_length=255,
        unique=True,
        help_text=_('Auto-generated ID in format: XXX_XXX_XXXXXXXXXX')
    )

    # Relationships
    fee_transaction = models.OneToOneField(
        verbose_name=_("fee transaction"),
        to=FeeTransaction,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sslcommerz_sessions',
    )
    student = models.ForeignKey(
        verbose_name=_("student"),
        to=Student,
        on_delete=models.PROTECT,
        related_name='sslcommerz_sessions',
    )

    # Transaction status and dates
    status = models.CharField(
        verbose_name=_('status'),
        choices=SSLCommerzTransactionStatus.choices,
        default=SSLCommerzTransactionStatus.UNATTEMPTED,
        max_length=50
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        help_text=_('Transaction creation timestamp')
    )
    validated_on = models.DateTimeField(
        verbose_name=_('validated date'),
        blank=True,
        null=True,
        help_text=_('Transaction validation timestamp')
    )

    # Amount and currency information
    currency = models.CharField(
        verbose_name=_('currency'),
        max_length=10,
        default='BDT',
        help_text=_('Merchant settlement currency (e.g., BDT, USD)')
    )
    currency_type = models.CharField(
        verbose_name=_('currency type'),
        max_length=10,
        default='BDT',
        help_text=_('Transaction request currency')
    )
    currency_amount = models.DecimalField(
        verbose_name=_('currency amount'),
        max_digits=12,
        decimal_places=2,
        help_text=_('Transaction request amount')
    )
    amount = models.DecimalField(
        verbose_name=_('amount'),
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
        help_text=_('Final amount after conversions')
    )
    store_amount = models.DecimalField(
        verbose_name=_('store amount'),
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
        help_text=_('Net amount after bank charges')
    )

    # Payment method details
    card_type = models.CharField(
        verbose_name=_('card type'),
        max_length=255,
        blank=True,
        help_text=_('Payment method (e.g., VISA, BKASH)')
    )
    card_no = models.CharField(
        verbose_name=_('card number'),
        max_length=120,
        blank=True,
        help_text=_('Customer card number or mobile banking reference')
    )
    card_brand = models.CharField(
        verbose_name=_('card brand'),
        max_length=55,
        blank=True,
        help_text=_('Payment brand (VISA, MASTER, AMEX, IB, MOBILEBANKING, etc.)')
    )
    card_issuer = models.CharField(
        verbose_name=_('issuer bank name'),
        max_length=120,
        blank=True,
        help_text=_('Issuing bank name')
    )
    card_issuer_country = models.CharField(
        verbose_name=_('card issuer country'),
        max_length=120,
        blank=True,
        help_text=_('Issuer country name')
    )
    card_issuer_country_code = models.CharField(
        verbose_name=_('card issuer country code'),
        max_length=5,
        blank=True,
        help_text=_('ISO country code')
    )
    bank_tran_id = models.CharField(
        verbose_name=_('bank transaction id'),
        max_length=120,
        blank=True,
        help_text=_('Bank\'s transaction ID')
    )

    # Security and validation
    verify_sign = models.CharField(
        verbose_name=_('verify sign'),
        max_length=255,
        blank=True,
        help_text=_('Cryptographic signature for IPN data validation')
    )
    verify_key = models.CharField(
        verbose_name=_('verify key'),
        max_length=1024,
        blank=True,
        help_text=_('Parameters used for signature')
    )

    # Risk assessment
    risk_level = models.IntegerField(
        verbose_name=_('risk level'),
        blank=True,
        null=True,
        help_text=_('transaction risk level (0 = safe, 1 = high risk)')
    )
    risk_title = models.CharField(
        verbose_name=_('risk title'),
        max_length=50,
        blank=True,
        help_text=_('Risk assessment details')
    )

    def generate_unique_transaction_id(self):
        prefix = 'hms_'
        product_identifier = str(self.student.fullName).zfill(3)
        transaction_id = None
        unique = False

        while not unique:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            transaction_id = f"{prefix}{product_identifier}_{random_suffix}"
            if not SSLCommerzSession.objects.filter(transaction_id=transaction_id).exists():
                unique = True

        return transaction_id

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_unique_transaction_id()
        super().save(*args, **kwargs)
