from django.db import models
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.template.loader import get_template
from django.template import Context
from ecloud import settings
    
   
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=30)
    instance_max = models.IntegerField(blank=True)
    instance_quota = models.IntegerField(blank=True)
    instance_used = models.IntegerField(blank=True)
    cpu_quota = models.IntegerField(blank=True)
    cpu_used = models.IntegerField(blank=True)
    memory_quota = models.IntegerField(blank=True)
    memory_used = models.IntegerField(blank=True)

    #def __str__(self):
    #    return 'Project %s, %sGB RAM, %sGB Disk' % (self.name, self.instance_max, self.instance_quota)

class CloudInfo(models.Model):
    project = models.ForeignKey(Project)
    ipaddress = models.IPAddressField(blank=True)
    port = models.IntegerField(blank=True)
    token = models.CharField(max_length=30)

class Image(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    handler = models.CharField(max_length=100, blank=True)
 
    def __str__(self):
        return '%s, %s, %s' % (self.name, self.description, self.handler)

class Resource(models.Model):
    cpuNum = models.IntegerField(blank=True)
    memorySize = models.IntegerField(blank=True)
    storageSize = models.IntegerField(blank=True)
    flavor = models.IntegerField(blank=True)
    
    def __str__(self):
        return '%sVCPU, %sGB RAM, %sGB Disk' % (self.cpuNum, self.memorySize, self.storageSize)
       
class Order(models.Model):
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    resource = models.ForeignKey(Resource)
    
    startTime = models.DateTimeField()    
    expiredTime = models.DateTimeField()
    
    status = models.CharField(max_length=30)
    hanlderLog = models.TextField()

    # below two item is used for future        
    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.user.username, self.image.name, self.startTime, self.expiredTime, self.status)

    # send email to user for this order, 
    def sendEmail(self):
        subject = '[ECloud] Your order is submitted'
        template = get_template('email/order_submit_email.txt')
        context = Context({
          'username': self.user.username,
          'image': self.image,
          'orderNumber': self.id,
          'startTime': self.startTime,
          'expiredTime': self.expiredTime,
        })
        message = template.render(context)
        email = EmailMessage( subject=subject, body=message,
                            to=[self.user.email], cc=[settings.DEFAULT_ADMIN_EMAIL]
                )
        email.send()
    
class StatusType(models.Model):
    type = models.CharField(max_length=30)
    
    def __str__(self):
        return '%s' %(self.type)
    
class Instance(models.Model):
    order = models.ForeignKey(Order)
    
    instance = models.CharField(max_length=30)
    uniqueID = models.CharField(max_length=100)
    
    internalIPAddress = models.IPAddressField(blank=True)
    externalIPAddress =  models.IPAddressField(blank=True)
    
    status = models.ForeignKey(StatusType)

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.order.user.username, self.order.image.name, self.uniqueID, self.instance, self.status.type)
        
