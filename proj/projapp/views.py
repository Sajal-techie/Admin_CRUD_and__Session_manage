from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate
from django.contrib import messages
from . models import Custom_user
from django.db.models import Q

  
# login page
@never_cache
def index(request):
    if 'username' in request.session:
        return redirect(home)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Custom_user.objects.get(username = username,password = password)
        except Custom_user.DoesNotExist:
            user = None
            
            
        if user is not None:
            request.session['username'] = username
            
            return redirect(index)
        else:
              if not Custom_user.objects.filter(username=username).exists():
                    messages.error(request, 'Username is not valid')
              else:
                    messages.error(request, 'Invalid password for the given username')
              
              return redirect('index')
        
    return render(request, 'index.html')


# signun page
def signup(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        conf_password = request.POST['password1']
        
        
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters .')
            return render(request,'signup.html')
        
        
        if password != conf_password:
            messages.error(request, 'Passwords do not match.')
            return render(request,'signup.html')
        
        if len(number) != 10:
            messages.error(request, 'Phone number should be 10 digits .')
            return render(request,'signup.html')
        
        # check if the user exist in database
        if Custom_user.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return render(request,'signup.html')
        
        
        if Custom_user.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return render(request,'signup.html')
        
        if Custom_user.objects.filter(number=number).exists():
            messages.error(request, 'number already exists')
            return render(request,'signup.html')
        
        
        # create an instance and save it in the table 
        user = Custom_user(username=username, email=email, number=number, password=password)
        user.save()
        
        messages.success(request, 'Signup successfull . Now, you can Login')
        
        return redirect(index)
    
    return render(request, 'signup.html')
    


# home page 
@never_cache
def home(request):
    if 'username' in request.session:
        username = request.session['username']
        mobile = {
            'mobile_phones' : [
                {
                    'brand': 'Samsung',
                    'name': 'S23 Ultra',
                    'price': '1,24,999',
                    'img':'s23.jpeg'
                },
                {
                    'brand': 'Apple',
                    'name': 'iphone 15 pro',
                    'price': '1,59,999',
                    'img':'iphone15.jpg'
                },
                {
                    'brand': 'Google',
                    'name': 'Pixel 8 pro ',
                    'price': '1,06,999',
                    'img':'pixel8.jpg'
                },
                {
                    'brand': 'OnePlus',
                    'name': 'Open',
                    'price': '1,39,999',
                    'img':'oneplus.jpg'
                },
                {
                    'brand': 'Vivo',
                    'name': 'x90 pro ',
                    'price': '74,999',
                    'img':'vivox90.jpg'
                },
                {
                    'brand': 'Xiaomi',
                    'name': '13 pro ',
                    'price': '79,999',
                    'img':'Xiaomi.webp'
                },
            ],
            'user':username
                   
        }
       
        return render(request,'home.html',mobile)

    return redirect(index)


# logout button
def logout(request):
    if 'username' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out successfully')
        
        return redirect(index)


# loginpage for admins
@never_cache
def admin_login(request):
    if 'username1' in request.session:
        return redirect(admin_home)
    
    if request.method == 'POST':
        username1 = request.POST['username1']
        password = request.POST['password']
        
        user = authenticate(username = username1,password = password)
        
        if user is not None:
            request.session['username1'] = username1
            
            return redirect(admin_login)
        else:
            messages.error(request, 'Invalid username or password')

            return redirect('admin_login')
        
    return render(request, 'admin_login.html')


# homepage for admins
@never_cache
def admin_home(request):
    if 'username1' in request.session:
        us = Custom_user.objects.all()
        context = {
            'user':us
        }
        
        return render(request,'admin_home.html',context)
    
    return redirect(admin_login)

# logout button admin
def admin_logout(request):
    if 'username1' in request.session:
        request.session.flush()
        messages.success(request, 'You have been logged out successfully')
        
        return redirect(admin_login)
    

# add newuser button  
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        
        
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect(admin_home)
        
        
        if len(number) != 10:
            messages.error(request, 'Phone number should be 10 digits long.')
            return redirect(admin_home)
        
        
        if Custom_user.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect(admin_home)
        
        
        if Custom_user.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect(admin_home)
        
        if Custom_user.objects.filter(number=number).exists():
            messages.error(request, 'Number already exist')
            return redirect(admin_home)
        
        user = Custom_user(username=username, email=email, number=number,password=password)
        user.save()
        messages.success(request, 'created new user successfully')
        
        return redirect('admin_home')
        
    return render(request, 'admin_home.html')


def edit_user(request):
    us = Custom_user.objects.all()
    context = {
        'user': us
    }
    return render(request, 'admin_home.html',context)


# update details of existing user
def update_user(request,id):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters .')
            return redirect(admin_home)
        
        
        if len(number) < 10:
            messages.error(request, 'Phone number should be 10 digits .')
            return redirect(admin_home)
        
        
        if Custom_user.objects.exclude(id=id).filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect(admin_home)
        
        
        if Custom_user.objects.exclude(id=id).filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect(admin_home)
        
        if Custom_user.objects.exclude(id=id).filter(number=number).exists():
            messages.error(request, 'number  already exist')
            return redirect(admin_home)
        
        user = Custom_user(
                           id = id ,
                           username=username, 
                           email=email, 
                           number=number,
                           password=password
                           )
        user.save()
        messages.success(request, 'Updated user details ')
        
        return redirect('admin_home')
    

# delete existing user
def delete_user(request,id):
    us = Custom_user.objects.filter(id = id)
    us.delete()
    messages.success(request, 'successfully deleted user data')
    
    return redirect('admin_home')


# search existing user 
def search(request):
    searched = request.GET['search']
    us = Custom_user.objects.filter( Q( username__icontains=searched) | Q( email__icontains=searched) | Q(number__icontains=searched))
    cont = {
        'user': us
    }
    
    return render(request, 'search.html',cont)

 