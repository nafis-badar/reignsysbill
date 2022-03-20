from optparse import check_choice
from re import T
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
from invoice.middlewares import get_clear_array,get_clear_object,number_to_word,format_float,datetime_fomat
import inflect
# import render_to_pdf from util.py
from .utils import render_to_pdf
from .models import UserInput
import math
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='loginuser')
def index(request):
    return render(request, 'index.html')

@login_required(redirect_field_name='login')
@csrf_exempt
def user_input(request):
    if request.method == "GET":
        return render(request, 'input.html')
    if request.method == "POST":
        data = request.POST
        customer_details = data.get("customer_details")
        request.session['customer_details'] = customer_details
        customer_address = data.get("customer_address")
        request.session['customer_address'] = customer_address
        customer_gst = data.get("customer_gst")
        request.session['customer_gst'] = customer_gst
        customer_pan = data.get("customer_pan")
        request.session['customer_pan'] = customer_pan
        customer_po = data.get("customer_po")
        request.session['customer_po'] = customer_po
        invoice_date = data.get("invoice_date")
        request.session['invoice_date'] = invoice_date
        candidate_name = data.get("candidate_name")
        request.session['candidate_name'] = candidate_name
        candidate_designation = data.get("candidate_designation")
        request.session['candidate_designation'] = candidate_designation
        joining_date = data.get("joining_date")
        request.session['joining_date'] = joining_date
        due_date = data.get("due_date")
        request.session['due_date'] = due_date
        candidate_ctc = data.get("candidate_ctc")
        request.session['candidate_ctc'] = candidate_ctc
        ctc_percent = data.get("ctc_percent")
        request.session['ctc_percent'] = ctc_percent
        igst_percent = data.get("igst_percent")
        request.session['igst_percent'] = igst_percent
        sac_code = data.get("sac_code")
        request.session['sac_code'] = sac_code
        check_user=UserInput.objects.all() 
        invoice_number = 0
        if check_user is not None and len(check_user)>0:
            max_invoice = UserInput.objects.latest()
            max_invoice_print = max_invoice.invoice_num
            invoice_number = int(max_invoice_print)+1
        else:
            invoice_number=1000
        request.session['invoice_number'] = invoice_number
        amnt_float = int(candidate_ctc) * int(ctc_percent) / 100
        amnt= format_float(amnt_float)
        request.session['amnt'] = amnt
        igst_amnt_float = amnt_float * int(igst_percent) / 100
        igst_amnt = format_float(igst_amnt_float)
        request.session['igst_amnt'] = igst_amnt
        total_amnt_float = amnt_float + igst_amnt_float
        total_amnt=format_float(total_amnt_float)
        request.session['total_amnt'] = total_amnt
        total_amt_word = number_to_word(total_amnt)
        request.session['total_amt_word'] = total_amt_word
        try:
            create_input = UserInput.objects.create(
                customer_details=customer_details,
                customer_address=customer_address,
                customer_pan=customer_pan,
                customer_gst=customer_gst,
                customer_po=customer_po,
                invoice_date=invoice_date,
                invoice_num=invoice_number,
                candidate_name=candidate_name,
                candidate_designation=candidate_designation,
                candidate_ctc=candidate_ctc,
                joining_date=joining_date,
                due_date=due_date,
                ctc_percent=ctc_percent,
                sac_code=sac_code,
                amnt=amnt,
                igst_percent=igst_percent,
                igst_amnt=igst_amnt,
                total_amt=total_amnt,
                total_amt_word=total_amt_word
            )
        except ValueError:
            return HttpResponse("this is failed")
        

        return redirect('pdf')

    # importing get_template from loader

@login_required
# Creating our view, it is a class based view
# class GeneratePdf(View):
def get_pdf(request, *args, **kwargs):
    customer_details = request.session.get('customer_details')
    customer_address = request.session.get('customer_address')
    customer_gst = request.session.get('customer_gst')
    customer_pan = request.session.get('customer_pan')
    customer_po = request.session.get('customer_po')
    invoice_date= request.session.get('invoice_date')
    invoice_date_format =datetime_fomat(invoice_date)
    candidate_name = request.session.get('candidate_name')
    candidate_designation = request.session.get('candidate_designation')
    joining_date = request.session.get('joining_date')
    joining_date_format = datetime_fomat(joining_date)
    due_date = request.session.get('due_date')
    due_date_format = datetime_fomat(due_date)
    ctc_percent = request.session.get('ctc_percent')
    igst_percent = request.session.get('igst_percent')
    sac_code = request.session['sac_code']
    invoice_num = request.session['invoice_number']
    amnt = request.session['amnt']
    igst_amnt = request.session['igst_amnt']
    total_amnt = request.session['total_amnt']
    total_amt_word = request.session['total_amt_word']

    pdf = render_to_pdf('invoice.html', {'customer_details': customer_details,'customer_address': customer_address,
                                            'customer_gst': customer_gst,
                                            'customer_pan': customer_pan,
                                            'customer_po': customer_po,
                                            'invoice_date': invoice_date_format,'invoice_num':invoice_num,
                                            'candidate_name': candidate_name, 'due_date': due_date_format,
                                            'candidate_designation': candidate_designation,
                                            'joining_date': joining_date_format, 'ctc_percent': ctc_percent,
                                            'sac_code': sac_code, 'amnt': amnt, 'igst_amnt': igst_amnt,
                                            'igst_percent':igst_percent,'total_amnt': total_amnt, 'total_amt_word': total_amt_word})


    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
@csrf_exempt
def invoice_list(request):
    fetch_invoice = UserInput.objects.order_by()
    cleared_invoice = get_clear_array(fetch_invoice)
    return render(request,'user_list.html',{'data':cleared_invoice})


@login_required
@csrf_exempt
def get_invoice_detail(request,id):
    invoice_detail = UserInput.objects.get(
        invoice_num=id
    )
    clear_invoice_detail = get_clear_object(invoice_detail)
    pdf = render_to_pdf('invoice.html', {
                                            'customer_details':clear_invoice_detail['customer_details'],
                                            'customer_address':clear_invoice_detail['customer_address'],
                                            'customer_gst': clear_invoice_detail['customer_gst'],
                                            'customer_pan': clear_invoice_detail['customer_pan'],
                                            'customer_po': clear_invoice_detail['customer_po'],
                                            'invoice_date': datetime_fomat(clear_invoice_detail['invoice_date']),'invoice_num':clear_invoice_detail['invoice_num'],
                                            'candidate_name': clear_invoice_detail['candidate_name'],
                                            'candidate_designation': clear_invoice_detail['candidate_designation'],
                                            'joining_date': datetime_fomat(clear_invoice_detail['joining_date']),
                                            'due_date':datetime_fomat(clear_invoice_detail['due_date']),
                                            'ctc_percent': clear_invoice_detail['ctc_percent'],
                                            'sac_code': clear_invoice_detail['sac_code'], 'amnt': clear_invoice_detail['amnt'],
                                            'igst_percent': clear_invoice_detail['igst_percent'], 'igst_amnt': clear_invoice_detail['igst_amnt'],
                                            'total_amnt': clear_invoice_detail['total_amt'], 'total_amt_word': clear_invoice_detail['total_amt_word']})
    return HttpResponse(pdf, content_type='application/pdf')

def loginuser(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        user=authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'login.html', {'error':'This Username or Password incorrect'})
        else:
            login(request,user)
            return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('loginuser')
