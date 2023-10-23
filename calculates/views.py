from django.shortcuts import redirect, render
from django.views import View

from .forms import CalcForm
from .calculation_logic import ExpressionCalculation


class MainView(View):
    template_name = 'index.html'

    def get(self, request):
        history = request.session.get('history')
        form = CalcForm()
        return render(request, self.template_name, {
            'form': form,
            'history': history
        })

    def post(self, request):
        form = CalcForm(request.POST)
        history = request.session.get('history', [])
        if form.is_valid():
            calculation = ExpressionCalculation(
                form.cleaned_data['expression']
            )
            history.append({
                'expression': form.cleaned_data['expression'],
                'result': calculation.get_result()
            })
            request.session['history'] = history
            return redirect('/')

        return render(request, self.template_name, {
            'form': form,
            'history': history
        })
