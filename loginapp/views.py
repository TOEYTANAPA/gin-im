from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import SignUpForm,ProfileForm
from mainapp.models import *
from django.views.generic.edit import UpdateView
# change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from datetime import date
def handler404(request):
    print("404")
    response = render_to_response('404.html',{},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler403(request):
    print("403")
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response

def handler400(request):
    print("400")
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response

def handler500(request):
    print("500")
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def home(request):
    return render(request, 'home.html',{'username': request.user.username})

# from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

# @login_required
# def profile(request):
#     love_list = []
#     order_list =[]
#     try:
#         p = Profile.objects.get(user = request.user)
#         print (p.name)
#         print (p.picture.url)
#         form = ProfileForm(initial={'name': p.name,'image':p.picture.url,'phone':p.phone_number,'address':p.address})
#         form.fields['name'].widget.attrs['placeholder'] = p.name
#         # form.fields['image'].widget.attrs['placeholder'] = p.picture.url
#         form.fields['phone'].widget.attrs['placeholder'] = p.phone_number
#         form.fields['address'].widget.attrs['placeholder'] = p.address

#         if request.method == 'POST':
#             form = ProfileForm(request.POST, request.FILES)
#             if form.is_valid():
#                 print("Earn")
#                 profile_update = Profile.objects.filter(user=request.user).update(name=form.cleaned_data['name'],
#                     picture= request.FILES['image'],
#                     address=form.cleaned_data['address'],
#                      phone_number=form.cleaned_data['phone'])
#                 p = Profile.objects.get(user=request.user)
#                 p.picture = request.FILES['image']
#                 p.save()
#                 # form.save()
               
#                 # login(request, user)
#                 return redirect('profile')
       
#         love = {'name' : '' , 'img':''}   
      
#         user = request.user
#         store = Store.objects.filter(likes=user)
#         for l in store:
#             love['name'] = l.name
#             love['img'] = l.image
#             love_list.append(love)
       

#         try :
#             reviews = Review.objects.filter(user=request.user)
#             temp = { 'rating_color': 0,'rating_no_color': 0, }
#             rate = []
#             profile_picture = []
#             for i in reviews:
#                 temp['rating_color'] = i.rating
#                 temp['rating_no_color'] = 5 - temp['rating_color']
#                 rate.append(temp)
#                 profile_picture.append(Profile.objects.get(user=i.user).picture.url)

#             out = zip(reviews,rate,profile_picture)
#             mobile_out = zip(reviews,rate,profile_picture)
#             # review

#         except :
#             raise

#         try :
#             orders = Order.objects.filter(user=request.user)
#             for i in orders:
#                 temp = {'id':0,'name_s':"",'menu_amount':[],'date':None}
#                 temp['id'] = i.id
#                 print(i.store.id)
#                 s = Store.objects.get(id=i.store.id) 
#                 temp['name_s'] = s.name
#                 temp['date'] = i.date

#                 menu_list = []
#                 amount_list = []
#                 keys = ['menu','amount']
#                 for m,a in zip(i.menu,i.amount):
#                     ma = {'menu':Menu.objects.get(id=m),'amount':a}
#                     temp['menu_amount'].append(ma)
#         #             menu_list.append(Menu.objects.get(id=m))
#         #             amount_list.append(a)
                    
#         # { row.SITE_NAME : row.LOOKUP_TABLE for row in cursor }
                
#         #         temp['menu_amount'](dict(zip(menu_list, amount_list)))
            

#                 order_list.append(temp)

#         except :
#             raise


#     except Profile.DoesNotExist:
#             raise



#     return render(request, 'profile.html',{'form': form,'username': request.user.username,'person':p,'love_list':love_list,'order_list':order_list,'out':out,'mobile_out':mobile_out})

# @login_required
# def profile_store(request):
#     love_list = []
#     order_list =[]
#     try:
#         p = Profile.objects.get(user = request.user)
#         print (p.name)
#         print (p.picture.url)
#         form = ProfileForm(initial={'name': p.name,'image':p.picture.url,'phone':p.phone_number,'address':p.address})
#         form.fields['name'].widget.attrs['placeholder'] = p.name
#         form.fields['phone'].widget.attrs['placeholder'] = p.phone_number
#         form.fields['address'].widget.attrs['placeholder'] = p.address

#         if request.method == 'POST':
#             form = ProfileForm(request.POST, request.FILES)
#             if form.is_valid():
#                 print("Earn")
#                 profile_update = Profile.objects.filter(user=request.user).update(name=form.cleaned_data['name'],
#                     picture= request.FILES['image'],
#                     address=form.cleaned_data['address'],
#                      phone_number=form.cleaned_data['phone'])
#                 p = Profile.objects.get(user=request.user)
#                 p.picture = request.FILES['image']
#                 p.save()
   
#                 return redirect('profile')
       
#         love = {'name' : '' , 'img':''}   
      
#         user = request.user
#         store = Store.objects.filter(likes=user)
#         for l in store:
#             love['name'] = l.name
#             love['img'] = l.image
#             love_list.append(love)
       

#         try :
#             reviews = Review.objects.filter(user=request.user)
#             temp = { 'rating_color': 0,'rating_no_color': 0, }
#             rate = []
#             profile_picture = []
#             for i in reviews:
#                 temp['rating_color'] = i.rating
#                 temp['rating_no_color'] = 5 - temp['rating_color']
#                 rate.append(temp)
#                 profile_picture.append(Profile.objects.get(user=i.user).picture.url)

#             out = zip(reviews,rate,profile_picture)
#             mobile_out = zip(reviews,rate,profile_picture)
#             # review

#         except :
#             raise

#         try :
#             orders = Order.objects.filter(user=request.user)
#             for i in orders:
#                 temp = {'id':0,'name_s':"",'menu_amount':[],'date':None}
#                 temp['id'] = i.id
#                 print(i.store.id)
#                 s = Store.objects.get(id=i.store.id) 
#                 temp['name_s'] = s.name
#                 temp['date'] = i.date

#                 menu_list = []
#                 amount_list = []
#                 keys = ['menu','amount']
#                 for m,a in zip(i.menu,i.amount):
#                     ma = {'menu':Menu.objects.get(id=m),'amount':a}
#                     temp['menu_amount'].append(ma)
#         #             menu_list.append(Menu.objects.get(id=m))
#         #             amount_list.append(a)
                    
#         # { row.SITE_NAME : row.LOOKUP_TABLE for row in cursor }
                
#         #         temp['menu_amount'](dict(zip(menu_list, amount_list)))
            

#                 order_list.append(temp)

#         except :
#             raise


#     except Profile.DoesNotExist:
#             raise



#     return render(request, 'profile_store.html',{'form': form,'username': request.user.username,'person':p,'love_list':love_list,'order_list':order_list,'out':out,'mobile_out':mobile_out})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print("Earn")
           
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            p = Profile(picture = request.FILES['image'],user=user,name=username,email=form.cleaned_data.get('email'))
            p.save()
            # login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def profile(request):
    

    love_list = []
    order_list =[]
    coupon_list =[]

    user_order_list=[]
    try:
        p = Profile.objects.get(user = request.user)
        print (p.name)
        print (p.picture.url)
        form = ProfileForm(initial={'name': p.name,'image':p.picture.url,'phone':p.phone_number,'address':p.address})
        form.fields['name'].widget.attrs['placeholder'] = p.name
        # form.fields['image'].widget.attrs['placeholder'] = p.picture.url
        form.fields['phone'].widget.attrs['placeholder'] = p.phone_number
        form.fields['address'].widget.attrs['placeholder'] = p.address

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                print("Earn",form.cleaned_data['name'])
                profile_update = Profile.objects.filter(user=request.user).update(
                    name=form.cleaned_data['name'],
                    picture= request.FILES['image'],
                    address=form.cleaned_data['address'],
                    phone_number=form.cleaned_data['phone'])
                p = Profile.objects.get(user=request.user)
                p.picture = request.FILES['image']
                p.save()
                # form.save()
            else:
                profile_update = Profile.objects.filter(user=request.user).update(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone'])

                # login(request, user)
                return redirect('profile')
       
        love = {'name':'', 'id' : 0 , 'img':''}   
      
        user = request.user
        store = Store.objects.filter(likes=user)
        for l in store:
            love['id'] = l.id
            love['img'] = l.image
            love['name'] = l.name
            print(love['id'] ," this is id")
            love_list.append(love)
       

        try :
            reviews = Review.objects.filter(user=request.user)
            temp = { 'rating_color': 0,'rating_no_color': 0, }
            rate = []
            profile_picture = []
            for i in reviews:
                temp['rating_color'] = i.rating
                temp['rating_no_color'] = 5 - temp['rating_color']
                rate.append(temp)
                profile_picture.append(Profile.objects.get(user=i.user).picture.url)

            out = zip(reviews,rate,profile_picture)
            mobile_out = zip(reviews,rate,profile_picture)
            # review

        except :
            raise

        try :
            orders = Order.objects.filter(user=request.user)
            for i in orders:
                temp = {'id':0,'name_s':"",'menu_amount':[],'date':None}
                temp['id'] = i.id
                print(i.store.id)
                s = Store.objects.get(id=i.store.id) 
                temp['name_s'] = s.name
                temp['date'] = i.date

                menu_list = []
                amount_list = []
                
                for m,a in zip(i.menu,i.amount):
                    ma = {'menu':Menu.objects.get(id=m),'amount':a}
                    temp['menu_amount'].append(ma)
                

                order_list.append(temp)


        except :
            pass

        try :
            coupon = GetCoupon.objects.filter(user=request.user)
            for i in coupon :   
                c = Coupon.objects.get(id=i.coupon.id)
                # print("Is expired : ",date.today() !>  c.date_expire)
                temp = {'id_coupon': 0,'id_store':0,'name':"",'msg':"",'amount':1,'date': None,'code':"-", 'image':""}
                if i.amount > 0 and date.today() <  c.date_expire :            

                    temp['id_coupon'] = c.id
                    temp['name'] = c.store.name
                    temp['id_store'] = c.store.id
                    temp['msg'] = c.msg
                    temp['amount'] = i.amount
                    temp['date'] = c.date_expire
                    temp['image'] = c.image
                    if c.code != None :
                        temp['code'] = c.code
                    coupon_list.append(temp)
        except :
            raise

       

        

    except Profile.DoesNotExist:
        form = ProfileForm()
        profile = Profile.objects.create(user=request.user,name=request.user.get_short_name(),email = request.user.email)
        print(profile.user)
    
    # check = Profile.objects.get(user=request.user)
    person = Profile.objects.get(user=request.user)
    try :
        s = StoreByUser.objects.get(user=request.user)
        try :
            p = s.store
            if "delivery" in p.tags :
                delivery = True
            else :
                delivery = False
           
            user_order = Order.objects.filter(store__id=p.id).order_by('-date')

            for i in user_order:
                temp = {'id':0,'username':'','address':'','menu_amount':[],'date':None,'total':0,
                'slip':None}
                temp['id'] = i.id
                temp['username'] = i.user.username
                temp['address'] = i.address
                temp['total'] = i.total
                temp['slip'] = i.slip_payment
                menu_list = []
                amount_list = []
                    
                for m,a in zip(i.menu,i.amount):
                    ma = {'menu':Menu.objects.get(id=m),'amount':a}
                    temp['menu_amount'].append(ma)
                temp['date'] = i.date

                user_order_list.append(temp)
                print(user_order_list)
            return render(request, 'profile_store.html',{'form': form,'username': request.user.username,
                'person':person,'user_order_list_mobile':user_order_list,'user_order_list_desktop':user_order_list,
                'delivery':delivery})
        except :
            raise
    except StoreByUser.DoesNotExist:
        return render(request, 'profile.html',{'form': form,'username': request.user.username,
            'person':p,'love_list':love_list,'order_list':order_list,'out':out,
            'mobile_out':mobile_out,'coupon_list':coupon_list,'coupon_list_mobile':coupon_list})

    # if check.status == 'store' :
    #     try :
    #         p = Store.objects.get(user = request.user)
    #         user_order = Order.objects.filter(store__id=p.id)

    #         for i in user_order:
    #             temp = {'id':0,'username':'','address':'','menu_amount':[],'date':None,'total':0}
    #             temp['id'] = i.id
    #             temp['username'] = i.user.username
    #             temp['address'] = i.address
    #             temp['total'] = i.total
    #             menu_list = []
    #             amount_list = []
                    
    #             for m,a in zip(i.menu,i.amount):
    #                 ma = {'menu':Menu.objects.get(id=m),'amount':a}
    #                 temp['menu_amount'].append(ma)
    #             temp['date'] = i.date

    #             user_order_list.append(temp)
    #     except :
    #         raise

        # return render(request, 'profile_store.html',{'form': form,'username': request.user.username,
        #     'person':p,'user_order_list_mobile':user_order_list,'out':out,
        #     'mobile_out':mobile_out})
    # else :


    

    # return render(request, 'profile.html',{'form': form,'username': request.user.username,
    #         'person':p,'love_list':love_list,'order_list':order_list,'out':out,
    #         'mobile_out':mobile_out,'coupon_list':coupon_list,'coupon_list_mobile':coupon_list})