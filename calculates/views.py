from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import CalcHistory
from .forms import CalcForm


def calculate_value(expression):
    try:
        result = eval(expression)
    except:
        result = None
    return result


class MainView(View):
    template_name = 'index.html'
    
    def get(self, request):
        history = CalcHistory.objects.all()
        form = CalcForm()
        return render(request, self.template_name, {'form': form, 'history': history})

    def post(self, request):
        form = CalcForm(request.POST)
        history = CalcHistory.objects.all()

        if form.is_valid():
            expression = form.cleaned_data['expression']
            result = calculate_value(expression)

            if result is not None:
                calc_history = CalcHistory(expression=expression, result=result)
                calc_history.save()
            else:
                return HttpResponse("Ошибка при вычислении")

            history = CalcHistory.objects.all()

        return render(request, self.template_name, {'form': form, 'history': history})


