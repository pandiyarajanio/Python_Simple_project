from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .form import userupdate

# Create your views here.



def index(request):
    if request.session.has_key('log'):
        return render(request,'index.html')
    else:
        return redirect('login')



def login(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    if request.session.has_key('log'):
        return redirect('index')
    else:

        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            try:
                check=User.objects.get(username=username)
                if not check.is_active:
                    messages.info(request,'acces denied')
                    return redirect('login')
            except:
                pass
            user = auth.authenticate(request,username=username,password=password)
            if user is not None:
                request.session['log']='log'
                return redirect('index')
            else:
                messages.info(request,'invalid username and password')
                return redirect('login')
        else:
            return render(request,'login.html')



def register(request):
    if request.session.has_key('log'):
        return redirect('index')
    else:
        if request.method =='POST':
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
            password2=request.POST['password2']
           # print(username, email, password1, password2)
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'username taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'email taken')
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,email=email,password=password1)
                    user.save()
                    return redirect('login')
            else:
                messages.info(request,'password is not matching......')
                return redirect('register')
        else:
            return render(request,'register.html')


def logout(request):
    del request.session['log']
    return redirect('login')


def adminlogin(request):
    # if request.user.is_authenticated:
    #     return redirect('adminhome')
    if request.session.has_key('admin-log'):
        return redirect('adminhome')
    else:

        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']

            user= auth.authenticate(username=username,password=password)

            if user is not None:

                if user.is_superuser:
                    # auth.login(request,user)
                    request.session['admin-log']='admin-log'
                    messages.info(request,'succesfully loged')
                    return redirect('adminhome')
                else:
                    messages.info(request,'you are not user')
                    return redirect('adminlogin')
            else:
                    messages.info(request,'invalid credential')
                    return redirect('adminlogin')
        else:
            return render(request,'adminlogin.html')


def adminhome(request):
    if request.session.has_key('admin-log'):
        users=User.objects.all()
        print(users)    

        context={'users':users}
        return render(request,'adminhome.html',context)
    else:
        return redirect('adminlogin')


# def delete(request,pk):
#     user=User.objects.get(id=pk)
#     if request.method=='POST':
#         User.objects.get(id=pk).delete()
#         return redirect('adminhome')
#     context = {'user':user}
#     return render(request,'delete.html',context)


def delete(request,pk):
    User.objects.get(id=pk).delete()
    return redirect('adminhome')



def block(request,pk):
    user=User.objects.get(id=pk)
    user.is_active=False
    user.save()
    if 'log' in request.session:
        del request.session['log']
    return redirect('adminhome')

def unblock(request,pk):
    user=User.objects.get(id=pk)
    user.is_active=True
    user.save()
    return redirect('adminhome')

def update(request,pk):
    if request.session.has_key('admin-log'):
        print(pk)
        user = User.objects.get(id=pk)
        form = userupdate(instance=user)
        context = {'form' : form, }
        if request.method=="POST":
            print(user)
            form = userupdate(request.POST, instance=user)
            if form.is_valid():
                try:
                    form.save()
                except:
                    # if User.objects.filter(username='username').exists:
                    #     messages.info(request,'user is already exists') 
                    # else:
                    messages.info(request,'Email address is already exists') 
                    return render(request,'update.html',context)
            return redirect('adminhome')

        context = {'form' : form}
        return render(request,'update.html',context)
    else:
        return redirect('adminlogin')



def adduser(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request,'username taken')
            return redirect('adduser')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email is taken')
            return redirect('adduser')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            print('user created')
            return redirect('adminhome')
    else:
        return render(request,'add.html')

def adminlogout(request):
    del request.session['admin-log']
    auth.logout(request)
    return redirect('adminlogin')



