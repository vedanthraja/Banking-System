from django.shortcuts import render, get_object_or_404
from .models import account, trans_info
from django.utils import timezone
from .forms import LoginForm, TransactionForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        acct_no = request.POST.get('acct_no')
        pin = request.POST.get('pin')
        user = account.objects.filter(acct_no=acct_no, pin=pin).first()
        if user is not None:
            return redirect('acct_details', acct_no=acct_no)
        else:
            messages.info(request, '* Account No.(12 digit) or Pin(6 digit) is incorrect')
            return redirect('login_page')
    form = LoginForm()
    return render(request, 'bank/login_page.html', {'form':form})

def acct_details(request, acct_no):
    if request.method == 'POST':
        amount  = int(request.POST.get('amount'))
        cred_acct_num = request.POST.get('cred_acct_num')
        cred_acct = account.objects.filter(acct_no=cred_acct_num).first()
        deb_acct = account.objects.get(acct_no=acct_no)
        if cred_acct is not None:
            if cred_acct.acct_no == deb_acct.acct_no:
                messages.info(request, '* Invalid account number')
            elif amount < 0:
                messages.info(request, '* Invalid ammount')
            elif deb_acct.balance >= amount:
                deb_acct.balance = deb_acct.balance - amount
                cred_acct.balance = cred_acct.balance + amount
                deb_acct.save()
                cred_acct.save()
                trans_info.objects.create(trans_date = timezone.now(),amount = amount, cred_acct_num = cred_acct, deb_acct_num = deb_acct)
                messages.info(request, '* Transaction successful')
            else:
                messages.info(request, '* Insufficient Balance!')
        else:
            messages.info(request, '* Account does not exist')
        
        return redirect('acct_details', acct_no=deb_acct.acct_no)
    
    form = TransactionForm()
    acct = account.objects.get(acct_no=acct_no)
    return render(request, 'bank/acct_details.html', {'acct':acct, 'transForm':form})

def acct_statement(request, acct_no):
    user_acct = account.objects.get(acct_no=acct_no)
    q2 = trans_info.objects.filter(deb_acct_num = user_acct)
    q3 = trans_info.objects.filter(cred_acct_num = user_acct)
    q4 = (q2.union(q3))
    q1 = q4.order_by('trans_date')
    return render(request,'bank/acct_statement.html',{'q1':q1,'user_acct':user_acct})
