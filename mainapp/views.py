from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.contrib.postgres.search import SearchVector,TrigramSimilarity,SearchQuery,SearchRank
from django.db.models import Avg
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.sessions.models import Session
from datetime import date


def home(request):
	reviews_list = Review.objects.all()[:10]
	temp = { 'rating_color': 0,'rating_no_color': 0, }
	rate = []
	profile_picture = []
	out= []
	mobile_out =[]


	
	try :
		for i in reviews_list:
			temp['rating_color'] = i.rating
			temp['rating_no_color'] = 5 - temp['rating_color']
			rate.append(temp)
			profile_picture.append(Profile.objects.get(user=i.user).picture.url)
		out = zip(reviews_list,rate,profile_picture)
		mobile_out= zip(reviews_list,rate,profile_picture)
	except :
		raise Http404


	response = set_cookie(request, 'home.html', {'out':out,'mobile_out':mobile_out})
	
	
	return response

@login_required
def addStore(request):
	addForm = StoreForm()
	if request.method == 'POST':
		addForm = StoreForm(request.POST, request.FILES)
		if addForm.is_valid():
			print("is valid")
			tag=addForm.cleaned_data['category']
			delivery= addForm.cleaned_data['delivery'],
			if delivery:
				tag += ",delivery"
			print(tag)
			create_store = Store.objects.create(
		           # user = request.user,
		           name = addForm.cleaned_data['store_name'],
		           place = addForm.cleaned_data['place'],
		           phone = addForm.cleaned_data['phone'],
		           category = addForm.cleaned_data['category'],
		           day_open =  addForm.cleaned_data['day_open'],
		           time_open= addForm.cleaned_data['time_open'],
		           time_close= addForm.cleaned_data['time_close'],
		           tags= tag,
		           image =request.FILES['store_image'],
		           created_by= request.user)
			next_page = "/store/"+str(create_store.id)
			return HttpResponseRedirect(next_page)

	return render(request, 'addStore.html', {'addStoreForm':addForm,})
    # return redirect('loginapp.add_store')

@login_required
def addMenu(request,pk):
	menuForm = MenuForm()
	try:
		store = Store.objects.get(id=pk)
		if request.method == 'POST':
			menuForm = MenuForm(request.POST, request.FILES)
			if menuForm.is_valid():
				print("is valid")
				create_menu = Menu.objects.create(
					store = store,
		          	name = menuForm.cleaned_data['menu_name'],
		          	price = menuForm.cleaned_data['menu_price'],
		          	image =request.FILES['menu_image'],
		          	created_by= request.user)
				next_page = "/store/"+str(pk)
				return HttpResponseRedirect(next_page)
	except Store.DoesNotExist:
		return HttpResponseRedirect('home')	
	
				# return render() go to some page that tell error not have tihs store 
	return render(request, 'addMenu.html', {'menuForm':menuForm,'store_name':store.name})

def set_cookie(request,template,dicts):
	response = render(request, template, dicts)
	if request.user.is_authenticated():
		print("User has login")
	else :
		if not request.session.session_key:
			request.session.save()
		session_id = request.session.session_key
		if 'name' in request.COOKIES:
			value = request.COOKIES['name']
			# response.delete_cookie('name')
			print("old cookie "+ value)
		else :
			# expire in 10 years
			response.set_cookie('name',session_id,max_age= 315360000)
			print(" new cookie create")

	return response
    
    
@login_required
def report(request):
    return render(request, 'report.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')
    
@login_required
def questionnaire(request):
    return render(request, 'questionnaire.html')

@login_required
@csrf_exempt
def delivery(request):

	if request.is_ajax():
		address = request.GET.get('address',False)
		phone_number = request.GET.get('phone_number',False)
		payment = request.GET.get('payment',False)

		order = request.GET.get('data',False)
		order = json.loads(order)
		print(address)
		print(phone_number)
		print(payment)
		menu_list = []
		amount_list = []

		for item in order :

			m = Menu.objects.get(store__id=item['store'],name=item['name'])
			menu_list.append(m.id)
			amount_list.append(item['amount'])
			s = Store.objects.get(id=item['store'])
		order = Order.objects.create(user=request.user,menu=menu_list,store=s,amount=amount_list,address =address)

			# print("order_id : ",order.id)

	return JsonResponse({'order_id':order.id},safe=False)

 
  

  


@login_required
def success(request,order_id):
	return render(request,'delivery.html',{'username':request.user.username,'id':order_id}) 

