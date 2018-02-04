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
import datetime
from django.core import serializers
from datetime import  timedelta
from django.core.paginator import Paginator
# import calendar

def home(request):
	display_list = DisplayHome.objects.all()[:10]

	# out= []
	# mobile_out =[]
	rate = []
	profile_picture = []
	reviews_list = []
	desktop = []
	mobile = []
	item_list =[]
	# coupon_list= []
	for item in display_list:
		if item.coupon is None :
			if item.review is None :
				item_list = {'rating_color': 0 ,'rating_no_color': 0 ,'profile_picture':None,
				'type':'review','store':'','username':'','create_at' : None,'comment' : ''}
				temp = { 'rating_color': 0,'rating_no_color': 0, }
			else:
				item_list = {'rating_color': 0 ,'rating_no_color': 0 ,'profile_picture':None,
					'type':'review','store':'','username':'','create_at' : None,'comment' : ''}
				temp = { 'rating_color': 0,'rating_no_color': 0, }

				item_list['rating_color'] = item.review.rating
				item_list['rating_no_color'] = 5 - item_list['rating_color']
					# item_list['reiview'] = item.review
					# item_list['rate'] =temp
					# item_list['rate'] =temp
				item_list['store'] = item.review.store.name
				item_list['username'] = item.user.username
				item_list['create_at'] = item.review.created_at
				item_list['comment'] = item.review.comment


				item_list['profile_picture'] = Profile.objects.get(user=item.review.user).picture.url
					
		elif item.review is None :
			if item.coupon is None :
				item_list = {'rating_color': 0 ,'rating_no_color': 0 ,'profile_picture':None,
				'type':'review','store':'','username':'','create_at' : None,'comment' : ''}
				temp = { 'rating_color': 0,'rating_no_color': 0, }
		
			else:
				coupon = Coupon.objects.get(id=item.coupon.id)
				item_list = {'username':'','profile_picture': None,'coupon_msg' :'','store':''
				,'type':'coupon','create_at' : None}
				item_list['profile_picture'] = Profile.objects.get(user=item.user).picture.url
				item_list['coupon_msg'] = coupon.msg
				item_list['store'] = coupon.store.name
				item_list['username'] = item.user.username
				item_list['create_at'] = item.coupon.created_at
			# rate.append(temp)
			# reviews_list.append(item.review)
			# profile_picture.append(Profile.objects.get(user=item.review.user).picture.url)
			# out = zip(reviews_list,rate,profile_picture)
			# mobile_out= zip(reviews_list,rate,profile_picture)
			# except :
			# 	raise Http404

		desktop.append(item_list)
		mobile.append(item_list)



	response = set_cookie(request, 'home.html', {'desktop':desktop,'mobile':mobile})
	
	
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
				collect_session(request,"เพิ่มเมนู",create_menu.id)
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
	# collect_session(request,"รีวิวร้านค้า",review.id)
	today =datetime.date.today()
	today_name = today.strftime('%B')
	month = today.strftime('%B')
	year = today.strftime('%Y')
	store = StoreByUser.objects.get(user = request.user).store
	reviews_count = Review.objects.filter(store=store).count()
	order_count = Order.objects.filter(store=store).count()
	member_viewer = User_session.objects.filter(action="enter_store",value=store.id).count()
	anonymous_viewer =Anonymous_session.objects.filter(action="enter_store",value=store.id).count()
	viewer = member_viewer+anonymous_viewer

	# member_viewer_today =  User_session.objects.filter(created_at__gt=today).count()
	# anonymous_viewer_today = Anonymous_session.objects.filter(created_at__gt=today).count()
	# viewer_today= member_viewer_today+anonymous_viewer_today

	now = datetime.datetime.now()
	first_day_string = "2018-01-01"
	first_day = datetime.datetime.strptime(first_day_string, "%Y-%m-%d").date()

	print("now",now)
	# print(viewer_today)
	print("today",today)
	differ = datetime.date.today() - first_day
	print("differ",differ.days)
	viewer_list_per_day = []
	for i in reversed(range(differ.days)):
		member_viewer_yesterday = 0
		anonymous_viewer_yesterday =0
		viewer_yesterday =0
		print('',i+1)
		yesterday = datetime.date.today() - datetime.timedelta(days=i+1)
		member_viewer_yesterday =  User_session.objects.filter(action="enter_store",value=store.id,created_at__date=yesterday).count()
		anonymous_viewer_yesterday = Anonymous_session.objects.filter(action="enter_store",value=store.id,created_at__date=yesterday).count()
		print("member_viewer_yesterday ",member_viewer_yesterday)

		viewer_yesterday= int(anonymous_viewer_yesterday)+int(member_viewer_yesterday)
		viewer_list_per_day.append(viewer_yesterday)
	print("viewer_list_per_day",viewer_list_per_day)

	return render(request, 'report.html',{'month':month,'year':year,'store':store,
		'reviews_count':reviews_count,'order_count':order_count,
		'viewer':viewer,'viewer_list_per_day':json.dumps(viewer_list_per_day),'differ_dates':differ.days})

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
		# payment = request.GET.get('payment',False)
		# slip = request.GET.get('slip',False)
		total_price = request.GET.get('total_act',False)
		order = request.GET.get('data',False)
		order = json.loads(order)
		print(address)
		print(phone_number)
		# print(payment)
	
		menu_list = []
		amount_list = []

		for item in order :

			m = Menu.objects.get(store__id=item['store'],name=item['name'])
			menu_list.append(m.id)
			amount_list.append(item['amount'])
			s = Store.objects.get(id=item['store'])
		order = Order.objects.create(user=request.user,menu=menu_list,store=s,amount=amount_list,
			address =address,total=total_price,)
		# if (payment == "PromtPay"):
		# 	next_page = "upload-slip"
		# 	print(next_page)
		# 	return JsonResponse({'next_page':next_page,'order_id':order.id},safe=False)
		# 	# return HttpResponseRedirect(next_page)
		# else:
		# 	next_page = "success"
		next_page = "select-payment"
		return JsonResponse({'next_page':next_page,'order_id':order.id},safe=False)

