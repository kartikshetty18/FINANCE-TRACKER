from django.shortcuts import render,redirect
from myapp.models import UserLogin,AddEmployee,CapitalInterest,AddCustomer,AddLoan,LoanHistory,BankTransaction,OtpCode
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Max,Sum
import datetime
import smtplib
import os
import random
from datetime import datetime
from datetime import date
from django.contrib import messages
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import date




def index(request):
    return render(request,'index.html')


def admin_home(request):
    if 'username' in request.session:
        count1=AddEmployee.objects.count()
        count2=AddCustomer.objects.count()
        count3=AddLoan.objects.count()
        data=AddLoan.objects.all()
        return render(request, 'admin_dashboard.html', {'user': request.session['username'],'count1':count1,'count2':count2,'count3':count3,'data':data})
    return redirect('login')




def user_home(request):
    return render(request,'user_home.html')


def agent_home(request):
    username=request.session['username']
    data=AddLoan.objects.filter(agent=username).all()
    return render(request,'agent_home.html',{'data':data})


def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        request.session['username']=username
        password = request.POST.get('password')
        count=UserLogin.objects.filter(username=username).count()
        if count>=1:
            data=UserLogin.objects.get(username=username)
            upass=data.password
            utype=data.utype
            if upass == password:
                if utype=='admin':
                    return redirect('admin_home')
                if utype=='user':
                    return redirect('user_home')

                if utype=='agent':
                    return redirect('agent_home')
            else:
                return render(request, 'login.html', {'success': 'incorrect password'})

        else:
            return render(request, 'login.html', {'success': 'incorrect username'})

    return render(request, 'login.html')


def registration(request):
    return render(request,'registration.html')

def password(request):
    return render(request,'password.html')


def bankTransaction(request):
    if request.method=="POST":
        date = request.POST.get('date')
        particular = request.POST.get('particular')
        amount = request.POST.get('amount')
        note = request.POST.get('note')
        transaction = request.POST.get('transaction_type')
        if transaction=='Deposit':
            BankTransaction.objects.create(date=date,particular=particular,note=note,deposit=amount,withdraw=0)

        if transaction == 'Withdraw':
            BankTransaction.objects.create(date=date, particular=particular, note=note, deposit=0, withdraw=amount)

        return render(request,'bankTransaction.html', {'success':'Added successfully'})
    return render(request, 'bankTransaction.html')





def customer(request):
    last_id = AddCustomer.objects.aggregate(Max('cust_id'))['cust_id__max']
    new_cust_id = 1 if last_id is None else int(last_id) + 1

    if request.method == 'POST':
        name = request.POST.get('name')
        aadhar_no = request.POST.get('aadhar_no')
        mobile_no = request.POST.get('mobile_no')
        district = request.POST.get('district')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        occupation = request.POST.get('occupation')
        utype = request.POST.get('utype', 'customer')
        UserLogin.objects.create(username=aadhar_no,password=mobile_no,utype='customer')


        AddCustomer.objects.create(
            name=name,
            aadhar_no=aadhar_no,
            mobile_no=mobile_no,
            district=district,
            city=city,
            pincode=pincode,
            occupation=occupation,
            cust_id=new_cust_id,
            utype=utype
        )


        return render(request, 'customer.html', {'success': f'Customer added successfully with ID {new_cust_id}'})

    return render(request, 'customer.html',{'new_cust_id':new_cust_id})


from django.shortcuts import render
from .models import AddEmployee, UserLogin

