from crispy_forms.helper import FormHelper
from django import forms

from .models import Submission, Problem, SubProblem


def handle_uploaded_file(f):
    query_string = str('')
    for chunk in f.chunks():
        query_string += str(chunk)
    return query_string


class ProblemEditModeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProblemEditModeForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        self.fields.update({
            'init_queries_file': forms.FileField(required=False)
        })
        self.fields['text'].widget.attrs['class'] = 'text'
        self.fields['number_of_subproblems'].required = False
        self.fields['init_queries'].widget.attrs['class'] = 'text'
        self.fields['init_queries_status'].required = False
        self.fields['init_queries_error_details'].widget.attrs['readonly'] = True
        self.fields['init_queries_error_details'].widget.attrs['class'] = 'text'
        self.fields['init_queries_error_details'].required = False

    class Meta:
        model = Problem
        exclude = ['problem_setter_id']


class SubProblemEditModeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubProblemEditModeForm, self).__init__(*args, **kwargs)

        # self.fields.update({
        #    'result_output': forms.CharField(required=False, widget=forms.Textarea())
        # })

        self.fields['title'].required = False
        self.fields['text'].widget.attrs['class'] = 'text'
        self.fields['text'].required = False
        self.fields['dump_queries'].widget.attrs['class'] = 'text'
        self.fields['index'].required = False
        self.fields['dump_queries'].required = False
        self.fields['dump_queries_status'].required = False
        self.fields['dump_queries_error_details'].widget.attrs['class'] = 'text'
        self.fields['dump_queries_error_details'].required = False
        self.fields['final_query'].widget.attrs['class'] = 'text'
        self.fields['final_query_status'].required = False
        self.fields['final_query_error_details'].widget.attrs['class'] = 'text'
        self.fields['final_query_error_details'].widget.attrs['readonly'] = True
        self.fields['final_query_error_details'].required = False
        self.fields['result'].widget.attrs['class'] = 'text'
        self.fields['result'].widget.attrs['readonly'] = True
        self.fields['result'].required = False

    class Meta:
        model = SubProblem
        exclude = ['problem']


class ProblemDisplayModeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProblemDisplayModeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['title'].widget.attrs['readonly'] = True
        self.fields['text'].widget.attrs['readonly'] = True
        self.fields['text'].label = False

    class Meta:
        model = Problem
        fields = ['title', 'text']


class SubProblemDisplayModeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubProblemDisplayModeForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['text'].widget.attrs['class'] = 'text'
        self.fields['text'].required = False
        self.fields['index'].required = False
        self.fields['dump_queries'].required = False
        self.fields['dump_queries_status'].required = False
        self.fields['dump_queries_error_details'].required = False
        self.fields['final_query_status'].required = False
        self.fields['final_query_error_details'].required = False
        self.fields['result'].required = False

    class Meta:
        model = SubProblem
        fields = ['title', 'text']


class SubmissionForm(forms.ModelForm):
    submission_file = forms.FileField()

    class Meta:
        model = Submission
        fields = '__all__'