@login_required
def order(request):
	orders = Order.objects.filter(user = request.user)
	menu = []
	for o in orders:
		menu.append({"name":o.menu.name,"image":o.menu.image.url})

	return render(request, 'order.html',{'menu':menu})
    




# @login_required
def shop(request, pk):

	collect_session(request,"enter_store",pk)

	temp = { 'rating_color': 0,'rating_no_color': 0, }
	reviewForm = ReviewForm()
	# print("name:", string)
	store = Store.objects.get(id=pk)
	delivery = False
	if "delivery" in store.tags :
		delivery = True
	cate = store.category
	menues2 =  Menu.objects.filter(store=store).order_by('-id')[:]

	reviews = Review.objects.filter(store=store)

	rate = []
	profile_picture = []
	store_loved_color = None
	if request.user.is_authenticated():
		user = request.user
		store = get_object_or_404(Store, id=pk)
		if store.likes.filter(id=user.id).exists():
			store_loved_color= True
		else:
			store_loved_color = None

	for i in reviews:
		temp['rating_color'] = i.rating
		temp['rating_no_color'] = 5 - temp['rating_color']
		rate.append(temp)
		try :
			profile_picture.append(Profile.objects.get(user=i.user).picture.url)
		except:
			raise Http404


	out = zip(reviews,rate,profile_picture)
	if request.method == 'POST':
		if "review" in request.POST:
			if request.POST['star'] is  None:
				star = 0;
			else:
				star = request.POST['star']
			print ("star: ",star)
			reviewForm = ReviewForm(request.POST, request.FILES)
			if reviewForm.is_valid():
				review = Review.objects.create(
		            user = request.user,
		            store = store,
		            comment = reviewForm.cleaned_data['comment'],
		            rating = star,)
				next_page = "/main/"+store.name
				return HttpResponseRedirect(next_page)
		elif "order" in request.POST:
			print("order post")
			output = []
			total=0
			price_per_menu = 0;
			a = {"orderlist": [], "price": [], "url_pic": [], "amount": []}
			for m in menues2:
				temp = {'name': '', 'url_pic' : '', 'amount': 0,"store":store}
				# print("id",m.id)
				if request.POST.get(str(m.id)) is  None:
					next_page = "/store/"+str(pk)
					return HttpResponseRedirect(next_page)
					# pass

				else:
					p = Profile.objects.get(user=request.user)
					delivery_address = p.address 
					delivery_phone = p.phone_number
					print(p)
					print(p.address)
					print(p.name)
					
					a = request.POST.get(str(m.id))
					name = Menu.objects.get(id=m.id).name
					# print("earrn")
					# print (name,a)
					# temp['name'] = m.name
					# temp['url_pic'] = m.image.url,
					if int(a) > 0:
						if " " in m.price:
							size,price= m.price.split(" ")

						else:
							price = m.price

						price_per_menu = int(price)*int(a)
						total += price_per_menu
						# temp['amount'] = a
						
						# output.append(temp)
						output.append({"name":name,
							"price":price_per_menu,
							"url_pic":m.image.url,
							"amount":a,
							"store":store.id
							})
						# Order.objects.create(user=request.user,menu=m)
						print("go to checkout")
			return  render(request,'checkout.html',{'username':request.user.username,'data':json.dumps(output),
				'output':output,'total':total,'delivery_address':delivery_address,'delivery_phone':delivery_phone})


	return render(request,'stores.html',{'reviewForm':reviewForm,'username':request.user.username,'menues':reversed(menues2),'mobile_menues':reversed(menues2),
		'reviews':reviews,'out':out,'store':store,'delivery':delivery,'category':cate,'store_loved_color':store_loved_color})