@login_required
def payment(request,pk):
	
	try:
		slipForm = SlipPaymentForm()
		o = Order.objects.get(id=pk)
		order = Order.objects.filter(id=pk)
		total = o.total
		store=o.store
		if request.method == 'POST':
			slipForm = SlipPaymentForm(request.POST,request.FILES)
			if "byCash" in request.POST:
				print("Earn")
				slipForm.fields['slip_image'].required = False

			if slipForm.is_valid():
				if slipForm.cleaned_data['slip_image'] is None:
					order.update(payment="จ่ายเงินปลายทาง") 
				else:
					order.update(payment="พร้อมเพย์")
					o.slip_payment = request.FILES['slip_image']
					o.save()

				# print(slipForm.cleaned_data['slip_image'] )
				# print(request.FILES['slip_image'])	
				# o.slip_payment = request.FILES['slip_image']
				# o.save()
			
				next_page = "/success/"+str(pk)
				return HttpResponseRedirect(next_page)

		return render(request, 'payment.html', {'slipForm':slipForm,'store':store,'total':total})		
	
	except Order.DoesNotExist:
		raise
	
@login_required
def showSlip(request,pk):
	
	try:
		# slipForm = SlipPaymentForm()
		order = Order.objects.get(id=pk)
		image = order.slip_payment.url
		
		
	
		return render(request, 'slip.html', {'order':order,'image':image,})		
	
	except Order.DoesNotExist:
		raise
	

  

  


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
	time_status = 0
	delivery = False
	if "delivery" in store.tags :
		delivery = True

		try :
			time = DeliveryTime.objects.get(store=store)
			# print(calendar.day_name[date.today().weekday()])
			day = date.today().weekday()
			time_now = datetime.datetime.now().time()
			time_status = 0
			if day == 0 :# monday

				if time.monday :
					time_open = time.monday_open
					time_close = time.monday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
				
			elif day == 1 :# tuesday
				if time.tuesday :
					time_open = time.tuesday_open
					time_close = time.tuesday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0

			elif day == 2:	# wednesday
				if time.wednesday :
					time_open = time.wednesday_open
					time_close = time.wednesday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
			
			elif day == 3 :# thursday
				if time.thursday :
					time_open = time.thursday_open
					time_close = time.thursday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
				
			elif day == 4:# friday
				if time.friday :
					time_open = time.friday_open
					time_close = time.friday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
				
			elif day == 5 :# saturday
				if time.saturday :
					time_open = time.saturday_open
					time_close = time.saturday_close
					if time_open is None and time_close is None:
						time_status = 0
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
				
			elif day == 6:# sunday
				# print(time.sunday)
				if time.sunday :
					time_open = time.sunday_open
					time_close = time.sunday_close
					# print(time_close)
					# print(time_open)
					if time_open is None and time_close is None:
						time_status = 0
						# print(None)
					else :
						if time_now >= time_open and time_now <= time_close :
							time_status = 1
				else :
					time_status = 0
				# print()
		except :
			pass
			

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
				DisplayHome.objects.create(user=request.user,review=review)
				next_page = "/store/"+str(pk)
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
			delivery_charge = 0
			if(store.name == "กินอิ่มนอนอุ่น"):
				if(total < 150):
					delivery_charge = int(store.delivery_payment)

				else:
					delivery_charge = int(store.delivery_payment)
				total+=delivery_charge

			return  render(request,'checkout.html',{'username':request.user.username,'data':json.dumps(output),
				'output':output,'total':total,'delivery_address':delivery_address,
				'delivery_phone':delivery_phone,'store':store,'delivery_charge':delivery_charge})


	return render(request,'stores.html',{'reviewForm':reviewForm,'username':request.user.username,'menues':reversed(menues2),'mobile_menues':reversed(menues2),
		'reviews':reviews,'out':out,'store':store,'delivery':delivery,'category':cate,'store_loved_color':store_loved_color,'time_status':time_status})




