from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import DistributionProfileViewSet, EmployeesProfileViewSet, CompanyProfileViewSet, ProductFormViewSet

router = DefaultRouter()
router.register(r'distribution', DistributionProfileViewSet, basename='distribution-profile')
router.register(r'companies', CompanyProfileViewSet, basename="companies")

distribution_router = NestedDefaultRouter(router, r'distribution', lookup='distribution')
distribution_router.register(r'employees', EmployeesProfileViewSet, basename="employees-profile")
distribution_router.register(r'companies', CompanyProfileViewSet, basename="companies-profile")

company_router = NestedDefaultRouter(distribution_router, r'companies', lookup='company')
company_router.register(r'products', ProductFormViewSet, basename='products')

urlpatterns = [
    path('distribution/', RedirectView.as_view(url='/distribution/me/')),
    path('', include(router.urls)),
    path('', include(distribution_router.urls)),
    path('', include(company_router.urls)),
]
