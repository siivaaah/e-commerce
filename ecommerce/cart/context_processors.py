from cart.models import Cart

def count_items(request):
    u=request.user
    count = 0
    if request.user.is_authenticated: #checks whether the user is authenticated
        c=Cart.objects.filter(user=u) #to filter cart records to a particular user

        #to calculate total count

        for i in c:
            count+=i.quantity

    return {'count':count}