# def searchBycate(request,cate):
# 	stores_list = []
# 	stores =[]
# 	store_love_list =[]

# 	collect_session(request,"search_cate",cate)
# 	try :
# 		if cate == "all":
# 			stores = Store.objects.all()
# 		else :
# 			stores = Store.objects.filter(tags__contains=cate)
# 		print("stores",stores)
		

# 		for s in stores :
# 			temp = {'name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
			
# 			# temp['name'].append(s.name)
# 			temp['name'] = s.name
# 			tags = s.tags.split(',')
# 			for tag in tags :
# 				temp['tags'].append(tag)

# 			try:
# 				rating_avg = Review.objects.filter(store__name = s.name).aggregate(Avg('rating'))
# 				temp['rating_color'] = round(rating_avg['rating__avg'])

# 			except:
# 				temp['rating_color'] = 0


# 			temp['rating_no_color'] = 5 - temp['rating_color']

# 			temp['no_reviews'] = Review.objects.filter(store__name=s.name).count()

# 			menues = Menu.objects.filter(store__name=s.name)[:4]
# 			for menu in menues:
# 				temp['menues'].append(menu)

# 			temp['love'] = s.total_likes
			
# 			if request.user.is_authenticated():
# 				user = request.user
# 				store = get_object_or_404(Store, name=s.name)
# 				if store.likes.filter(id=user.id).exists():
# 					temp['store_loved_color'] = True
# 				else:
# 					temp['store_loved_color'] = None
					
			
# 			stores_list.append(temp)

# 		print("============================")
# 		for i in stores_list:
# 			print (i)

