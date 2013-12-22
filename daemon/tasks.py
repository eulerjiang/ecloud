'''
Created on Mar 15, 2013

@author: Euler Jiang
'''
from ecloud_web.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

from celery import task
import datetime

from daemon.InstanceHandler import InstanceHanlder

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from util.email import orderExpiredNotify,sendEmail_OrderStatus

@periodic_task(run_every=crontab(hour="*", minute="*/5", day_of_week="*"))
def instanceDeleteNotify():
    print("Check will be expired order and notify user")
    currentDatetime = datetime.datetime.today()
    # 
    timedelta1=datetime.timedelta(hours=24)
    timedelta2=datetime.timedelta(hours=4)
    timedelta3=datetime.timedelta(minutes=30)

    activeOrderList = Order.objects.filter(status ='Finished')
    print("current time: %s", currentDatetime)
    for order in activeOrderList:
        myExpiredDatetime =  order.expiredTime
        expiredTimeDelta = myExpiredDatetime - currentDatetime
        print("check order %d %s", order.pk, myExpiredDatetime)
        if datetime.timedelta(minutes=25) <= expiredTimeDelta <= datetime.timedelta(minutes=30):
            print("Your VM will be expired in 30 minutes later")
            timeDelta = "30 minutes"
        elif datetime.timedelta(hours=3, minutes=55) <= expiredTimeDelta <= datetime.timedelta(hours=4):
            print("Your VM will be expired in 4 hours later")
            timeDelta = "4 hours"
        elif datetime.timedelta(hours=23, minutes=55) < expiredTimeDelta <= datetime.timedelta(hours=24):
            print("Your VM will be expired in 1 day later")
            timeDelta = "1 day"
        else:
            print("Not need to send notification")
            continue
        orderExpiredNotify(order,timeDelta)
    return 0

@periodic_task(run_every=crontab(hour="*", minute="*/2", day_of_week="*"))
def cleanExpiredInstance():
    currentDatetime = datetime.datetime.today()
    
    expiredOrderList = Order.objects.exclude(status ='closed').filter(Q(expiredTime__lte = currentDatetime))
    print("Start Clean Expired Instance")
    for oneOrder in expiredOrderList:
        instance = Instance.objects.get(order = oneOrder)

        handler = InstanceHanlder()
        handler.destroyInstance(instance.uniqueID, oneOrder.image.handler)
        
        instances = Instance.objects.filter(order = oneOrder)
        if len(instances) == 1:
            intance = instances[0]
            intance.status = get_object_or_404(StatusType, type="expired")
            intance.save()
        
        oneOrder.status = "closed"
        oneOrder.save()
    return 0

@task
def submitOrder(NewOrder):
    imageName = NewOrder.image.name
    handlerCommand = NewOrder.image.handler
    username = NewOrder.user.username

    # update order status to handling
    NewOrder.status = "handling"
    NewOrder.save()
    
    # create instance handler
    orderHandler = InstanceHanlder()

    handleLogFile = settings.ecloud_log_dir + "/order" + str(NewOrder.pk) + ".log"

    resultCode = orderHandler.createInstance(imageName, username, NewOrder.pk, handlerCommand)
    if resultCode != 0:
        print( "Failed to handling order %s, %s, %s" % (imageName, username, NewOrder.pk) )
        # update order status
        NewOrder.status = "failed"
        NewOrder.HandlerLog = orderHandler.failureReason

        NewOrder.save()
        sendEmail_OrderStatus(order=NewOrder,status='failed', attchFile = handleLogFile )
        return "Failed to handling order %s, %s, %s" % (imageName, username, NewOrder.pk)
    else:
        # insert instance to instance table
        instanceName =  orderHandler.getInstanceName()
        publicIP = orderHandler.getInstancePublicIP()
        privateIP = orderHandler.getInstancePrivateIP()
        
        uniqueID = orderHandler.getInstanceUniqueID()
        
        status = get_object_or_404(StatusType, type="running")
        
        NewInstance = Instance(order = NewOrder, instance=instanceName, uniqueID = uniqueID, internalIPAddress = privateIP, externalIPAddress = publicIP, status = status)
        NewInstance.save()
            
        # update order status
        NewOrder.status = "success"
        NewOrder.save()

        sendEmail_OrderStatus(order=NewOrder, status='success',attchFile = handleLogFile)
        
        return "Success to handle order"

@task
def sendInstanceAction(uuid, action):
    if action == 'start':
        startInstance(uuid)
    elif action == 'restart':
        restartInstance(uuid)
    elif action == 'stop':
        stopInstance(uuid)
    elif action == 'delete':
        deleteInstance(uuid)       

    return "Success to send action %s to instance %s" %(action, uuid)

@task
def startInstance(uuid):
    instance = Instance.objects.get(uniqueID = uuid)
    order = instance.order
    command = order.image.handler
    
    userid = order.user.username
    instanceUniqueID = uuid
    
    handler = InstanceHanlder()
    handler.startInstance(uuid, command)

    instance.status = get_object_or_404(StatusType, type="running")
    instance.save()
    
    return "Success to start instance"

@task
def stopInstance(uuid):
    instance = Instance.objects.get(uniqueID = uuid)
    order = instance.order
    command = order.image.handler
    
    userid = order.user.username
    instanceUniqueID = uuid
    
    handler = InstanceHanlder()
    handler.stopInstance(uuid, command)

    # if success  
    instance.status = get_object_or_404(StatusType, type="shutdown")
    instance.save()
  
    return "Success to stop instance"

@task
def restartInstance(uuid):
    instance = Instance.objects.get(uniqueID = uuid)
    order = instance.order
    command = order.image.handler
    
    userid = order.user.username
    instanceUniqueID = uuid
    
    instance.status = get_object_or_404(StatusType, type="rebooting")
    instance.save()

    handler = InstanceHanlder()
    handler.restartInstance(uuid, command)

    # if success
    instance.status = get_object_or_404(StatusType, type="running")
    instance.save()
  
    return "Success to restart instance"

@task
def deleteInstance(uuid):
    instance = Instance.objects.get(uniqueID = uuid)
    order = instance.order
    
    print("----------------------")
    order.expiredTime = datetime.datetime.today()
    order.save()
    print(order)
  
    return "Success to delete instance"

@task
def getConsoleToken(uuid):
    instance = Instance.objects.get(uniqueID = uuid)
    order = instance.order
    command = order.image.handler
    
    handler = InstanceHanlder()
    token = handler.getVNCConole(uuid, command)
    token = token.strip()

    return token
