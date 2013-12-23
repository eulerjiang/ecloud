# Create your views here.
from django.template import RequestContext

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404

from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.core.mail import BadHeaderError

from ecloud_web.forms import *
from ecloud_web.models import *

from daemon.tasks import *

def main_page(request):
    username = request.user.username
    instance_list = []
    
    if username != '':
        user = User.objects.filter(username = username)
        orders = Order.objects.filter(user = user)
        expiredStatus = StatusType.objects.filter(type = 'expired')
        instance_list = Instance.objects.filter(order=orders).select_related().exclude(status = expiredStatus).order_by("-id")
            
    variables = RequestContext(request, {
        'instance_list': instance_list
    })
    
    return render_to_response('main_page.html', variables)

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html', variables)
        
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
    
@login_required
def order_instance_page(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            templateName = form.cleaned_data['templateName']
            startTime = form.cleaned_data['startTime']
            expiredTime = form.cleaned_data['expiredTime']
            resourceType = form.cleaned_data['resourceType']

            status = 'Submit'
            username = request.user.username
            
            user = get_object_or_404(User, username = username)
            template = get_object_or_404(Image, name = templateName)
            resource = get_object_or_404(Resource, id = resourceType)

            newOrder = Order(image = template,
                            startTime = startTime,
                            expiredTime = expiredTime,
                            status = status, 
                            user = user,
                            resource = resource
                            )
            newOrder.save()
            
            submitOrder.delay(newOrder)
            
            try:
                newOrder.sendEmail()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
              
            return HttpResponseRedirect('/user/view_order')           
    else:
        imageChoices = [ (image.name, image.description) for image in Image.objects.all() ]
        resourceChoices = [ (resource.id,  str(resource.cpuNum)+"CPU," + str(resource.memorySize) + "G MEM," +  str(resource.storageSize) + "G Disk") for resource in Resource.objects.all() ]
        projectChoices = [ (project.id, str(project.name)) for project in Project.objects.all() ]

        if len(imageChoices) == 0 or len(resourceChoices) == 0:
            return HttpResponse('Please contact administrator to update template or type')
        
        form = OrderForm()
        form.setItems(projectChoices, imageChoices, resourceChoices)
        
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('user/order_instance.html', variables)

@login_required
def view_order_page(request):
    username = request.user.username
    
    user = get_object_or_404(User, username = username)
    all_order_list = Order.objects.filter(user = user).order_by('-id')

    order_list = all_order_list.filter(Q(status="submit") | Q(status="success") | Q(status="pending") | Q(status="handling") )
    closed_order_list = all_order_list.filter(Q(status="closed") | Q(status="failed"))
    
    variables = RequestContext(request, {
        'order_list': order_list,
        'closed_order_list': closed_order_list
    })
    return render_to_response('order/list_order.html', variables)

@login_required
def order_list_page(request):
    username = request.user.username
    
    user = get_object_or_404(User, username = username)
    all_order_list = Order.objects.filter(user = user).order_by('-id')

    orderStatusChoices = ('submit','pending','handling','success','failed', 'cancel','close','expired', 'error')

    order_list = all_order_list.filter(Q(status="submit") | Q(status="success") | Q(status="pending") | Q(status="handling") )
    closed_order_list = all_order_list.filter( Q(status="closed") | Q(status="failed"))
    
    variables = RequestContext(request, {
        'order_list': order_list,
        'closed_order_list': closed_order_list
    })
    return render_to_response('order/list_order.html', variables)


@login_required
def order_update_page(request, orderid):
    order = Order.objects.get(id = orderid)
    if request.method == 'POST':
        #action = request.REQUEST['action']
        expiredTime = request.REQUEST['expiredTime'] 
        
        order.expiredTime = expiredTime
        order.save()

    variables = RequestContext(request, {
        'order': order,
     })
    return render_to_response('order/update_order.html', variables)

@login_required
def instance_vnc_console_page(request, instance_uuid):
    print(instance_uuid + ":OK")
    instance = Instance.objects.get(uniqueID = instance_uuid)
    host = request.get_host().split(":")[0]
   
    token = getConsoleToken(instance_uuid)
 
    variables = RequestContext(request, {
        'url': host, 
        'port': '6080',
        'token': token,
        'uuid': instance_uuid
    })
    return render_to_response('instance/vnc_console.html', variables)

@login_required
def instance_action_page(request):
    if request.method == 'POST':
        actionVaule = request.REQUEST['action']
        actionArray = actionVaule.split('__')

        action = actionArray[1]
        instance_uuid = actionArray[2]

        sendInstanceAction.delay(instance_uuid, action)
        variables = RequestContext(request, {
            'action': action,
            'uuid': instance_uuid
        })
        
        return render_to_response('instance/action.html', variables)

@login_required
def instance_list_page(request):

    return ""

@login_required
def resource_usage_page(request):
    return ""
    