# 	except Exception as e:
# 		raise Http404


# 	return render(request, 'search_cate.html',{'stores':stores_list,'category':cate,})


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
		
		page = request.GET.get('page', 1)

		for s in stores :
			temp = {'id':'','name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
			
			# temp['name'].append(s.name)
			temp['name'] = s.name
			temp['id'] = s.id
			tags = s.tags.split(',')
			for tag in tags :
				temp['tags'].append(tag)

			try:
				rating_avg = Review.objects.filter(store__id = s.id).aggregate(Avg('rating'))
				temp['rating_color'] = round(rating_avg['rating__avg'])

			except:
				temp['rating_color'] = 0


			temp['rating_no_color'] = 5 - temp['rating_color']

			temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()

			menues = Menu.objects.filter(store__id=s.id)[:4]
			for menu in menues:
				temp['menues'].append(menu)

			temp['love'] = s.total_likes
			
			if request.user.is_authenticated():
				user = request.user
				store = get_object_or_404(Store, id=s.id)
				if store.likes.filter(id=user.id).exists():
					temp['store_loved_color'] = True
				else:
					temp['store_loved_color'] = None
					
			
			stores_list.append(temp)

		print("============================")
		for i in stores_list:
			print (i)

		paginator = Paginator(stores_list, 10)
		try:
			stores = paginator.page(page)
		except PageNotAnInteger:
			stores = paginator.page(1)
		except EmptyPage:
			stores = paginator.page(paginator.num_pages)

	except Exception as e:
		raise 


	return render(request, 'search_cate.html',{'stores':stores,'category':cate,})





def searchAll(request):
	stores_list = []
	stores =[]
	store_love_list =[]
	cate = request.POST.get("search", "")

	collect_session(request,'search_input',cate)

	page = request.GET.get('page', 1)


	# collect_session(request,'search_input',cate)
	page = request.GET.get('page', 1)

	if request.method == 'POST':
		if request.POST.get('search') is None:
			return  HttpResponseRedirect('home')
		else:
			print("ddd",request.POST.get('search'))	

		
	

	try :
		# stores = Store.objects.filter(tags__contains=cate)

		stores= Store.objects.annotate(search=SearchVector('tags', 'name')).filter(search__contains=cate)

		for s in stores :
			temp = {'id':'','name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
			temp['name'] = s.name
			temp['id'] = s.id

			tags = s.tags.split(',')
			for tag in tags :
				temp['tags'].append(tag)

			try:
				rating_avg = Review.objects.filter(store__id = s.id).aggregate(Avg('rating'))
				temp['rating_color'] = round(rating_avg['rating__avg'])

			except:
				temp['rating_color'] = 0


			temp['rating_no_color'] = 5 - temp['rating_color']

			temp['no_reviews'] = Review.objects.filter(store__id=s.id).count()

			menues = Menu.objects.filter(store__id=s.id)[:4]
			for menu in menues:
				temp['menues'].append(menu)

			temp['love'] = s.total_likes
			
			if request.user.is_authenticated():
				user = request.user
				store = get_object_or_404(Store, id=s.id)
				if store.likes.filter(id=user.id).exists():
					temp['store_loved_color'] = True
				else:
					temp['store_loved_color'] = None

			stores_list.append(temp)


		paginator = Paginator(stores_list, 10)
		try:
			stores = paginator.page(page)
		except PageNotAnInteger:
			stores = paginator.page(1)
		except EmptyPage:
			stores = paginator.page(paginator.num_pages)

	except :
		raise


	return render(request, 'search_input.html',{'stores':stores,'category':cate})

# def searchAll(request):
# 	stores_list = []
# 	stores =[]
# 	store_love_list =[]
# 	cate = request.POST.get("search", "")

# 	collect_session(request,'search_input',cate)
# 	# collect_session(request,'search_input',cate)

# 	if request.method == 'POST':
# 		if request.POST.get('search') is None:
# 			return  HttpResponseRedirect('/main/')
# 		else:
# 			print("ddd",request.POST.get('search'))	

		


# 	try :
# 		# stores = Store.objects.filter(tags__contains=cate)

# 		stores= Store.objects.annotate(search=SearchVector('tags', 'name')).filter(search__contains=cate)

# 		for s in stores :
# 			temp = {'name': '', 'tags' : [], 'rating_color': 0,'rating_no_color': 0, 'no_reviews':0,'menues' : [],'love':0,'store_loved_color':[]}
# 			temp['name'] = s.name

# 			tags = s.tags.split(',')
# 			for tag in tags :
# 				temp['tags'].append(tag)

# 			try:
# 				rating_avg = Review.objects.filter(store__name = s.name).aggregate(Avg('rating'))
# 				temp['rating_color'] = round(rating_avg['rating__avg'])

# 			except:
# 				temp['rating_color'] = 0


# 			temp['rating_no_color'] = 5 - temp['rating_color']

# 			temp['no_reviews'] = Review.objects.filter(store__name=s.name).count()

# 			menues = Menu.objects.filter(store__name=s.name)[:4]
# 			for menu in menues:
# 				temp['menues'].append(menu)

# 			temp['love'] = s.total_likes
			
# 			if request.user.is_authenticated():
# 				user = request.user
# 				store = get_object_or_404(Store, name=s.name)
# 				if store.likes.filter(id=user.id).exists():
# 					temp['store_loved_color'] = True
# 				else:
# 					temp['store_loved_color'] = None

# 			stores_list.append(temp)



# 	except :
# 		raise


# 	return render(request, 'search_input.html',{'stores':stores_list,'category':cate})


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


			obj, created = Informations.objects.update_or_create(
				user=request.user, defaults={'age': age,'birthdate':date(year=int(year), month=int(month), day=int(day)),
				'sex':gender,'salary':salary,'size':list_size,'breakfast':bf,'lunch':lunch,'dinner':dinner,'late':late,
				'taste':taste,'price':price,'service':service,'clean':clean,'at':at,'location':location,
				'thai':thai,'diet':diet,'shabu':shabu,'grill':grill,'steak':steak,'fastfood':fastfood,'cake':cake,
				'dessert':dessert,'coffee':coffee,'juice':juice,'facebook':facebook,'twitter':twitter,'instagram':instagram,'line':line},
			)

			if created :
				try:
					c = Coupon.objects.all()
					for i in c :
						GetCoupon.objects.create(user=request.user,coupon=i,amount=i.amount)
				except Exception as e:
					raise

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
        sid = request.POST.get('pk', None)
        print(sid)
        store = get_object_or_404(Store, id=int(sid))
        print(store)

        if store.likes.filter(id=user.id).exists():
            store.likes.remove(user)
        else:
            store.likes.add(user)
        collect_session(request,'กด like ',store)
    context = {'likes_count': store.total_likes}
    return HttpResponse(json.dumps(context), content_type='application/json')
@login_required
def use_coupon(request,coupon):
	try :
		print(coupon)
		c = GetCoupon.objects.get(coupon__id=coupon,user=request.user)

		c.amount -= 1
		c.save()

		cou = Coupon.objects.get(id=coupon)
		DisplayHome.objects.create(user=request.user,coupon=cou)

		collect_session(request,'ใช้คูปอง',coupon)
		
		time = datetime.datetime.now()
		add_time = time + datetime.timedelta(0,3600)

		success_coupon = {'name':cou.store.name,'msg':cou.msg,'image':cou.image,'time':add_time}
	
		return render(request, 'use_coupon.html',{'coupon':success_coupon})
	except : 	
		raise

@login_required
def use_code(request):
	if request.is_ajax():
		try:
			code = request.GET.get('code',False)
			coupon = Coupon.objects.get(code=code)
			c = CodeType.objects.get(coupon=coupon)
			if c.code_type == 'ส่วนลด':
				code_type = 0
				msg = 'ส่วนลด'
				value = int(c.value)
			elif c.code_type == 'แถม' :
				code_type = 1
				msg = 'รับฟรี'
				value = c.value
			collect_session(request,'ใช้โค้ด',coupon.id)
		
		except Exception as e:
			raise


		print(code)
		return JsonResponse({'code':code_type,'value':value,'msg':msg},safe=False)

@login_required
def edit_delivery(request):
	s = StoreByUser.objects.get(user=request.user)
	t= DeliveryTime.objects.get(store=s.store)

	# time = {'m': t.monday_off,'tu':t.tuesday_off,'w': t.wednesday_off,'th': t.thursday_close,
	# 'f':t.friday_off,'sa':t.saturday_off,'su':t.sunday_off}
	time = [t.monday,t.tuesday,t.wednesday,t.thursday_close,t.friday,t.saturday,t.sunday]
	day = ['วันจันทร์','วันอังคาร','วันพุธ','วันพฤหัสบดี','วันศุกร์','วันเสาร์','วันอาทิตย์']
	index =  [0,1,2,3,4,5,6,]
	list_time = zip(time,day,index)
	return render(request, 'delivery_close.html',{'time':list_time})



def home_tohrung(request):
	return render(request, 'midnight.html',{})


def changeDelivery(request):
	if request.method == 'POST':
		user = request.user
		index = request.POST.get('index', None)
		isChecked = request.POST.get('isChecked', None)
		if isChecked == 'true':
			checked=True
		elif isChecked == 'false':
			checked=False

		print(checked)
		index = int(index)
		s = StoreByUser.objects.get(user=request.user)
		print(s.store.name)
		if index == 0 :
			DeliveryTime.objects.filter(store=s.store).update(monday=checked)
		elif index == 1 :
			DeliveryTime.objects.filter(store=s.store).update(tuesday=checked)
		elif index == 2 :
			DeliveryTime.objects.filter(store=s.store).update(wednesday=checked)
		elif index == 3 :
			DeliveryTime.objects.filter(store=s.store).update(thursday=checked)
		elif index == 4 :
			DeliveryTime.objects.filter(store=s.store).update(friday=checked)
		elif index == 5 :
			DeliveryTime.objects.filter(store=s.store).update(saturday=checked)
		elif index == 6 :
			print("55555555")
			DeliveryTime.objects.filter(store=s.store).update(sunday=checked)
	

		context = 'success'
	return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def update_status(request):
	order = Order.objects.all().order_by('-id')

	order_list = []

	for i in order :
		temp = {'id':0,'name':"",'menu_amount':[],'total':0,'status':""}
		temp['id'] = i.id
		temp['name'] = i.store.name
		temp['total'] = i.total
		temp['status'] = i.status
		for m,a in zip(i.menu,i.amount):

			# ma = {'menu':None,'amount':""}
			ma = {'menu':Menu.objects.get(id=m),'amount':a}
			temp['menu_amount'].append(ma)
	#         #             menu_list.append(Menu.objects.get(id=m))
	#         #             amount_list.append(a)

		order_list.append(temp)


	return render(request, 'update_status.html',{'order_list':order_list})


@login_required
def change_status(request):

	if request.method == 'POST':
		status = int(request.POST.get('status', None))
		order_id = int(request.POST.get('order_id', None))
		
		s = "รับออเดอร์"
		print(order_id)
		print(status)
		if status == 0 :
			s = "รับออเดอร์"
			print(s)

		elif status == 1:	
			s = "กำลังทำอาหาร"
			print(s)

		elif status == 2 :
			s = "กำลังส่ง"
			print(s)


		
		# print(s)
		Order.objects.filter(id=order_id).update(status=s)



	return JsonResponse({},safe=False)
