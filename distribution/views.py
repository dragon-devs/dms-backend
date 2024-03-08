from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import DistributionProfile, EmployeesProfile, CompanyProfile, ProductForm
from .serializers import DistributionProfileSerializer, EmployeesProfileSerializer, CompanyProfileSerializer, \
   ProductFormSerializer


class DistributionProfileViewSet(ModelViewSet):
   queryset = DistributionProfile.objects.all()
   serializer_class = DistributionProfileSerializer
   permission_classes = [IsAdminUser]

   # def get_permissions(self):
   #     if self.request.method == "GET":
   #         return [AllowAny()]
   #     return [IsAuthenticated()]

   @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
   def me(self, request):
      (_, created) = DistributionProfile.objects.get_or_create(user_id=request.user.id)

      if created:
         username = request.user.username.capitalize()
         _.name = username + " Distribution"
         _.save()

      if request.method == "GET":
         serializer = DistributionProfileSerializer(_)
         return Response(serializer.data)
      elif request.method == "PUT":
         serializer = DistributionProfileSerializer(_, data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data)

   @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
   def employees(self, request):
      distribution_profile = DistributionProfile.objects.get(user=request.user)

      employees = EmployeesProfile.objects.filter(distribution=distribution_profile)

      serializer = EmployeesProfileSerializer(employees, many=True)
      return Response(serializer.data)


class EmployeesProfileViewSet(DistributionProfileViewSet):
   serializer_class = EmployeesProfileSerializer
   permission_classes = [IsAuthenticated]

   def perform_create(self, serializer):
      serializer.save(distribution=self.get_user_dis_profile_id())

   def get_queryset(self):
      return EmployeesProfile.objects.filter(distribution=self.get_user_dis_profile_id())

   def get_user_dis_profile_id(self):
      return get_object_or_404(DistributionProfile, user=self.request.user)


class CompanyProfileViewSet(ModelViewSet):
   serializer_class = CompanyProfileSerializer
   permission_classes = [IsAuthenticated]

   def perform_create(self, serializer):
      serializer.save(distribution=self.get_user_dis_profile_id())

   def get_queryset(self):
      return CompanyProfile.objects.filter(distribution=self.get_user_dis_profile_id())

   def get_user_dis_profile_id(self):
      return get_object_or_404(DistributionProfile, user=self.request.user)

   @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
   def for_user(self, request):
      distribution = get_object_or_404(DistributionProfile, user=request.user)

      companies = CompanyProfile.objects.filter(distribution=distribution)
      serializer = CompanyProfileSerializer(companies, many=True)

      return Response(serializer.data)


class ProductFormViewSet(ModelViewSet):
   serializer_class = ProductFormSerializer
   permission_classes = [IsAuthenticated]

   def perform_create(self, serializer):
      company = get_object_or_404(CompanyProfile, pk=self.kwargs['company_pk'])

      existing_product = ProductForm.objects.filter(company=company, name=serializer.validated_data['name']).first()

      if existing_product:
         serializer.errors['name'] = ['A product with the same company and name already exists.']
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      serializer.save(company=company)

   def get_queryset(self):
      company = CompanyProfile.objects.filter(distribution=self.get_user_dis_profile_id())
      dis_company = get_object_or_404(company, pk=self.kwargs['company_pk'])

      return ProductForm.objects.filter(company=dis_company)

   def get_user_dis_profile_id(self):
      return get_object_or_404(DistributionProfile, user=self.request.user)
