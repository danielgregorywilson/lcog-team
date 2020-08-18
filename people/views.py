from django.forms import CharField, DateField, SelectDateWidget, Form, Textarea
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from .models import PerformanceEvaluation, PerformanceReview
from .serializers import PerformanceReviewSerializer


class PerformanceReviewForm(Form):
    discussion_date = DateField(widget=SelectDateWidget)
    evaluation = CharField(widget=Textarea, required=False)


class PerformanceReviewView(FormView):
    template_name = "people/performancereview.html"
    form_class = PerformanceReviewForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # Set evaluation value
        pr = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        try:
            pe = pr.performanceevaluation
        except PerformanceEvaluation.DoesNotExist:
            pe = PerformanceEvaluation.objects.create(review=pr)
        if form.cleaned_data['evaluation']:
            pe.evaluation = form.cleaned_data['evaluation']
        pe.discussion_date = form.cleaned_data['discussion_date']
        pe.save()
        if pr.status == PerformanceReview.NEEDS_EVALUATION:
            pr.status = PerformanceReview.EVALUATION_WRITTEN_AND_DATE_SET
            pr.save()
        
        
        # Send notification emails
        return super().form_valid(form)


class PerformanceReviewEmployeeMetConfirmView(View):
    
    def get(self, request, *args, **kwargs):
        review_pk = request.GET['review_pk']
        review = PerformanceReview.objects.get(pk=review_pk)
        evaluation = review.performanceevaluation
        evaluation.employee_discussed = True
        evaluation.save()
        if evaluation.manager_discussed:
            review.status = PerformanceReview.EVALUATION_COMPLETED
            review.save()
        return HttpResponse('Success')
        

class PerformanceReviewManagerMetConfirmView(View):
    
    def get(self, request, *args, **kwargs):
        review_pk = request.GET['review_pk']
        review = PerformanceReview.objects.get(pk=review_pk)
        evaluation = review.performanceevaluation
        evaluation.manager_discussed = True
        evaluation.save()
        if evaluation.employee_discussed:
            review.status = PerformanceReview.EVALUATION_COMPLETED
            review.save()
        return HttpResponse('Success')
