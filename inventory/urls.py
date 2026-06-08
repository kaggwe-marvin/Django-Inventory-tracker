from django.urls import path
from inventory.views import InventoryCSVReportView

app_name = "inventory"

urlpatterns = [
    path("reports/csv/", InventoryCSVReportView.as_view(), name="csv-report"),
]
