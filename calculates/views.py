from django.shortcuts import redirect, render
from django.views import View

from .forms import CalcForm


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
            history.append({
                'expression': form.cleaned_data['expression'],
                'result': eval(form.cleaned_data['expression'])
            })
            request.session['history'] = history
            return redirect('/')

        return render(request, self.template_name, {
            'form': form,
            'history': history
        })
