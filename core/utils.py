from django.contrib.auth.tokens import default_token_generator
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_decode
# from django.contrib import messages
# from core.models import DormitoryApplications

def generate_verification_link(dorm_application):
    from django.urls import reverse
    uuid = dorm_application.uuid
    token = dorm_application.token  # Use the pre-generated token from the model
    verification_url = reverse('verify_email', kwargs={'uuid': uuid, 'token': token})
    return verification_url
