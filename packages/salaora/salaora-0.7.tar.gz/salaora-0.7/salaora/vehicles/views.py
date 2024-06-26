from django.shortcuts import render
from django.shortcuts import redirect

from vehicles.models import Vehicle, populate_vehicles_from_csv_string
from vehicles.forms import BulkCreateVehiclesForm

def vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    context = {
        "vehicle": vehicle
    }
    return render(request, "vehicle.html", context)


def vehicles(request):
    vehicles = Vehicle.objects.all().order_by("-price")

    if vehicles:
        context = {
            "vehicles": vehicles
        }

        return render(request, "vehicles.html", context)

    else:
        return render(request, "bulk_create_vehicles.html", {})

def bulk_create_vehicles(request):
    if request.method == "POST":
        form = BulkCreateVehiclesForm(request.POST)
        csv_data = form["csv_data"].value()
        populate_vehicles_from_csv_string(csv_data)
        return(redirect("vehicles"))

    return render(request, "bulk_create_vehicles.html", {})
