from django.db import models


class UserLogin(models.Model):
    username = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=100,null=True)
    utype = models.CharField(max_length=100,null=True)


class AddEmployee(models.Model):
    emp_type = models.CharField(max_length=100,null=True)
    emp_name = models.CharField(max_length=100,null=True)
    mobile_no = models.BigIntegerField()
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100,null=True)
    upload_aadhar = models.ImageField(upload_to='documents/')
    address = models.CharField(max_length=100, null=True)

class AddCustomer(models.Model):
    name = models.CharField(max_length=100, null=True)
    aadhar_no = models.BigIntegerField()
    mobile_no = models.BigIntegerField()
    district = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pincode = models.BigIntegerField(null=True)
    occupation = models.CharField(max_length=100, null=True)
    cust_id = models.CharField(max_length=100, null=True)
    utype = models.CharField(max_length=100, null=True)

class AddLoan(models.Model):
    agent = models.CharField(max_length=100, null=True)
    acc_no = models.CharField(max_length=100,null=True)
    cust_no = models.CharField(max_length=100, null=True)
    amount = models.BigIntegerField(null=True)
    interest = models.IntegerField(null=True)
    issue_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    loan_status = models.CharField(max_length=100, null=True)
    payment_mode = models.CharField(max_length=100, null=True)

class LoanHistory(models.Model):
    agent = models.CharField(max_length=100, null=True)
    customer = models.CharField(max_length=100, null=True)
    acc_no = models.CharField(max_length=100, null=True)
    amount = models.IntegerField(null=True)
    deposit_date = models.DateField(null=True)
    particulars = models.CharField(max_length=100,null=True)
    approve_status = models.CharField(max_length=100, null=True)

class BankTransaction(models.Model):
    date = models.DateField(null=True)
    particular = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=100, null=True)
    deposit = models.IntegerField(null=True,blank=True)
    withdraw = models.IntegerField(null=True,blank=True)

class OtpCode(models.Model):
    otp_code=models.IntegerField(null=True)
    status=models.CharField(max_length=20,null=True,blank=True)

class CapitalInterest(models.Model):
    amount=models.IntegerField(null=True)
    cdate=models.DateField(null=True,blank=True)

