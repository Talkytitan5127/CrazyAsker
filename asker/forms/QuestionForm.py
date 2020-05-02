from django import forms

from asker.models import Question, Tag

class QuestionForm(forms.Form):

    tags = forms.ModelMultipleChoiceField(
        Tag.objects,
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control'}
        )
    )
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control align-baseline'}
        )
    )


    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)


    def save(self, commit=True):
        text, title = self.cleaned_data['text'], self.cleaned_data['title']
        question = Question(text=text, title=title)
        question.author = self.author
        if commit:
            question.save()
        for tag in self.cleaned_data['tags']:
            tag.questions.add(question)

        return question

    class Meta:
        model = Question
        fields = ('title', 'text')
