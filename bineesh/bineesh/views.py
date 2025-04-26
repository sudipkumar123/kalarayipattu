from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
def Instructors(request):
    return render(request, 'Instructors.html')

def Schedule(request):
    return render(request, 'Schedule.html')
#def enroll(request):
 #   return render(request, 'enroll.html')
def enroll(request):
    open_modal = True
    form_submitted = False

    if request.method == "POST":
        try:
            # Gather general info
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            name = f"{first_name} {last_name}"
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            program = request.POST.get('program')
            schedule = request.POST.get('schedule')
            experience = request.POST.get('experience')

            # Optional yoga teacher section
            yoga_experience = request.POST.get('yoga_experience')
            yoga_certification = request.POST.get('yoga_certification')
            teach_yoga = 'Yes' if request.POST.get('teach_yoga') else 'No'

            # Health info
            health_issues = 'Yes' if request.POST.get('health_issues') else 'No'

            # Uploaded file
            payment_receipt = request.FILES.get('payment_receipt')

            # Build email body
            body = f"""
📥 New Enrollment Submission:

👤 Name: {name}
📧 Email: {email}
📱 Phone: {phone}
🎂 Date of Birth: {dob}
⚧️ Gender: {gender}

📘 Selected Program: {program}
🕰️ Preferred Schedule: {schedule}
🥋 Martial Arts/Yoga Experience: {experience}

🧘‍♀️ Yoga Experience (years): {yoga_experience or 'N/A'}
📜 Certification: {yoga_certification or 'N/A'}
📚 Interested in Teaching Yoga: {teach_yoga}

❤️ Health Issues: {health_issues}
            """

            # Handle file upload
            if payment_receipt:
                receipt_name = f"receipt_{uuid.uuid4()}_{payment_receipt.name}"
                path = default_storage.save(receipt_name, payment_receipt)
                full_path = default_storage.path(path)
            else:
                full_path = None

            # Send email
            email_message = EmailMessage(
                subject="🥋 New Enrollment Submission with Receipt",
                body=body,
                from_email='ssudipkumar358@gmail.com',
                to=['ssudipkumar358@gmail.com'],
            )

            if full_path:
                email_message.attach_file(full_path)

            email_message.send()

            # Clean up uploaded file
            if full_path and default_storage.exists(full_path):
                default_storage.delete(full_path)

        except Exception as e:
            print(f"⚠️ Error sending enrollment email: {e}")
            messages.error(request, "Something went wrong while submitting your form. Please try again.")
        else:
            messages.success(request, "🎉 Your enrollment form was submitted successfully!")
            form_submitted = True

    return render(request, 'enroll.html', {
        'open_modal': open_modal and not form_submitted,
        'form_submitted': form_submitted,
    })
def freeTrialModal(request):
    open_modal = True            # Keep modal open for GET request or failed POST
    form_submitted = False       # Will be true if submission is successful

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        class_type = request.POST.getlist('class_type[]')
        message = request.POST.get('message')

        # === Send email to owner ===
        try:
            subject = "🥋 New Free Trial Submission"
            class_type_str = ", ".join(class_type)
            body = f"""
A new user has submitted the Free Trial form:

👤 Name: {name}
📧 Email: {email}
📱 Phone: {phone}
🥋 Experience: {experience}
📚 Preferred Classes: {class_type_str}
📝 Message: {message}
            """

            send_mail(
                subject,
                body,
                'ssudipkumar358@gmail.com',         # Your email (must match EMAIL_HOST_USER in settings)
                ['ssudipkumar358@gmail.com'],         # Your recipient/owner email
                fail_silently=False,
            )

        except Exception as e:
            print(f"⚠️ Email sending failed: {e}")
            messages.error(request, "Something went wrong while sending your request. Please try again.")

        else:
            messages.success(request, "🎉 Your free trial request has been submitted successfully!")
            form_submitted = True  # Hide modal after submit

    return render(request, 'freeTrialModal.html', {
        'open_modal': open_modal and not form_submitted,
        'form_submitted': form_submitted,
    })
