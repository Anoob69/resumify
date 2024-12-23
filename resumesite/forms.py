from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resume


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ContactForm(forms.ModelForm):
    # Adding custom fields for start and end dates with appropriate attributes
    experience_1_start = forms.DateField(
        label="Experience 1 Start Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=True
    )
    experience_1_end = forms.DateField(
        label="Experience 1 End Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=True
    )
    experience_2_start = forms.DateField(
        label="Experience 2 Start Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )
    experience_2_end = forms.DateField(
        label="Experience 2 End Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )
    education_1_start = forms.DateField(
        label="Education 1 Start Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=True
    )
    education_1_end = forms.DateField(
        label="Education 1 End Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=True
    )
    education_2_start = forms.DateField(
        label="Education 2 Start Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )
    education_2_end = forms.DateField(
        label="Education 2 End Date",
        widget=forms.DateInput(attrs={"placeholder": "dd-mm-yyyy"}),
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],
        required=False
    )

    class Meta:
        model = Resume
        fields = [
            'name', 'email', 'mobile', 'address',
            'skills_1', 'skills_2', 'skills_3', 'skills_4',
            'experience_1_title', 'experience_1_desc',
            'experience_2_title', 'experience_2_desc',
            'education_1', 'education1_score',
            'education_2', 'education2_score'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'container justify-content-center'
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-5 mb-10'),
                Column('email', css_class='form-group col-md-7 mb-10'),
                css_class='form-row center'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-5 mb-10'),
                Column('address', css_class='form-group col-md-7 mb-10'),
                css_class='form-row center'
            ),
            Row(
                Column('skills_1', css_class='form-group col-md-6 mb-10'),
                Column('skills_2', css_class='form-group col-md-6 mb-10'),
                css_class='form-row center'
            ),
            Row(
                Column('skills_3', css_class='form-group col-md-6 mb-10'),
                Column('skills_4', css_class='form-group col-md-6 mb-10'),
                css_class='form-row center'
            ),
            Row(
                Column('experience_1_title', css_class='form-group col-md-7 mb-10'),
                Column('experience_1_start', css_class='form-group col-md-3 mb-10'),
                Column('experience_1_end', css_class='form-group col-md-3 mb-10'),
                css_class='form-row center'
            ),
            'experience_1_desc',
            Row(
                Column('experience_2_title', css_class='form-group col-md-7 mb-10'),
                Column('experience_2_start', css_class='form-group col-md-3 mb-10'),
                Column('experience_2_end', css_class='form-group col-md-3 mb-10'),
                css_class='form-row center'
            ),
            'experience_2_desc',
            Row(
                Column('education_1', css_class='form-group col-md-12 mb-10'),
                Column('education_1_start', css_class='form-group col-md-3 mb-10'),
                Column('education_1_end', css_class='form-group col-md-3 mb-10'),
                Column('education1_score', css_class='form-group col-md-3 mb-10'),
                css_class='form-row center'
            ),
            Row(
                Column('education_2', css_class='form-group col-md-12 mb-10'),
                Column('education_2_start', css_class='form-group col-md-3 mb-10'),
                Column('education_2_end', css_class='form-group col-md-3 mb-10'),
                Column('education2_score', css_class='form-group col-md-3 mb-10'),
                css_class='form-row center'
            ),
            Submit('submit', 'Submit', css_class="btn-success")
        )

    # Custom validation for mobile number
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) != 10 or not mobile.isdigit():
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mobile

    # Custom validation for scores
    def clean_education1_score(self):
        score = self.cleaned_data['education1_score']
        if not isinstance(score, int) or score < 1 or score > 100:
            raise forms.ValidationError("Score must be between 1 and 100.")
        return score

    def clean_education2_score(self):
        score = self.cleaned_data.get('education2_score')
        if score is not None and (not isinstance(score, int) or score < 1 or score > 100):
            raise forms.ValidationError("Score must be between 1 and 100.")
        return score

    # Custom validation for start and end dates
    def clean(self):
        cleaned_data = super().clean()
        experience_1_start = cleaned_data.get('experience_1_start')
        experience_1_end = cleaned_data.get('experience_1_end')

        if experience_1_start and experience_1_end and experience_1_start > experience_1_end:
            self.add_error('experience_1_end', "End date must be after start date for Experience 1.")

        experience_2_start = cleaned_data.get('experience_2_start')
        experience_2_end = cleaned_data.get('experience_2_end')

        if experience_2_start and experience_2_end and experience_2_start > experience_2_end:
            self.add_error('experience_2_end', "End date must be after start date for Experience 2.")

        education_1_start = cleaned_data.get('education_1_start')
        education_1_end = cleaned_data.get('education_1_end')

        if education_1_start and education_1_end and education_1_start > education_1_end:
            self.add_error('education_1_end', "End date must be after start date for Education 1.")

        education_2_start = cleaned_data.get('education_2_start')
        education_2_end = cleaned_data.get('education_2_end')

        if education_2_start and education_2_end and education_2_start > education_2_end:
            self.add_error('education_2_end', "End date must be after start date for Education 2.")

        return cleaned_data
