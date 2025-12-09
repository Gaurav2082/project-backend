from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from Backend.utils import detect_language, generate_documentation
from core.models import Documentation

import json
import logging

logger = logging.getLogger(__name__)

# ------------------- File Upload View -------------------
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

            file_name = uploaded_file.name
            code_content = uploaded_file.read().decode("utf-8")
            language = detect_language(code_content)
            documentation = generate_documentation(code_content)

            doc = Documentation.objects.create(
                file_name=file_name,
                language=language,
                code=code_content,
                generated_doc=documentation
            )

            return Response({
                "message": "File uploaded and documented.",
                "documentation": documentation,
                "file_name": doc.file_name,
                "language": doc.language,
                "uploaded_at": doc.uploaded_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- Generate Docs -------------------
class GenerateDocView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            code_snippet = data.get("codeSnippet", "")
            if not code_snippet:
                return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

            documentation = generate_documentation(code_snippet)
            return Response({"documentation": documentation})

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- Generate PDF -------------------
class GeneratePDFView(APIView):
    def post(self, request):
        try:
            documentation = request.data.get("documentation", "")
            if not documentation:
                return Response({"error": "No documentation provided"}, status=status.HTTP_400_BAD_REQUEST)

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, 750, "Generated Documentation")

            y_position = 730
            line_height = 14
            for line in documentation.split("\n"):
                pdf.drawString(100, y_position, line[:90])
                y_position -= line_height
                if y_position < 50:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 12)
                    y_position = 750

            pdf.save()
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="documentation.pdf"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- Signup -------------------
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class SignupView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=email, email=email, password=password, first_name=name)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# ------------------- Login (OTP removed) -------------------
class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate

        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful"
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ------------------- Dashboard -------------------
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "message": f"Welcome {user.username}!",
            "email": user.email
        })
