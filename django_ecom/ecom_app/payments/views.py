from django.shortcuts import render
from ..utils import get_session
from ..orders.utils import submit_payment, get_total


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
