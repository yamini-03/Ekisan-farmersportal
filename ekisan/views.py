from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render
import pyrebase
import random
import string
import json
import urllib.request

from django.shortcuts import redirect

from datetime import date
import razorpay
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse

firebaseConfig = {
    'apiKey': "AIzaSyDztSthRiZSB6XTlhhD_i-8KT8RJ3DyM3Y",
    'authDomain': "efarming-7d78e.firebaseapp.com",
    'databaseURL': "https://efarming-7d78e-default-rtdb.firebaseio.com/",
    'projectId': "efarming-7d78e",
    'storageBucket': "efarming-7d78e.appspot.com",
    'messagingSenderId': "790177229471",
    'appId': "1:790177229471:web:6c118d22fb64cd8d6010aa"
  }
firebase1 = pyrebase.initialize_app(firebaseConfig)
authe = firebase1.auth()
database = firebase1.database()

role = "con"
def about(request):
    return render(request,'About-us.html')


def index(request):
    global curuser
    curuser = authe.current_user
    return render(request, 'index.html',{'cur':curuser})


def logout(request):
    try:
        auth.logout(request)
        authe.current_user = None
        return render(request, "index.html")
    except:
        return render(request, "crop.html")

def output(request):
    return redirect('http://localhost:3000/')


def Csignup(request):
    lettersU = string.ascii_uppercase
    lettersD = string.digits
    id = (''.join(random.choice(lettersD) for i in range(3)) + ''.join(random.choice(lettersU) for i in range(1)))
    id1 = 'EK'+id
    name = request.POST.get('name')
    email = request.POST.get('email')
    contactno = request.POST.get('contact')
    address = request.POST.get('address')
    city = request.POST.get('city')
    pin = request.POST.get('pin')
    passw = request.POST.get('pass')

    try:
        user = authe.create_user_with_email_and_password(email, passw)
        mess = 'user created successfully'
        
        Uid = user['localId']
        data = {
            'Name': name,
            'Email': email,
            'Mobile_No': contactno,
            'Address': address,
            'City': city,
            'Pin code': pin,
            'Cid': id1,
            'Password': passw,
        }
        database.child('Consumer').child('Details').child(Uid).set(data)
        return render(request, "index.html",{'cur':user})
    except:
        mess = 'Failed to create Account!!'
       
        return render(request, "index.html")

