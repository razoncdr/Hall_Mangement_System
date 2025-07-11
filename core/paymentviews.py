from django.db import models
from django.shortcuts import render

from core.decorators import allowed_users
from core.models import StudentFees, Payment_Status, Student


@allowed_users(allowed_roles=['Student'])
def fee_payment(request):
    student = Student.objects.filter(userprofile__user=request.user).first()
    unpaid_fees = StudentFees.objects.filter(student=student, paymentStatus=Payment_Status.UNPAID)
    total_amount = unpaid_fees.aggregate(total=models.Sum('amount'))['total'] or 0

    return render(request, 'student_fee/fee_payment.html', {
        "student": student,
        "unpaid_fees": unpaid_fees,
        "total_amount": total_amount,
    })

@allowed_users(allowed_roles=['Student'])
def fee_payment_history(request):
    student = Student.objects.get(userprofile__user=request.user)
    paid_fees = (
        StudentFees.objects
        .filter(student=student, paymentStatus=Payment_Status.PAID)
        .prefetch_related('fee_transactions')
        .order_by('-entryDate')
    )

    return render(request, 'student_fee/fee_payment_history.html', {
        "student": student,
        "paid_fees": paid_fees,
    })


def payment_success(request):
    return render(request, 'student_fee/payment_success.html')


def payment_fail(request):
    return render(request, 'student_fee/payment_fail.html')


def payment_cancel(request):
    return render(request, 'student_fee/payment_cancel.html')
