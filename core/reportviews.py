from django.db.models import Prefetch
from django.shortcuts import (render)

from .decorators import *
from .forms import *


@allowed_users(allowed_roles=['Hall Provost', 'Admin', 'Operator'])
def fee_transaction_report(request):
    student_fees = StudentFees.objects.none()
    form = StudentFeeTransactionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Extract cleaned form data
        cd = form.cleaned_data

        # Filter by Date Range
        from_date = cd.get("From_Date")
        to_date = cd.get("To_Date")
        to_date = to_date + datetime.timedelta(days=1)
        student_fees = StudentFees.objects.filter(
            fee_transactions__transaction_date__gte=from_date,
            fee_transactions__transaction_date__lt=to_date
        )

        # Apply optional filters
        if cd.get("session"):
            student_fees = student_fees.filter(student__session=cd["session"])

        if cd.get("batch"):
            student_fees = student_fees.filter(student__batch=cd["batch"])

        if cd.get("semester"):
            student_fees = student_fees.filter(semester=cd["semester"])

        if cd.get("feesHead"):
            student_fees = student_fees.filter(feeshead=cd["feesHead"])

        if cd.get("registration_number"):
            student_fees = student_fees.filter(student__registration_number__icontains=cd["registration_number"])

        student_fees = student_fees.select_related('student').prefetch_related(
            Prefetch(
                'fee_transactions',
                queryset=FeeTransaction.objects.select_related('sslcommerz_session')
            )
        ).order_by('-fee_transactions__transaction_date')

    context = {
        'dataset': student_fees,
        'form': form,
    }
    return render(request, 'report/fee_transaction_report.html', context)
