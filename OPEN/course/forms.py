from django.forms import CharField, FileField, Form, ValidationError
from OPEN.course.models import Forum


class AddForumForm(Form):
    """
    Add new Forum
    """
    title = CharField(max_length=100)
    uploads = FileField(required = True)

    def clean_uploads(self):
        uploads = self.cleaned_data['uploads']
        ext = uploads.name.split('.')[-1]
        if ext == 'pdf' or ext == 'webm':
            return uploads
        else:
            raise ValidationError("Not a valid upload file")