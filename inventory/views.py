import csv
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from typing import Any, Generator
from django.http import StreamingHttpResponse, HttpRequest
from django.views import View
from django.views.generic import TemplateView
from bookmarks.models import Bookmark
from inventory.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Echo:
    def write(self, value: str) -> str:
        return value


class InventoryCSVReportView(View):
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> StreamingHttpResponse:
        products = Product.objects.all().iterator(chunk_size=500)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        def generate_rows() -> Generator[str, None, None]:
            yield writer.writerow(
                ["Product Name", "SKU Code", "Current Stock", "Threshold Limit"]
            )
            for product in products:
                yield writer.writerow(
                    [
                        product.name,
                        product.sku,
                        product.stock,
                        product.low_stock_threshold,
                    ]
                )

        response = StreamingHttpResponse(generate_rows(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="inventory_metrics.csv"'
        return response


class UnifiedDashboardView(TemplateView):
    template_name = "dashboard.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        # Role-Based Authorization Guard Component
        if not request.session.get("is_authenticated_operator"):
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # 1. Handle Bookmarks (Static limit)
        context["bookmarks"] = Bookmark.objects.prefetch_related("tags")[:5]

        # 2. Handle Inventory Filter (Option A) - Swapped ordering() for order_by()
        product_list = Product.objects.all().order_by("sku")
        sku_filter = self.request.GET.get("sku", "").strip()
        if sku_filter:
            product_list = product_list.filter(sku__icontains=sku_filter)

        # 3. Handle Inventory Pagination (Option B)
        page_number = self.request.GET.get("page", "1")
        paginator = Paginator(product_list, 5)  # Show 5 records maximum per view window
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["sku_filter"] = sku_filter
        return context


class SystemLoginView(FormView):  # type: ignore[type-arg]
    template_name = "login.html"
    success_url = reverse_lazy("root-dashboard")

    def get_form(self, form_class: Any = None) -> Any:
        # Generate a lightweight ad-hoc authentication form dynamically
        from django import forms

        class LoginForm(forms.Form):
            username = forms.CharField(
                widget=forms.TextInput(attrs={"placeholder": "Operator Username"})
            )
            password = forms.CharField(
                widget=forms.PasswordInput(attrs={"placeholder": "Security Key"})
            )

        return LoginForm(**self.get_form_kwargs())

    def form_valid(self, form: Any) -> Any:
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # Fast verification check using memory configurations
        if username == getattr(settings, "SUPER_USER", "admin") and password == getattr(
            settings, "SUPER_PASS", "secret123"
        ):
            self.request.session["is_authenticated_operator"] = True
            messages.success(self.request, "Access granted. Session initialized.")
            return super().form_valid(form)

        messages.error(self.request, "Access Denied: Invalid Operator Credentials.")
        return self.form_invalid(form)


class SystemLogoutView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        # Flush session state cookies cleanly
        request.session.flush()
        return redirect("login")