def employee(request):
    if request.method == 'POST':
        emp_type = request.POST.get('emp_type')
        emp_name = request.POST.get('emp_name')
        mobile_no = request.POST.get('mobile_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        upload_aadhar = request.FILES.get('upload_aadhar')
        address = request.POST.get('address')

        # Check username already exists
        if UserLogin.objects.filter(username=username).exists():
            return render(request, 'employee.html', {
                'error': 'Username already exists'
            })

        # Save employee
        AddEmployee.objects.create(
            emp_type=emp_type,
            emp_name=emp_name,
            mobile_no=mobile_no,
            username=username,
            password=password,
            upload_aadhar=upload_aadhar,
            address=address
        )

        # Save login
        UserLogin.objects.create(
            username=username,
            password=password,
            utype='agent'
        )

        return render(request, 'employee.html', {
            'success': 'Added successfully'
        })

    return render(request, 'employee.html')




def generate_acc_no():
    current_year = datetime.now().year
    prefix = str(current_year)

    # Get all acc_no entries starting with current year
    acc_nos = AddLoan.objects.filter(acc_no__startswith=prefix).values_list('acc_no', flat=True)

    max_num = 0
    for acc in acc_nos:
        try:
            # Split like "2025-01" -> ['2025', '01']
            num = int(acc.split('-')[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            continue  # skip malformed entries

    next_num = max_num + 1
    return f"{prefix}-{next_num:02d}"


def loan(request):
    acc_no = generate_acc_no()  # <-- Auto-generate acc_no here
    data = AddEmployee.objects.all()
    cdata = AddCustomer.objects.all()
    today = date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        agent = request.POST.get('agent')
        cust_no = request.POST.get('cname')
        amount = request.POST.get('amount')
        interest = request.POST.get('interest')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')
        loan_status = 'open'
        payment_mode = request.POST.get('payment_mode')



        AddLoan.objects.create(
            agent=agent,
            acc_no=acc_no,
            cust_no=cust_no,
            amount=amount,
            interest=interest,
            issue_date=issue_date,
            due_date=due_date,
            loan_status=loan_status,
            payment_mode=payment_mode
        )

        CapitalInterest.objects.create(amount=amount,cdate=today)
        return render(request, 'loan.html', {
            'success': f'Loan added successfully. Account No: {acc_no}',
            'data': data,'cdata':cdata,'today':today
        })

    return render(request, 'loan.html', {'data': data,'acc_no':acc_no,'cdata':cdata,'today':today})

def loan_history(request):
    if request.method=='POST':
        agent = request.POST.get('agent')
        customer = request.POST.get('customer')
        acc_no = request.POST.get('acc_no')
        amount = request.POST.get('amount')
        deposit_date = request.POST.get('deposit_date')
        particulars = request.POST.get('particulars')
        approve_status = request.POST.get('approve_status')
        LoanHistory.objects.create(agent=agent,customer=customer,acc_no=acc_no,amount=amount,deposit_date=deposit_date,particulars=particulars,approve_status=approve_status)
        return render(request,  'loan_history.html',{'success':'Added Successfully'})
    return render(request, 'loan_history.html')

def forgetpassword(request):
    if request.method=="POST":
        username=request.POST.get('email')
        request.session['username']=username
        ucheck=UserLogin.objects.filter(username=username).count()
        if ucheck>=1:
            otp =random.randint(1000,9999)
            OtpCode.objects.create(otp_code=otp,status='active')
            subject = "OTP Verification"
            body = f"Your OTP is: {otp}\n\nDo not share this OTP with anyone."
            message = f"Subject: {subject}\n\n{body}"
            mail=smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('vvkvk619@gmail.com','sezs eivs wkpt naim')
            mail.sendmail('vvkvk619@gmail.com',username,message)
            mail.close()
        else:
            return render(request,'forgetpassword.html',{'msg':"inalid username"})
    return render(request,'forgetpassword.html')
def otp(request):
    if request.method=="POST":
        otp=request.POST.get('t1')
        ucheck=OtpCode.objects.filter(otp_code=otp).count()
        if ucheck>=1:
            return redirect('resetpassword')
        else:
            return render(request,'otp.html',{'msg':'invalid otp'})
    return render(request,'otp.html')

def resetpassword(request):
    username = request.session.get('username')  # safer than direct access
    if request.method == "POST":
        newpassword = request.POST.get('t1')
        confirmpassword = request.POST.get('t2')
        if newpassword == confirmpassword:
            UserLogin.objects.filter(username=username).update(password=newpassword)
            return redirect('login_auth')
        else:
            return render(request, 'resetpassword.html', {'msg': 'New password and confirm password must be the same.'})
    return render(request, 'resetpassword.html')









def employee_view(request):
    udata=AddEmployee.objects.all()
    return render(request,'employee_view.html',{'udata':udata})


def customer_view(request):
    udata=AddCustomer.objects.all()
    return render(request,'customer_view.html',{'udata':udata})

def loan_view(request):
    udata=AddLoan.objects.all()
    return render(request,'loan_view.html',{'udata':udata})



def loan_history_view(request):
    data = AddEmployee.objects.all()
    udata = LoanHistory.objects.none()
    total_amount = 0
    selected_agent = None

    if request.method == "POST":
        selected_agent = request.POST.get('agent')

        if 'approve' in request.POST:
            selected_ids = request.POST.getlist('selected_ids')
            if selected_ids:
                LoanHistory.objects.filter(id__in=selected_ids).update(approve_status='Approved')

        if selected_agent:
            udata = LoanHistory.objects.filter(agent=selected_agent)
            total_amount = udata.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'agent_wise_collection.html', {
        'data': data,
        'udata': udata,
        'total_amount': total_amount,
        'selected_agent': selected_agent,
    })



def bankTransaction_view(request):
    udata = BankTransaction.objects.all()

    total_deposit = udata.aggregate(Sum('deposit'))['deposit__sum'] or 0
    total_withdraw = udata.aggregate(Sum('withdraw'))['withdraw__sum'] or 0
    balance = total_deposit - total_withdraw

    context = {
        'udata': udata,
        'total_deposit': total_deposit,
        'total_withdraw': total_withdraw,
        'balance': balance
    }
    return render(request, 'BankTransaction_view.html', context)

def employee_del(request,pk):
    udata = AddEmployee.objects.get(id=pk)
    udata.delete()
    return redirect('employee_view')

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import LoanHistory

def approved_transaction(request):
    data = LoanHistory.objects.filter(approve_status='approved')
    total_sum = data.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'approved_transaction.html', {
        'udata': data,
        'total_amount': total_sum
    })


def approve_loan(request, id):
    loan = get_object_or_404(LoanHistory, id=id)

    loan.approve_status = 'approved'
    loan.save()

    return redirect('approved_transaction')


def loan_report_admin(request):
    if request.method == "POST":
        type = request.POST.get('type')
        data = AddLoan.objects.filter(loan_status=type)

        # Handle CSV Download
        if 'download_csv' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="loan_report_{type}.csv"'

            writer = csv.writer(response)
            writer.writerow(
                ['Agent', 'Account No', 'Customer No', 'Amount', 'Interest', 'Issue Date', 'Due Date', 'Loan Status',
                 'Payment Mode'])

            for loan in data:
                writer.writerow([
                    loan.agent,
                    loan.acc_no,
                    loan.cust_no,
                    loan.amount,
                    loan.interest,
                    loan.issue_date,
                    loan.due_date,
                    loan.loan_status,
                    loan.payment_mode,
                ])
            return response

        # Handle Excel Download
        elif 'download_excel' in request.POST:
            wb = Workbook()
            ws = wb.active
            ws.title = "Loan Report"

            headers = ['Agent', 'Account No', 'Customer No', 'Amount', 'Interest', 'Issue Date', 'Due Date',
                       'Loan Status', 'Payment Mode']
            ws.append(headers)

            for loan in data:
                ws.append([
                    loan.agent,
                    loan.acc_no,
                    loan.cust_no,
                    loan.amount,
                    loan.interest,
                    loan.issue_date,
                    loan.due_date,
                    loan.loan_status,
                    loan.payment_mode,
                ])

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="loan_report_{type}.xlsx"'
            wb.save(response)
            return response

        # Normal page render
        return render(request, 'loan_report_admin2.html', {'data': data, 'type': type})

    return render(request, 'loan_report_admin.html')



def employee_edit(request, pk):
    employee = get_object_or_404(AddEmployee, id=pk)

    if request.method == 'POST':
        emp_type = request.POST.get('emp_type')
        emp_name = request.POST.get('emp_name')
        mobile_no = request.POST.get('mobile_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        upload_aadhar = request.FILES.get('upload_aadhar')
        address = request.POST.get('address')

        employee.emp_type = emp_type
        employee.emp_name = emp_name
        employee.mobile_no = mobile_no
        employee.username = username

        # Only update upload_aadhar if a new file is uploaded
        if upload_aadhar:
            employee.upload_aadhar = upload_aadhar

        employee.address = address

        employee.save()
        return redirect('employee_view')

    return render(request, 'employee_edit.html', {'data': [employee]})


def customer_del(request,pk):
    udata = AddCustomer.objects.get(id=pk)
    udata.delete()
    return redirect('customer_view')

def customer_edit(request,pk):
    data=AddCustomer.objects.filter(id=pk).values()
    if request.method =='POST':
        name = request.POST.get('name')
        aadhar_no = request.POST.get('aadhar_no')
        mobile_no = request.POST.get('mobile_no')
        district = request.POST.get('district')
        city = request.POST.get('city')
        pincode =request.POST.get('pincode')
        occupation = request.POST.get('occupation')
        cust_id = request.POST.get('cust_id')
        utype=request.POST.get('utype')
        AddCustomer.objects.filter(id=pk).update(name=name,aadhar_no=aadhar_no,mobile_no=mobile_no,district=district,city=city,pincode=pincode,occupation=occupation,cust_id=cust_id,utype=utype)
        UserLogin.objects.filter(id=pk).update(username=aadhar_no,password=mobile_no)
        return redirect('customer_view')
    return render(request,'customer_edit.html',{'data':data})

def loan_del(request,pk):
    udata = AddLoan.objects.get(id=pk)
    udata.delete()
    return redirect('loan_history_view')

def loan_edit(request,pk):
    data=AddLoan.objects.filter(id=pk).values()
    if request.method=='POST':
        agent = request.POST.get('agent')
        acc_no = request.POST.get('acc_no')
        cust_no = request.POST.get('cust_no')
        amount = request.POST.get('amount')
        interest = request.POST.get('interest')
        issue_date = request.POST.get('issue_date')
        due_date = request.POST.get('due_date')
        loan_status = request.POST.get('loan_status')
        payment_mode = request.POST.get('payment_mode')
        AddLoan.objects.filter(id=pk).update(agent=agent,acc_no=acc_no,cust_no=cust_no,amount=amount,interest=interest,issue_date=issue_date,due_date=due_date,loan_status=loan_status,payment_mode=payment_mode)
        return redirect('loan_view')
    return render(request,'loan_edit.html',{'data':data})


def loan_history_del(request,pk):
    udata = LoanHistory.objects.get(id=pk)
    udata.delete()
    return redirect('loan_history_view')

def loan_history_edit(request,pk):
    data=LoanHistory.objects.filter(id=pk).values()
    if request.method=='POST':
        agent = request.POST.get('agent')
        customer = request.POST.get('customer')
        acc_no = request.POST.get('acc_no')
        amount = request.POST.get('amount')
        deposit_date = request.POST.get('deposit_date')
        particulars = request.POST.get('particulars')
        approve_status = request.POST.get('approve_status')
        LoanHistory.objects.filter(id=pk).update(agent=agent,customer=customer,acc_no=acc_no,amount=amount,deposit_date=deposit_date,particulars=particulars,approve_status=approve_status)
        return redirect('loan_history_view')
    return render(request,'loan_history_edit.html',{'data':data})



def bankTransaction_del(request,pk):
    udata = BankTransaction.objects.get(id=pk)
    udata.delete()
    return redirect('bankTransaction_view')

def bankTransaction_edit(request,pk):
    data=BankTransaction.objects.filter(id=pk).values()
    if request.method=="POST":
        date = request.POST.get('date')
        particular = request.POST.get('particular')
        note = request.POST.get('note')
        deposit = request.POST.get('deposit')
        withdraw = request.POST.get('withdraw')
        BankTransaction.objects.filter(id=pk).update(date=date,particular=particular,note=note,deposit=deposit,withdraw=withdraw)
        return redirect('bankTransaction_view')
    return render(request,'bankTransaction_edit.html',{'data':data})


def loan_view_agent(request):
    agent=request.session['username']
    data=AddLoan.objects.filter(agent=agent).values()
    return render(request,'loan_view_agent.html',{'data':data})




def update_loan_amount(request, acc_no):
    agent = request.session['username']
    data = AddLoan.objects.get(acc_no=acc_no)
    customer = data.cust_no
    loan_amount = data.amount
    today=date.today()

    if request.method == 'POST':
        customer = request.POST.get('customer')
        acc_no = request.POST.get('acc_no')
        amount = request.POST.get('amount')
        deposit_date = request.POST.get('deposit_date')
        particulars = request.POST.get('particulars')
        approve_status = 'Pending'

        # Convert string to date object
        try:
            deposit_date_obj = date.fromisoformat(deposit_date)
        except ValueError:
            return render(request, 'update_loan_amount.html', {
                'error': 'Invalid date format',
                'acc_no': acc_no,
                'customer': customer,
                'loan_amount': loan_amount,
                'today':today
            })

        # Check if collection already exists for today
        already_collected = LoanHistory.objects.filter(
            acc_no=acc_no,
            deposit_date=deposit_date_obj
        ).exists()

        if already_collected:
            return render(request, 'update_loan_amount.html', {
                'success': 'Already added today\'s collection',
                'acc_no': acc_no,
                'customer': customer,
                'loan_amount': loan_amount,
                'today': today
            })

        # Save the new transaction
        LoanHistory.objects.create(
            agent=agent,
            customer=customer,
            acc_no=acc_no,
            amount=amount,
            deposit_date=deposit_date_obj,
            particulars=particulars,
            approve_status=approve_status
        )

        return render(request, 'update_loan_amount.html', {
            'success': 'Added successfully',
            'acc_no': acc_no,
            'customer': customer,
            'loan_amount': loan_amount,
            'today': today
        })

    return render(request, 'update_loan_amount.html', {
        'acc_no': acc_no,
        'customer': customer,
        'loan_amount': loan_amount,
        'today': today
    })

def approved_loan_view(request):
    if 'username' in request.session:
        data = LoanHistory.objects.filter(approve_status__iexact='approved').values()
        return render(request, 'approved_loan_view.html', {'data': data})
    return redirect('login')
def loan_report_due(request):
    if request.method=="POST":
        ddate=request.POST.get('d')
        data=AddLoan.objects.filter(due_date=ddate).values()
        return render(request,'loan_report_due2.html',{'data':data})
    return render(request,'loan_report_due.html')

def datewise_report_admin(request):
    if request.method=="POST":
        ddate=request.POST.get('d')
        data=AddLoan.objects.filter(due_date=ddate).values()
        return render(request,'datewise_report_admin2.html',{'data':data})
    return render(request,'datewise_report_admin.html')



def cust_wise_collection(request):
    data=AddLoan.objects.all()
    return render(request,'cust_wise_collection.html',{'data':data})


def total_collection(request, acc_no):
    loan = AddLoan.objects.get(acc_no=acc_no)

    collections = LoanHistory.objects.filter(
        acc_no=acc_no,
        approve_status='approved'
    )

    paid_amount = collections.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_payable = loan.amount + loan.interest

    remaining_amount = total_payable - paid_amount

    print("Loan Amount =", loan.amount)
    print("Interest =", loan.interest)
    print("Paid Amount =", paid_amount)
    print("Total Payable =", total_payable)
    print("Remaining Amount =", remaining_amount)

    return render(request, 'total_collection.html', {
        'data': collections,
        'paid_amount': paid_amount,
        'loan_amount': loan.amount,
        'interest': loan.interest,
        'total_payable': total_payable,
        'remaining_amount': remaining_amount
    })
def loan_report_open(request):
    data=AddLoan.objects.filter(loan_status='Open')
    return render(request,'loan_report_open.html',{'data':data})

def loan_report_close(request):
    data = AddLoan.objects.filter(loan_status='Close')
    return render(request,'loan_report_close.html',{'data':data})



def loan_history_view_agent(request):
    agent = request.session['username']
    data = LoanHistory.objects.filter(agent=agent).values()
    return render(request, 'loan_history_view_agent.html', {'data': data})






