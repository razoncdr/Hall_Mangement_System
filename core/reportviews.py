from django.shortcuts import (render)

from .decorators import *
from .forms import *


@allowed_users(allowed_roles=['Hall Provost', 'Admin', ])
def feestatementreport(request):
    studentfees = StudentFees.objects.none()

    form = StudentFeeStatementForm(request.POST or None)

    # if request.method == "POST":

    #     # form = CreateUserForm(request.POST)
    #     # if request.method.is_valid():

    #     ToDate = datetime.datetime.strptime(request.POST.get("To_Date"), "%Y-%m-%d") + datetime.timedelta(days=1)
    #     FromDate = datetime.datetime.strptime(request.POST.get("From_Date"), "%Y-%m-%d")

    #     studentfees = StudentFees.objects.filter(entryDate__gte=FromDate, 
    #                                               entryDate__lt=ToDate, ).order_by('-entryDate').all()
    #     if request.POST.get("feesHead") != "":
    #         # print("feesHeadid: " + request.POST.get("feesHead")) 
    #         studentfees = studentfees.filter(feeshead=request.POST.get("feesHead"))

    #     if request.POST.get("batch") != "":
    #         # print("batchid: " + request.POST.get("batch")) 
    #         studentfees = studentfees.filter(student__batch_id=request.POST.get("batch"))

    #     # if request.POST.get("hall") != "":
    #     #     print("hallid: " + request.POST.get("hall")) 
    #     #     studentfees = studentfees.filter(student__room__hall_id=request.POST.get("hall"))

    #     if request.POST.get("semester") != "":
    #         # print("semesterid: " + request.POST.get("semester")) 
    #         studentfees = studentfees.filter(semester_id=request.POST.get("semester"))

    #     if request.POST.get("registration_number") != "":
    #         # print(request.POST.get("registration_number")) 
    #         studentfees = studentfees.filter(student__registration_number=request.POST.get("registration_number"))

    #     if request.POST.get("payment_Status") != "":
    #         print(request.POST.get("payment_Status")) 
    #         payment_Status = Payment_Status(request.POST.get("payment_Status"))
    #         print(payment_Status)
    #         studentfees = studentfees.filter(paymentStatus=payment_Status)

    context = {
        'dataset': studentfees,
        'form': form,
    }
    return render(request, 'report/Fee_Statement.html', context)
