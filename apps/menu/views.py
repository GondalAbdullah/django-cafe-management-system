from django.views.generic import ListView, DetailView
from .models import MenuItem
from django.shortcuts import render

# Create your views here.

def landing_page_view(request):
    return render(request, 'menu/landing_page.html')


class MenuListView(ListView):
    model = MenuItem
    template_name = "menu/list.html"
    context_object_name = "items"
    paginate_by = 12


    def get_queryset(self):
        qs = MenuItem.objects.filter(is_active=True)

        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category=category)

        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(name__icontains=search)

        return qs.order_by("category", "name")


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = MenuItem.CATEGORY_CHOICES
        ctx["current_category"] = self.request.GET.get("category", "")
        return ctx
    

class MenuDetailView(DetailView):
    model = MenuItem
    template_name = "menu/detail.html"
    context_object_name = "item"


# def menu_list(request):
#     category = request.GET.get('category')
#     if category:
#         items = MenuItem.objects.filter(category=category)
#     else:
#         items = MenuItem.objects.all()
#     categories = MenuItem.CATEGORY_CHOICES
#     return render(request, 'menu/menu_list.html', {'items': items, 'categories': categories})


# def menu_detail(request, pk):
#     item = get_object_or_404(MenuItem, pk=pk)
#     return render(request, 'menu/menu_detail.html', {'item': item})