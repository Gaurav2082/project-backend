from django.db import models

class Documentation(models.Model):
    file_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    code = models.TextField()
    generated_doc = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'Backend'  # Ensure Django recognizes the app

    def __str__(self):
        return self.file_name
