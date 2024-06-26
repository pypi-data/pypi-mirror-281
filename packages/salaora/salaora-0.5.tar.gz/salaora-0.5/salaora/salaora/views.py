from datetime import datetime

from django.shortcuts import render
from django.shortcuts import redirect

from django.db.models import Q

from reservations.models import Reservation
from vehicles.models import Vehicle

def index(request):
    today_dt = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    now_dt = datetime.now()
    q1 = Q(return_dt__date=today_dt)
    q2 = Q(return_dt__gt=now_dt)
    today_pending_returns = Reservation.objects.filter(q1 & q2).order_by("return_dt")
    context = {"today_pending_returns": today_pending_returns}
    return render(request, "index.html", context)
