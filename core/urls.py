from django.urls import path
from django.http import JsonResponse
from core.views import (
    SignupView,
    LoginView,
    FileUploadView,
    GenerateDocView,
    GeneratePDFView,
    DashboardView
)

def home(request):
    return JsonResponse({"message": "Welcome to the API!"})

urlpatterns = [
    path('', home, name='home'),  # Optional: root endpoint to avoid 404 at /
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('generate-doc/', GenerateDocView.as_view(), name='generate-doc'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate-pdf'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