def Clogin(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    global role
    
    role = 'con'
    try:
        user = authe.sign_in_with_email_and_password(email, password)

        id = database.child('Added_Items').shallow().get().val()
        lis_id = []
        for i in id:
            lis_id.append(i)

        details = {}
        farm = {}
        city = {}
        for i in lis_id:
            det = database.child('Added_Items').child(i).get().val()
            farmid = database.child('Added_Items').child(i).child('farmid').get().val()
            c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
           
            diction = dict(det)
            details[i] = diction
            city[i] = c
           
        details2 = {
            'det': details,
            'uid': lis_id,
            'city': city,
        }
        # return redirect('/displaycart/')
        return render(request, 'index.html',{'cur':user})
    except:
        message = "invalid credentials"
        return render(request, "index.html", {'mess': message})



def farmsignUp(request):
    lettersU = string.ascii_uppercase
    lettersD = string.digits
    id = (''.join(random.choice(lettersD) for i in range(3)) + ''.join(random.choice(lettersU) for i in range(1)))
    id1 = 'EK'+id
    name = request.POST.get('name')
    email = request.POST.get('email')
    adhar = request.POST.get('adhar')
    address = request.POST.get('address')
    city = request.POST.get('city')
    contact = request.POST.get('contact')
    pin = request.POST.get('pin')
    passw = request.POST.get('pass')
    passek = str('ek'+passw)
    try:
        user = authe.create_user_with_email_and_password(email, passek)
        mess = 'user created successfully'
        
        Uid = user['localId']
        data = {
            'Name': name,
            'Email': email,
            'Mobile_No': contact,
            'Adhar_No': adhar,
            'Address': address,
            'Pin code': pin,
            'Fid': id1,
            'Password': passw,
            'City': city,
        }
        database.child('Farmer').child('Details').child(Uid).set(data)
        return render(request, 'index.html', {'mess': mess,'cur':user})
    except:
        mess = 'Failed to create Account!!'
    
        return render(request, "index.html", {'mess': mess})

def fsignin(request):
    global role
    email = request.POST.get('email')
    PW = request.POST.get('pass')
    PWek = str('ek'+PW)

    methodpost = request.POST.get('mainlogin')
    methodpost1 = request.POST.get('innerlogin')

    if methodpost1:
        
        role = request.POST.get('RoleName')
        try:
            user = authe.sign_in_with_email_and_password(email, PWek)
            curuser = authe.current_user
            
            farmid = curuser['localId']

            try:
                proid = database.child('Added_Items').shallow().get().val()
                products = []
                for i in proid:
                    products.append(i)
                

                details = {}
                p = 0
                for i in products:
                    det = database.child('Added_Items').child(i).get().val()
                    if det['farmid'] == farmid:
                        diction = dict(det)
                      
                        diction['proid']=i
                        details[p] = diction
                        p += 1
                        
                animalid = database.child('Animals Info').child(farmid).shallow().get().val()
                animalsinfo = []
                for i in animalid:
                    animalsinfo.append(i)

                anidetails = {}
                p = 0
                for i in animalsinfo:
                    det = database.child('Animals Info').child(farmid).child(i).get().val()
                    diction = dict(det)
                    diction['animalid'] = i
                    anidetails[p] = diction
                    p += 1

                logid = database.child('Logs Info').child(farmid).shallow().get().val()
                loginfo = []
                for i in logid:
                    loginfo.append(i)

                logdetails = {}
                p = 0
                for i in loginfo:
                    det = database.child('Logs Info').child(farmid).child(i).get().val()
                    diction = dict(det)
                    diction['logid'] = i
                    logdetails[i] = diction
                    p += 1

                ucid = database.child('Upcoming task').child(farmid).shallow().get().val()
                upcomeinfo = []
                for i in ucid:
                    upcomeinfo.append(i)

                upcometaskdetails = {}
                for i in upcomeinfo:
                    det = database.child('Upcoming task').child(farmid).child(i).get().val()
                    diction = dict(det)
                    upcometaskdetails = diction


                details2 = {
                    'det': details,
                    'anidet': anidetails,
                    'logdet': logdetails,
                    'taskdet': upcometaskdetails
                }
                if role == 'far':
                    return render(request, "AddItem1.html", details2)
                else:
                    return render(request, "index.html",{'cur':user})
            except:
                return render(request, "index.html")
        except:
            mes = "Invalid Credentials"
            
            return render(request, "index.html", {'mess': mes})

    elif methodpost:
        
        role = request.POST.get('RoleName')
        try:
            user = authe.sign_in_with_email_and_password(email, PWek)
            
            curuser = authe.current_user
            farmid = curuser['localId']
            # session_id = user['localId']
            # request.session['uid'] = str(session_id)
            mes = "You are Loged in"
            return render(request, "index.html", {'mess': mes,'cur':user})
        except:
            mes = "Invalid Credentials"
            
            return render(request, "index.html", {'mess': mes})


def farmer(request):
    curuser = authe.current_user
    if curuser:
        additem = request.POST.get('additem')
        animal = request.POST.get('anisave')
        log = request.POST.get('logsave')
        farmid = curuser['localId']
        if additem:
            lettersD = string.digits
            oid = (''.join(random.choice(lettersD) for i in range(3)))
            vname = request.POST.get('Item Name')
            vprice = request.POST.get('price')
            vquant = request.POST.get('Quantity')
            url = request.POST.get('url')
            proid = vname[0:3] + oid
            c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
            fn = database.child('Farmer').child('Details').child(farmid).child('Name').get().val()

            productdata = {
                'Product_name': vname,
                'Price': vprice,
                'Quantity': vquant,
                'farmid': farmid,
                'url': url,
                'city': c,
                'fname': fn
            }
            database.child('Added_Items').child(proid).set(productdata)

        elif animal:
            animalname = request.POST.get('aniname')
            breed = request.POST.get('breed')
            count = request.POST.get('count')
            belowweight = request.POST.get('beweight')
            aboveweight = request.POST.get('abweight')

            aniuid = (animalname[0:3].join(random.choice(string.ascii_uppercase) for i in range(3)) +
                      ''.join(random.choice(string.digits) for i in range(2)))

            data = {
                'AnimalName': animalname,
                'Breed': breed,
                'Count': count,
                'Below_Weight_animals': belowweight,
                'Above_weight_animals': aboveweight
            }
            database.child('Animals Info').child(farmid).child(aniuid).set(data)

        elif log:
            logname = request.POST.get('cname')
            variety = request.POST.get('variety')
            season = request.POST.get('season')
            description = request.POST.get('description')

            loguid = (logname[0:3].join(random.choice(string.ascii_uppercase) for i in range(3)) +
                      ''.join(random.choice(string.digits) for i in range(2)))

            soil = 'dd/mm/yyyy'
            sow = 'dd/mm/yyyy'
            manu = 'dd/mm/yyyy'
            irr = 'dd/mm/yyyy'
            weed = 'dd/mm/yyyy'
            harvest = 'dd/mm/yyyy'
            store = 'dd/mm/yyyy'


            data = {
                'Logname': logname,
                'Variety': variety,
                'Season': season,
                'Description': description,
                'Soil_Preparation': soil,
                'Sowing': sow,
                'Manfacturing': manu,
                'Irrigation': irr,
                'Weeding': weed,
                'Harvesting': harvest,
                'Storage': store,

            }
            database.child('Logs Info').child(farmid).child(loguid).set(data)

        loguid = request.GET.get('id')
        soilprep = request.POST.get('soilprep')
        sowing = request.POST.get("sowing")
        manuring = request.POST.get('manufacturing')
        irrigation = request.POST.get('irrigation')
        weeding = request.POST.get('weeding')
        harvesting = request.POST.get('harvesting')
        storage = request.POST.get('storage')

        cropname= request.GET.get('cropname')
        from datetime import date
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        comingtask={}

        lettersD = string.digits
        prblmid = (''.join(random.choice(lettersD) for i in range(3)))

        if soilprep:
            soil = request.POST.get('soil')
            info = {'Soil_Preparation': soil}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if soil >= d1:
                task = {
                    'crop': cropname,
                    'logname': 'Soil Preparation',
                    "date": soil,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)

        elif sowing:
            sow = request.POST.get('sow')
            info = {'Sowing': sow}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if sow >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Sowing',
                    "date": sow,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)

        elif manuring:
            manu = request.POST.get('manure')
            info = {'Manfacturing': manu}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if manu >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Manfacturing',
                    "date": manu,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)
        elif irrigation:
            irr = request.POST.get('irrigate')
            info = {'Irrigation': irr}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if irr >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Irrigation',
                    "date": irr,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)
        elif weeding:
            weed = request.POST.get('weed')
            info = {'Weeding': weed}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if weed >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Weeding',
                    "date": weed,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)
        elif harvesting:
            harvest = request.POST.get('harvest')
            info = {'Harvesting': harvest}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if harvest >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Harvesting',
                    "date": harvest,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)
        elif storage:
            store = request.POST.get('store')
            info = {'Storage': store}
            database.child('Logs Info').child(farmid).child(loguid).update(info)
            if store >= d1:
                task = {
                    'crop' : cropname,
                    'logname' : 'Storing',
                    "date": store,
                }
                database.child('Upcoming task').child(farmid).child(loguid).child(prblmid).set(task)


        proid = database.child('Added_Items').shallow().get().val()
        products = []
        for i in proid:
            products.append(i)

        details = {}
        p = 0
        for i in products:
            det = database.child('Added_Items').child(i).get().val()

            if det['farmid'] == farmid:
                diction = dict(det)
                diction['proid'] = i
                details[p] = diction
                p += 1

        animalid = database.child('Animals Info').child(farmid).shallow().get().val()
        animalsinfo = []
        for i in animalid:
            animalsinfo.append(i)

        anidetails = {}
        p = 0
        for i in animalsinfo:
            det = database.child('Animals Info').child(farmid).child(i).get().val()
            diction = dict(det)
            diction['animalid'] = i
            anidetails[p] = diction
            p += 1

        logid = database.child('Logs Info').child(farmid).shallow().get().val()
        loginfo = []
        for i in logid:
            loginfo.append(i)

        logdetails = {}
        p = 0
        for i in loginfo:
            det = database.child('Logs Info').child(farmid).child(i).get().val()
            diction = dict(det)
            diction['logid'] = i
            logdetails[i] = diction
            p += 1

        ucid = database.child('Upcoming task').child(farmid).shallow().get().val()
        upcomeinfo = []
        for i in ucid:
            upcomeinfo.append(i)

        upcometaskdetails = {}
        for i in upcomeinfo:
            det = database.child('Upcoming task').child(farmid).child(i).get().val()
            diction = dict(det)
            upcometaskdetails = diction


        details2 = {
            'det': details,
            'anidet': anidetails,
            'logdet': logdetails,
            'taskdet': upcometaskdetails
        }

        return render(request,'AddItem1.html',details2)
    else:
        return render(request, 'farmlogin.html')


