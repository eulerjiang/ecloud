from django.template.loader import get_template
from django.template import Context
from ecloud import settings

from django.core.mail import EmailMessage

def orderExpiredNotify(order, expiredTimeString):
    subject = "%s Your order %s will be expired in %s later" %("[ECloud]", order.id, expiredTimeString)
    
    status = "notify"
    emailTemplateFile="email/order_email.txt"
    if status == "notify":
        emailTemplateFile="email/order_notify_email.txt"

    template = get_template(emailTemplateFile)

    context = Context({
          'username': order.user.username,
          'image': order.image,
          'orderNumber': order.id,
          'startTime': order.startTime,
          'expiredTime': order.expiredTime,
    })

    message = template.render(context)
    email = EmailMessage( subject=subject, body=message,
                            to=[order.user.email], cc=[settings.DEFAULT_ADMIN_EMAIL]
                )
    email.send()

def sendEmail_OrderStatus(order=None,user=None, status=None,attchFile = None):
    subject = '[ECloud] Your order is ' + status
    
    emailTemplateFile="email/order_email.txt"
    if status == "submit":
        emailTemplateFile="email/order_submit_email.txt"
    elif status == "success":
        emailTemplateFile="email/order_email.txt"

    template = get_template(emailTemplateFile)

    context = Context({
            'username': order.user.username,
            'image': order.image,
            'orderNumber': order.id,
            'startTime': order.startTime,
            'expiredTime': order.expiredTime,
            'order': order,
            'status': status
    })

    message = template.render(context)
    email = EmailMessage( subject=subject, body=message,
                            to=[order.user.email], cc=[settings.DEFAULT_ADMIN_EMAIL]
                )
    if attchFile is not None:
        email.attach_file(attchFile)

    email.send()
    
