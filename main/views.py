from django.shortcuts import render
from django.views import View

class HomePageView(View):
    def get(self, request):
        template_name = 'index.html'
        return render(request=request, template_name=template_name)