def buying(request):

    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)
    details = {}
    city = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        farmid = database.child('Added_Items').child(i).child('farmid').get().val()
        c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
        
        diction = dict(det)
        details[i] = diction
        city[i] = c
    details2 = {
        'det': details,
        'uid': lis_id,
        'city': city,
    }
    return render(request, 'buying.html', details2)


def apples(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Apple'):
            diction = dict(det)
            details[i] = diction

    details2 = {
        'det': details,
        'uid': lis_id
    }
    return render(request, 'buying.html', details2)


def bellpeper(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Bell peper'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def carrot(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Carrot'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def cauliflower(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Cauliflower'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def cucumber(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Cucumber'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def peas(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Peas'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def potato(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Potato'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def tomato(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Tomato'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def rice(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Rice'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)


def wheat(request):
    id = database.child('Added_Items').shallow().get().val()
    lis_id = []
    for i in id:
        lis_id.append(i)

     
    details = {}
    for i in lis_id:
        det = database.child('Added_Items').child(i).get().val()
        if (det['Product_name'] == 'Wheat'):
            diction = dict(det)
            details[i] = diction
     
    details2 = {
        'det': details,
        'uid': lis_id
    }
     
    return render(request, 'buying.html', details2)

def mainpro(request):
    uid = request.GET.get('z')

    proname = database.child('Added_Items').child(uid).child('Product_name').get().val()
    amount = database.child('Added_Items').child(uid).child('Price').get().val()
    quantity = database.child('Added_Items').child(uid).child('Quantity').get().val()
    url = database.child('Added_Items').child(uid).child('url').get().val()
    fname = database.child('Added_Items').child(uid).child('fname').get().val()

    return render(request,'product.html',{ 'proname': proname,'amount': amount,'quantity': quantity, 'url': url, 'fname': fname, 'uid':uid})

def addtocart(request):

    curuser = authe.current_user
    if curuser and role == 'con':
        cid = curuser['localId']
        uid = request.GET.get('z')
        reqquant = request.POST.get('req')

        proname = database.child('Added_Items').child(uid).child('Product_name').get().val()
        amount = database.child('Added_Items').child(uid).child('Price').get().val()
        quantity = database.child('Added_Items').child(uid).child('Quantity').get().val()
        url = database.child('Added_Items').child(uid).child('url').get().val()
        fname = database.child('Added_Items').child(uid).child('fname').get().val()
        fid = database.child('Added_Items').child(uid).child('farmid').get().val()

        productdata = {
            'Productname': proname,
            'Price': amount,
            'Requiredquantity':  reqquant,
            'url': url,
            'fid':fid,
            'totalprice': int(amount) * int(reqquant),

        }
        database.child('Cart').child(cid).child(uid).set(productdata)

        # return render(request, 'product.html',{'proname': proname, 'amount': amount,  'quantity': quantity,
        #                                        'url': url, 'fname': fname,'uid': uid})
        return render(request, 'product.html', {'proname': proname, 'amount': amount, 'quantity': quantity,
                                                'url': url, 'fname': fname,'fid': fid, 'uid': uid})
    else:
        mess = "You need to login"
        return render(request,'consumerlogin.html',{'mess':mess})


def displaycart(request):
    curuser = authe.current_user
    if curuser:
        cid = curuser['localId']
        try:
            sub = request.POST.get('minus')
            addq = request.POST.get('plus')
            id = request.GET.get('proid')
            if sub:
                qunatity = database.child('Cart').child(cid).child(id).child('Requiredquantity').get().val()
                itemprice = database.child('Cart').child(cid).child(id).child('Price').get().val()
                newq = int(qunatity) - 1
                if newq <= 0:
                    newq = 1
                else:
                    tp = int(itemprice) * int(newq)
                    up = {
                        'Requiredquantity': newq,
                        'totalprice': tp
                    }
                    database.child('Cart').child(cid).child(id).update(up)
            elif addq:
                qunatity = database.child('Cart').child(cid).child(id).child('Requiredquantity').get().val()
                newq = int(qunatity) + 1
                itemprice = database.child('Cart').child(cid).child(id).child('Price').get().val()
                tp = int(itemprice) * int(newq)
                up = {
                    'Requiredquantity': newq,
                    'totalprice': tp
                }
                database.child('Cart').child(cid).child(id).update(up)

            proid = database.child('Cart').child(cid).shallow().get().val()
            products = []
            for i in proid:
                products.append(i)
            details = {}
            totamt = []
            maxquant = {}
            sum = 0
            sum1 = 0

            for i in products:
                tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
                sum = sum + tamount
                det = database.child('Cart').child(cid).child(i).get().val()
                maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

                maxquant[i] = maxquantallow
                
                diction = dict(det)
                details[i] = diction
            sum1 = sum + 20

            add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
            city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
            pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

            details2 = {
                'det': details,
                'uid': products,
                'sum': sum,
                'sum1': sum1,
                'add': add,
                'city': city,
                'pin': pin,
                'mq': maxquant,
            }
            print(details2)
            return render(request, 'cart.html', details2)
        except:
            return render(request, 'nocart.html')
    else:
        mess = "You need to login"
        return render(request, 'consumerlogin.html', {'mess': mess})


def consumerlogin(request):
    return render(request, 'consumerlogin.html')


def myorders(request):
    curuser = authe.current_user
    if curuser:
        cid = curuser['localId']
        try:
            orderid = database.child('orderplaced').child(cid).shallow().get().val()
            orders = []
            products = []
            for i in orderid:
                orders.append(i)
                proid = database.child('orderplaced').child(cid).child(i).shallow().get().val()
                for j in proid:
                    products.append(j)
            details = {}
            past = request.POST.get('past')
            present = request.POST.get('present')
            delstat = 'notdelivered'
            page = 'Past Orders'
            if past:
                delstat = 'delivered'
                page = 'Past Orders'
            elif present:
                delstat = 'notdelivered'
                page = 'Ongoing Orders'
            for j in orderid:
                for i in products:
                    delstatus = database.child('orderplaced').child(cid).child(j).child(i).child('Deliverystatus').get().val()
                    if delstatus == delstat:
                        proname = database.child('orderplaced').child(cid).child(j).child(i).child('Product_name').get().val()
                        quant = database.child('orderplaced').child(cid).child(j).child(i).child('Required_quant').get().val()
                        price = database.child('Added_Items').child(i).child('Price').get().val()
                        url = database.child('Added_Items').child(i).child('url').get().val()
                        totalP = int(quant) * int(price)
                        diction = {
                            'proname':proname,
                            'quant':quant,
                            'price':price,
                            'totalprice':totalP,
                            'url':url,
                            'pagename':page,
                        }
                        details[i] = diction
                details2 = {
                    'det': details,
                }
            return render(request, 'myorders.html', details2)
        except:
            return HttpResponse("No orders till now")
    else:
        mess = "You need to login"
        return render(request, 'consumerlogin.html', {'mess': mess})


def razor(request):
    curuser = authe.current_user
    if request.method == 'POST':
        curuser = authe.current_user
        cid = curuser['localId']
        amount1 = int(request.GET.get('e'))* 100
        client = razorpay.Client(auth=('rzp_test_ssmxVx39H1TlGF','Gtc2eutjvAiD3P0MSE51KkJ1'))
        rep = ('EK'.join(random.choice(string.ascii_uppercase) for i in range(3)) + ''.join(random.choice(string.digits) for i in range(2)))
        orderinfo = client.order.create(dict (amount=amount1, currency="INR", receipt=rep))
        odid = orderinfo['id']
        amm = orderinfo['amount']

        proid = database.child('Cart').child(cid).shallow().get().val()
        products = []
        for i in proid:
            products.append(i)
        details = {}
        maxquant = {}
        sum = 0

        for i in products:
            tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
            sum = sum + tamount
            det = database.child('Cart').child(cid).child(i).get().val()
            maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()

            # diction1 = dict(maxquantallow)
            maxquant[i] = maxquantallow

            # farmid = database.child('Cart').child(i).child('farmid').get().val()
            # c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()

            diction = dict(det)
            # diction['maxquant']=maxquantallow
            details[i] = diction
        sum1 = sum + 20

        add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
        city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
        pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

        details2 = {
            'det': details,
            'uid': products,
            'sum': sum,
            'sum1': sum1,
            'add': add,
            'city': city,
            'pin': pin,
            'mq': maxquant,
            'orderinfo': orderinfo,
            'odid':odid,
            'amm': amm,
        }
        #  details2)
        return render(request,'confrimorder.html', details2)
    else:
        return render(request, 'index.html',{'cur':curuser})



@csrf_exempt
def success(request):
    global orderid, amount, orderid, amount
    from datetime import date
    today = date.today()
    # d1 = today.strftime("%d/%m/%Y")
    d1 = today.strftime("%Y-%m-%d")
    orderid = request.GET.get('oid')
    amount = request.GET.get('amm')

    curuser = authe.current_user
    cid = curuser['localId']

    name = database.child('Consumer').child('Details').child(cid).child('Name').get().val()
    add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
    city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
    pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()
    emailid = database.child('Consumer').child('Details').child(cid).child('Email').get().val()

    address = str(add) +"  "+ str(city) +"  "+ str(pin)


    proid = database.child('Cart').child(cid).shallow().get().val()
    products = []
    for i in proid:
        products.append(i)
    details = {}
    sum = 0

    for i in products:
        tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
        sum = sum + tamount
        det = database.child('Cart').child(cid).child(i).get().val()
        diction = dict(det)
        details[i] = diction
        details2 = {
            'Caddress':address,
            'Product_name': diction['Productname'],
            'Required_quant': diction['Requiredquantity'],
            'farmer_id': diction['fid'],
            'OrderDate': d1,
            'Pickup_date': 'None',
            'Pickup_status': 'notpicked',
            'Deliverystatus': 'notdelivered',
        }
        database.child('orderplaced').child(cid).child(orderid).child(i).set(details2)
    sum1 = sum + 20
    info = {
            "title": 'Order Confrimation',
            "orderid": orderid,
            "amount": amount,
            "date": d1,
            "name":name,
            "address":address,
            'sum': sum,
            'sum1': sum1,
            "det": details,
        }
    html_content = render_to_string("emailtemp.html", info)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'Order Confrimation',
        text_content,
        settings.EMAIL_HOST_USER,
        [emailid],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    database.child('Cart').child(cid).remove()
    return render(request, 'thank.html')


def removefromcart(request):

    curuser = authe.current_user
    cid = curuser['localId']
    uid = request.GET.get('z')
    database.child('Cart').child(cid).child(uid).remove()
    try:
        proid = database.child('Cart').child(cid).shallow().get().val()
        products = []
        for i in proid:
            products.append(i)
        details = {}
        totamt = []
        maxquant = {}
        sum = 0
        sum1 = 0
        # p = 0
        #  'maxquant', maxquant)
        for i in products:
            tamount = database.child('Cart').child(cid).child(i).child('totalprice').get().val()
            sum = sum + tamount
            det = database.child('Cart').child(cid).child(i).get().val()
            maxquantallow = database.child('Added_Items').child(i).child('Quantity').get().val()
             
            # diction1 = dict(maxquantallow)
            maxquant[i] = maxquantallow

            # farmid = database.child('Cart').child(i).child('farmid').get().val()
            # c = database.child('Farmer').child('Details').child(farmid).child('City').get().val()
            
            
            diction = dict(det)
            # diction['maxquant']=maxquantallow
            details[i] = diction
        sum1 = sum + 30

        add = database.child('Consumer').child('Details').child(cid).child('Address').get().val()
        city = database.child('Consumer').child('Details').child(cid).child('City').get().val()
        pin = database.child('Consumer').child('Details').child(cid).child('Pin code').get().val()

        details2 = {
            'det': details,
            'uid': products,
            'sum': sum,
            'sum1': sum1,
            'add': add,
            'city': city,
            'pin': pin,
            'mq': maxquant,
        }

        
        return render(request, 'cart.html', details2)
    except:
        return render(request, 'nocart.html')



def crop(request):
    return render(request, 'crop.html')


def seedfert(request):
    return render(request, 'seedferti.html')


def risk(request):
    return render(request, 'risk.html')


def risk2(request):
    return render(request, 'risk2.html')


def risk3(request):
    return render(request, 'risk3.html')


def risk4(request):
    return render(request, 'risk4.html')


def animal(request):
    return render(request, 'animal.html')


def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        country_code = 'IN'
        res = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c0b333162fb26b377e6962d7dae5e7b4').read()
        json_data = json.loads(res)
        
        data = {
            "country_code": str(json_data['weather'][0]['main']),
            "icon": str(json_data['weather'][0]['icon']),
            "longitude": str(json_data['coord']['lon']),
            "latitude": str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp']) + 'k',
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
            "wind": str(json_data['wind']['speed']) + 'km/h',
        }




    else:
        city = ''
        data = {}
    return render(request, 'weather.html', {'city': city, 'data': data})



def pickup(request):
    global data1, lis_id1
    detailsorder = {}
    curuser = authe.current_user
    cid = curuser['localId']
    data = database.child('orderplaced').shallow().get().val()
    lis_id = []
    lis_id1 = []
    lis_id2 = []
    p = 0
    for j in data:
        lis_id.append(j)
        data2 = database.child('orderplaced').child(j).shallow().get().val()
        for k in data2:
            lis_id2.append(k)
            data1 = database.child('orderplaced').child(j).child(k).shallow().get().val()
            for i in data1:
                lis_id1.append(i)
                det = database.child('orderplaced').child(j).child(k).child(i).get().val()
                det = dict(det)
                farmid = det['farmer_id']
                if cid == farmid:
                    pickdate = det['Pickup_date']
                    pickstate = det['Pickup_status']
                    
                    if pickdate != 'None' and role == 'far' and pickstate == 'notpicked':
                      
                      detailsorder[p] = det
                      p += 1
        

    details2 = {
        'detorder': detailsorder
    }

    return render(request, "pickup.html", details2)


def program(request):
    return render(request, 'prog.html')


def contact(request):
    return render(request, 'contactUs.html')


def cart(request):
    return render(request, 'cart.html')


def soil1(request):
    return render(request, 'Soil_lab.html')


def soil2(request):
    return render(request, 'Soil_lab2.html')


def soil3(request):
    return render(request, 'Soil_lab3.html')


def soil4(request):
    return render(request, 'Soil_lab4.html')


def seed1(request):
    return render(request, 'sdealer.html')


def seed2(request):
    return render(request, 'sdealer2.html')


def seed3(request):
    return render(request, 'sdealer3.html')


def seedvar(request):
    return render(request, 'svar.html')


def fert1(request):
    return render(request, 'fert.html')


def fert2(request):
    return render(request, 'fert2.html')


def fert3(request):
    return render(request, 'fert3.html')


def vert1(request):
    return render(request, 'veternity1.html')


def vert2(request):
    return render(request, 'v2.html')


def vert3(request):
    return render(request, 'v3.html')


def vert4(request):
    return render(request, 'v4.html')


def symdisease(request):
    return render(request, 'symdiseases.html')


def sd2(request):
    return render(request, 'sd2.html')


def sd3(request):
    return render(request, 'sd3.html')


def sd4(request):
    return render(request, 'sd4.html')


def myprof(request):
    curuser =authe.current_user
    uid = curuser['localId']
    data=database.child('Farmer').child('Details').child(uid).get().val()
    if data == None:
        data = database.child('Consumer').child('Details').child(uid).get().val()
    diction = dict(data)
   
    details = {
        'det':diction
    }
    return render(request, 'myprof.html',details)