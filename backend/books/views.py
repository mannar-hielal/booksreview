from django.shortcuts import render


# Create your views here.
def home_view(request):
    my_variable = "Hello World!"
    my_desc = "welcome to this long test, i am trying to make it shorter"
    my_array = ["moody", "moda", "mama"]
    return render(request, 'home.html', {
        'my_var': my_variable,
        'my_arr': my_array,
        'some_desc': my_desc
    })
