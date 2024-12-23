from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from .forms import ContactForm, SignupForm
from .models import Resume
from django.contrib import messages
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html', {})

def landing_page(request):
    return render(request, 'landing_page.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard_view(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'resumes': resumes})

@login_required
def info(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    resume = Resume.objects.create(
                        user=request.user,
                        name=form.cleaned_data['name'],
                        email=form.cleaned_data['email'],
                        mobile=form.cleaned_data['mobile'],
                        address=form.cleaned_data['address'],
                        skills_1=form.cleaned_data['skills_1'],
                        skills_2=form.cleaned_data['skills_2'],
                        skills_3=form.cleaned_data['skills_3'],
                        skills_4=form.cleaned_data['skills_4'],
                        experience_1_title=form.cleaned_data['experience_1_title'],
                        experience_1_start=form.cleaned_data['experience_1_start'],
                        experience_1_end=form.cleaned_data['experience_1_end'],
                        experience_1_desc=form.cleaned_data['experience_1_desc'],
                        experience_2_title=form.cleaned_data.get('experience_2_title', ''),
                        experience_2_start=form.cleaned_data.get('experience_2_start', None),
                        experience_2_end=form.cleaned_data.get('experience_2_end', None),
                        experience_2_desc=form.cleaned_data.get('experience_2_desc', ''),
                        education_1=form.cleaned_data['education_1'],
                        education_1_start=form.cleaned_data['education_1_start'],
                        education_1_end=form.cleaned_data['education_1_end'],
                        education1_score=form.cleaned_data['education1_score'],
                        education_2=form.cleaned_data.get('education_2', ''),
                        education_2_start=form.cleaned_data.get('education_2_start', None),
                        education_2_end=form.cleaned_data.get('education_2_end', None),
                        education2_score=form.cleaned_data.get('education2_score', None)
                    )

                    # Generate PDF
                    template = 'resume_template.html'
                    html = render_to_string(template, {'resume': resume})
                    buffer = BytesIO()
                    pisa_status = pisa.CreatePDF(html, dest=buffer)
                    pdf_content = buffer.getvalue()
                    buffer.close()

                    if pisa_status.err:
                        messages.error(request, "Failed to generate the PDF. Please try again.")
                        resume.delete()
                        return redirect('info')

                    resume.pdf_file.save(f"{resume.name}_resume.pdf", ContentFile(pdf_content))

                messages.success(request, "Your resume was successfully created!")
                return redirect('dashboard')

            except Exception as e:
                logger.exception("An error occurred while processing the resume: %s", e)
                messages.error(request, "An unexpected error occurred. Please try again.")
    return render(request, 'info.html', {'form': form})

@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    form = ContactForm(instance=resume)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=resume)
        if form.is_valid():
            try:
                with transaction.atomic():
                    updated_resume = form.save()

                    # Regenerate PDF
                    template = 'resume_template.html'
                    html = render_to_string(template, {'resume': updated_resume})
                    buffer = BytesIO()
                    pisa_status = pisa.CreatePDF(html, dest=buffer)
                    pdf_content = buffer.getvalue()
                    buffer.close()

                    if pisa_status.err:
                        logger.error("PDF generation failed during editing for resume ID: %s", resume.id)
                        messages.error(request, "Failed to regenerate the PDF. Please try again.")
                    else:
                        resume.pdf_file.save(f"{resume.name}_resume_updated.pdf", ContentFile(pdf_content))
                        messages.success(request, "Resume updated and PDF regenerated successfully!")
                return redirect('dashboard')

            except Exception as e:
                logger.exception("An error occurred while editing the resume: %s", e)
                messages.error(request, "An unexpected error occurred. Please try again.")
    return render(request, 'info.html', {'form': form})

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.delete()
    messages.success(request, "Resume deleted successfully.")
    return redirect('dashboard')

@login_required
def download_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        if not resume.pdf_file or not resume.pdf_file.name:
            logger.error("PDF file not found for resume ID: %s", resume_id)
            raise Http404("Resume PDF not found.")
        return FileResponse(resume.pdf_file.open('rb'), content_type='application/pdf', as_attachment=True, filename=f"{resume.name}_resume.pdf")
    except Resume.DoesNotExist:
        logger.error("Resume not found for ID: %s", resume_id)
        raise Http404("Resume not found.")
