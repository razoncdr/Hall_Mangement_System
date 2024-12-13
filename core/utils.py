import datetime
import random
import string
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from core.models import DormitoryApplications

def generate_random_password(length=10):
    """
    Generate a random password with letters, digits, and punctuation.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def generate_verification_link(dorm_application):
    from django.urls import reverse
    uuid = dorm_application.uuid
    token = dorm_application.token  # Use the pre-generated token from the model
    verification_url = reverse('verify_email', kwargs={'uuid': uuid, 'token': token})
    return verification_url


def send_email_to_user(email, subject, message):
    """
    Utility function to send email to the user.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email='no-reply@example.com',
        recipient_list=[email],
        fail_silently=False
    )
