from django.shortcuts import render
from django_ecom.utils import get_session
from orders.utils import submit_payment, get_total

# Create your views here.


def payment_view(request):
    session = get_session(request)

    if request.method == 'POST':
        submission = submit_payment(request, session)
        if submission:
            return render(request, 'payments/payment_successful.html')
    
    context = {
        "total": get_total(session)
    }
    return render(request, 'payments/checkout.html', context)
