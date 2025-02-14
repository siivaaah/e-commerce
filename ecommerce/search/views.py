from django.shortcuts import render
from shop.models import Products

from django.db.models import Q

def search(request):
    if (request.method=="POST"):
        q=request.POST['q']
        b=Products.objects.filter(Q(name__icontains=q) | Q(desc__icontains=q))
        context={'pro':b}

    return render(request,'search.html',context)
