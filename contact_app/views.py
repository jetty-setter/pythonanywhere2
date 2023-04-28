from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        if subject and message and from_email:
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
            else:
                messages.success(request, 'Your message was sent successfully. We will be in touch soon.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'contact.html')
