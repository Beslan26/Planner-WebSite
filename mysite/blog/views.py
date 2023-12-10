from django.shortcuts import render, get_object_or_404
from .forms import CreateListForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import ToDoList
from django.utils import timezone

from .forms import Test

# Create your views here.

def index(request, id):
    ls = ToDoList.objects.get(id=id)

    if request.method == 'POST':
        if request.POST.get('save'):
            for item in ls.item_set.all():
                p = request.POST

                if 'clicked' == p.get('c' + str(item.id)):
                    item.complete = True
                else:
                    item.complete = False

                if 'text' + str(item.id) in p:
                    item.text = p.get('text' + str(item.id))

                item.save()
        elif request.POST.get('add'):
            newItem = request.POST.get('new')
            if newItem != '':
                ls.item_set.create(text=newItem, complete=False)
            else:
                print('invalid')

    return render(request, 'blog/index.html', {'ls': ls})

def home(request):
	return render(request, "blog/home.html", {})


def get_name(request):
    if request.method == "POST":
        form = CreateListForm(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n, date=timezone.now())
            t.save()

            return HttpResponseRedirect("/%i" % t.id)

    else:
        form = CreateListForm()

    return render(request, "blog/create.html", {"form": form})


def view(request):
    l = ToDoList.objects.all()
    return render(request, 'blog/view.html', {'list':l} )


def test(request):
    if request.method == "POST":
        name = request.POST.get('name')
        return HttpResponse(f'Передали вот эти данные: {name}')
    else:
        form = Test()
        context = {'form': form}
        return render(request, 'blog/test.html', context)



