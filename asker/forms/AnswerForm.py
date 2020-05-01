from django import forms

from asker.models import Answer

class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control mb-3'}
        )
    )

    def __init__(self, author, question, *args, **kwargs):
        self.author = author
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = Answer(text=self.cleaned_data['text'])
        answer.author = self.author
        answer.question = self.question
        if commit:
            answer.save()

        return answer
