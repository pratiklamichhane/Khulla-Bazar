from django.shortcuts import render ,redirect
from item.models import Category , Item
from .forms import SignupForm
# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6] #filters non sold products
    categories = Category.objects.all() #displays all
    return render(request, 'core/index.html' ,{
        'categories' : categories,
        'items':items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        # Use a different variable name for the form instance
        submitted_form = SignupForm(request.POST)

        if submitted_form.is_valid():
            submitted_form.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })