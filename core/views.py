from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
   def post(self, request, *args, **kwargs):
      response = super().post(request, *args, **kwargs)
      # Customize the response to return only the access token
      response.data = {
         'access': response.data['access'],
      }
      return response
