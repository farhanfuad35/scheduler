from django.shortcuts import render
from django.http import *
from formtools.wizard.views import SessionWizardView
from .forms import *

# Create your views here.

# class defaultView(FormView):
#     template_name = 'test.html'
#     form_class = TeacherForm
#     success_url = '/'

# def defaultView(request):
#     form = TeacherForm()
#     return render(request, 'test.html', {'form': form})

class ScheduleWizard(SessionWizardView):
    template_name = 'test.html'

    def get_form_initial(self, step):
        if step == '1':
            return {"section":""}
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        # Do something with the form
        return HttpResponseRedirect('/')