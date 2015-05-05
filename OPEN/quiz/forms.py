from django.forms import ModelForm, Textarea, TextInput

from OPEN.quiz.models import Quiz


class AddQuizForm(ModelForm):
    """
    Add new Quiz
    """
    class Meta:
        model = Quiz
        exclude = ['date_deleted', 'course', 'user']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            'description': Textarea(attrs={'placeholder': 'Quiz Description', 'rows': 4}),
        }