def searchBycate(request,cate):
	stores_list = []
	stores =[]
	store_love_list =[]

	collect_session(request,"search_cate",cate)
	try :
		if cate == "all":
			stores = Store.objects.all()
		else :
			stores = Store.objects.filter(tags__contains=cate)
		print("stores",stores)
		

		for s in stores :
			temp = {'name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
			
			# temp['name'].append(s.name)
			temp['name'] = s.name
			tags = s.tags.split(',')
			for tag in tags :
				temp['tags'].append(tag)

			try:
				rating_avg = Review.objects.filter(store__name = s.name).aggregate(Avg('rating'))
				temp['rating_color'] = round(rating_avg['rating__avg'])

			except:
				temp['rating_color'] = 0


			temp['rating_no_color'] = 5 - temp['rating_color']

			temp['no_reviews'] = Review.objects.filter(store__name=s.name).count()

			menues = Menu.objects.filter(store__name=s.name)[:4]
			for menu in menues:
				temp['menues'].append(menu)

			temp['love'] = s.total_likes
			
			if request.user.is_authenticated():
				user = request.user
				store = get_object_or_404(Store, name=s.name)
				if store.likes.filter(id=user.id).exists():
					temp['store_loved_color'] = True
				else:
					temp['store_loved_color'] = None
					
			
			stores_list.append(temp)

		print("============================")
		for i in stores_list:
			print (i)

	except Exception as e:
		raise Http404


	return render(request, 'search_cate.html',{'stores':stores_list,'category':cate,})



def searchAll(request):
	stores_list = []
	stores =[]
	store_love_list =[]
	cate = request.POST.get("search", "")

	collect_session(request,'search_input',cate)
	# collect_session(request,'search_input',cate)

	if request.method == 'POST':
		if request.POST.get('search') is None:
			return  HttpResponseRedirect('/main/')
		else:
			print("ddd",request.POST.get('search'))	

		


	try :
		# stores = Store.objects.filter(tags__contains=cate)

		stores= Store.objects.annotate(search=SearchVector('tags', 'name')).filter(search__contains=cate)

		for s in stores :
			temp = {'name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
			temp['name'] = s.name

			tags = s.tags.split(',')
			for tag in tags :
				temp['tags'].append(tag)

			try:
				rating_avg = Review.objects.filter(store__name = s.name).aggregate(Avg('rating'))
				temp['rating_color'] = round(rating_avg['rating__avg'])

			except:
				temp['rating_color'] = 0


			temp['rating_no_color'] = 5 - temp['rating_color']

			temp['no_reviews'] = Review.objects.filter(store__name=s.name).count()

			menues = Menu.objects.filter(store__name=s.name)[:4]
			for menu in menues:
				temp['menues'].append(menu)

			temp['love'] = s.total_likes
			
			if request.user.is_authenticated():
				user = request.user
				store = get_object_or_404(Store, name=s.name)
				if store.likes.filter(id=user.id).exists():
					temp['store_loved_color'] = True
				else:
					temp['store_loved_color'] = None

			stores_list.append(temp)



	except :
		raise


	return render(request, 'search_input.html',{'stores':stores_list,'category':cate})


def outofstock(request):
    print("earn")
    store = StoreByUser.objects.get(user = request.user).store
    print(store)
    print(store.quote)
    menulist = Menu.objects.filter(store=store).order_by('-id')[:]

    # if request.method == 'POST':
    #     user = request.user
    #     s_name = request.POST.get('pk', None)
    #     print(s_name)
    #     store = get_object_or_404(Store, name=s_name)
    #     print(store)

    #     if store.likes.filter(id=user.id).exists():
    #         store.likes.remove(user)
    #     else:
    #         store.likes.add(user)
    return render(request, 'outofstock.html',{'menues':reversed(menulist),'store':store,'mobile_menues':reversed(menulist)})

def collect_session(request,act,val):
	if request.user.is_authenticated():
		User_session.objects.create(user=request.user,action=act,value=val)
	else :
		if 'name' in request.COOKIES:
			name = request.COOKIES['name']
			Anonymous_session.objects.create(name=name,action=act,value=val)


@login_required
def fill_in(request):
	# form = InformationsForm()
	# # print(form)
	return render(request, 'informations.html')


@login_required
def fill_in_edit(request):
	try:
		if Informations.objects.filter(user=request.user).exists():
			return render(request, 'informations_complete.html') 
		else :
			return render(request, 'informations.html') 
		
	except:
		raise

def calculate_age(day,month,year):
	today = date.today()
	year = int(year)
	month = int(month)
	day = int(day)
	print(type(year))
	return today.year - year - ((today.month, today.day) < (month, day))

@login_required
def fill_in_complete(request):
	if request.method == 'POST':
	
		list_meal = request.POST.getlist('meal')
		if not list_meal :
			print("mobile")
			list_meal = request.POST.getlist('meal-mobile')
			list_reason = request.POST.getlist('reason-mobile')
			list_size = request.POST['size-mobile']
			list_social = request.POST.getlist('social-mobile')
			list_fav = request.POST.getlist('fav-mobile')

		else :
			print("desktop")
			list_meal = request.POST.getlist('meal')
			list_reason = request.POST.getlist('reason')
			list_size = request.POST['size']
			list_social = request.POST.getlist('social')
			list_fav = request.POST.getlist('fav')

		gender = request.POST['sex']
		day = request.POST['day']
		month = request.POST['month']
		year = request.POST['year']
		salary = request.POST['salary']

		try :

			age = calculate_age(day,month,year)

			if 'bf' in list_meal :
				bf = True
			else :
				bf = False
			if 'lunch' in list_meal :
				lunch = True
			else :
				lunch = False	
			if 'dinner' in list_meal :
				dinner = True
			else :
				dinner = False
			if 'late' in list_meal :
				late = True
			else :
				late = False


			if 'taste' in list_reason :
				taste = True
			else :
				taste = False
			if 'price' in list_reason :
				price = True
			else :
				price = False
			if 'service' in list_reason :
				service = True
			else :
				service = False
			if 'clean' in list_reason :
				clean = True
			else :
				clean = False
			if 'at' in list_reason :
				at = True
			else :
				at = False
			if 'location' in list_reason :
				location = True
			else :
				location = False

				
			if 'facebook' in list_social :
				facebook = True
			else :
				facebook = False
			if 'twitter' in list_social :
				twitter = True
			else :
				twitter = False
			if 'instagram' in list_social :
				instagram = True
			else :
				instagram = False
			if 'line' in list_social :
				line = True
			else :
				line = False


			if 'japan' in list_fav :
				japan = True
			else :
				japan = False
			if 'shabu' in list_fav :
				shabu = True
			else :
				shabu = False
			if 'grill' in list_fav :
				grill = True
			else :
				grill = False
			if 'steak' in list_fav :
				steak = True
			else :
				steak = False
			if 'fastfood' in list_fav :
				fastfood = True
			else :
				fastfood = False
			if 'diet' in list_fav :
				diet = True
			else :
				diet = False
			if 'thai' in list_fav :
				thai = True
			else :
				thai = False
			if 'cake' in list_fav :
				cake = True
			else :
				cake = False
			if 'dessert' in list_fav :
				dessert = True
			else :
				dessert = False
			if 'juice' in list_fav :
				juice = True
			else :
				juice = False
			if 'coffee' in list_fav :
				coffee = True
			else :
				coffee = False


			print(age)
			obj, created = Informations.objects.update_or_create(
				user=request.user, defaults={'age': age,'birthdate':date(year=int(year), month=int(month), day=int(day)),
				'sex':gender,'salary':salary,'size':list_size,'breakfast':bf,'lunch':lunch,'dinner':dinner,'late':late,
				'taste':taste,'price':price,'service':service,'clean':clean,'at':at,'location':location,
				'thai':thai,'diet':diet,'shabu':shabu,'grill':grill,'steak':steak,'fastfood':fastfood,'cake':cake,
				'dessert':dessert,'coffee':coffee,'juice':juice,'facebook':facebook,'twitter':twitter,'instagram':instagram,'line':line},
			)

			# Informations.objects.create(user=request.user,age=age,birthdate=date(year=int(year), month=int(month), day=int(day)),
			# 	sex=gender,salary=salary,size=list_size,breakfast=bf,lunch=lunch,dinner=dinner,late=late,
			# 	taste=taste,price=price,price=service,clean=clean,at=at,location=location,
			# 	facebook=facebook,twitter=twitter,instagram=instagram,line=line,japanese=japan,
			# 	thai=thai,diet=diet,shabu=shabu,grill=grill,steak=steak,fastfood=fastfood,
			# 	cake=cake,dessert=dessert,coffee=coffee,juice=juice)


	
		except:
			raise

		
	
	return render(request, 'informations_complete.html')

def checkIsSell(request):
    # print("earn")
    if request.method == 'POST':
        user = request.user
        menu_id = request.POST.get('menu_id', None)
        isChecked = request.POST.get('isChecked', None)
        menu = get_object_or_404(Menu, id=menu_id)
        if isChecked == 'true':
        	isChecked=True
        elif isChecked == 'false':
        	isChecked=False
        	
        print(menu_id)
        print(menu)

        if isChecked:
            Menu.objects.filter(id=menu_id).update(isSell=isChecked)
        else:
            Menu.objects.filter(id=menu_id).update(isSell=isChecked)

    context = 'success'
    return HttpResponse(json.dumps(context), content_type='application/json')

def like_button(request):
    print("earn")
    if request.method == 'POST':
        user = request.user
        s_name = request.POST.get('pk', None)
        print(s_name)
        store = get_object_or_404(Store, name=s_name)
        print(store)

        if store.likes.filter(id=user.id).exists():
            store.likes.remove(user)
        else:
            store.likes.add(user)

    context = {'likes_count': store.total_likes}
    return HttpResponse(json.dumps(context), content_type='application/json')

