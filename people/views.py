from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms import BooleanField, CharField, ChoiceField, DateField, ModelForm, SelectDateWidget, Form, Textarea
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from .models import Employee, PerformanceReview, ReviewNote
from mainsite.helpers import get_host_url, send_email, send_evaluation_complete_email


class PerformanceReviewForm(Form):
    discussion_date = DateField(widget=SelectDateWidget)
    evaluation = CharField(widget=Textarea, required=False)


class PerformanceReviewView(FormView):
    template_name = "people/performancereview.html"
    form_class = PerformanceReviewForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pr = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        context['object'] = pr
        context['notes'] = ReviewNote.objects.filter(employee=pr.employee, manager__user=User(pk=self.request.user.pk))
        context['is_denied'] = pr.status == PerformanceReview.EVALUATION_DENIED
        return context

    def form_valid(self, form):
        # Set evaluation value
        pr = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        # try:
        #     pe = pr.performanceevaluation
        # except PerformanceEvaluation.DoesNotExist:
        #     pe = PerformanceEvaluation.objects.create(review=pr)
        # if form.cleaned_data['evaluation']:
        #     pe.evaluation = form.cleaned_data['evaluation']
        # pe.discussion_date = form.cleaned_data['discussion_date']
        # pe.save()
        if pr.status == PerformanceReview.NEEDS_EVALUATION:
            pr.status = PerformanceReview.EVALUATION_WRITTEN_AND_DATE_SET
            pr.save()
        if pr.status == PerformanceReview.EVALUATION_DENIED:
            pr.status = PerformanceReview.EVALUATION_COMPLETED
            pr.save()
        
        # Send notification emails
        host = get_host_url(self.request)
        send_email(
            [pr.employee.user.email],
            f'{pr.employee.manager.user.get_full_name()} has updated your performance evaluation',
            f'Your manager {pr.employee.manager.user.get_full_name()} has updated your information for an upcoming performance review. View here: {host}',
            f'Your manager {pr.employee.manager.user.get_full_name()} has updated your information for an upcoming performance review. View here: <a href="{host}">{host}</a>',
        )

        return super().form_valid(form)


class PerformanceReviewApprovalForm(Form):
    approved = BooleanField(required=False)
    denied = BooleanField(required=False)
    note = CharField(widget=Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        approved = cleaned_data.get("approved")
        denied = cleaned_data.get("denied")
        note = cleaned_data.get("note")

        if not approved and not denied:
            raise ValidationError("Please select either approved or denied")

        if approved and denied:
            raise ValidationError("Please select only one")

        if denied and not note:
            raise ValidationError("Please provide a note for the manager")


class PerformanceReviewApprovalView(FormView):
    template_name = "people/performancereviewapproval.html"
    form_class = PerformanceReviewApprovalForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # Set evaluation value
        pr = PerformanceReview.objects.get(pk=self.kwargs['pk'])
        # try:
        #     pe = pr.performanceevaluation
        # except PerformanceEvaluation.DoesNotExist:
        #     # TODO
        #     pass
        if form.cleaned_data['approved']:
            # pe.upper_manager_accepted = True
            pr.status = PerformanceReview.EVALUATION_APPROVED
        else:
            # pe.upper_manager_accepted = False
            pr.status = PerformanceReview.EVALUATION_DENIED
        if form.cleaned_data['note']:
            pe.upper_manager_note = form.cleaned_data['note']
        # pe.save()
        pr.save()
        
        # Send notification emails
        url = get_host_url(self.request) + reverse('performancereview-view', args=[pr.pk])
        if form.cleaned_data['approved']:
            send_email(
                [pr.employee.manager.user.email],
                f'A Performance Evaluation has been completed',
                f'{self.request.user.get_full_name()} has approved a performance evaluation for {pr.employee.user.get_full_name()}. Please review it here: {url}',
                f'{self.request.user.get_full_name()} has approved a performance evaluation for {pr.employee.user.get_full_name()}. Please review it here: <a href="{url}">{url}</a>',
            )
        else:
            send_email(
                [pr.employee.manager.user.email],
                f'A Performance Evaluation has been denied and requires revision',
                f'{self.request.user.get_full_name()} has denied a performance evaluation you wrote for {pr.employee.user.get_full_name()}. Please review their notes and revise it here: {url}',
                f'{self.request.user.get_full_name()} has denied a performance evaluation you wrote for {pr.employee.user.get_full_name()}. Please review their notes and revise it here: <a href="{url}">{url}</a>',
            )

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
            send_evaluation_complete_email([review.employee.manager.manager.user.email], review, get_host_url(self.request))
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
            send_evaluation_complete_email([review.employee.manager.manager.user.email], review, get_host_url(self.request))
        return HttpResponse('Success')


class ReviewNoteEditBase(View):
    template_name = "people/reviewnote_form.html"
    model = ReviewNote
    fields = ['employee', 'note']
    success_url = reverse_lazy('dashboard')


class ReviewNoteCreateView(ReviewNoteEditBase, CreateView):
    pass


class ReviewNoteUpdateView(ReviewNoteEditBase, UpdateView):
    pass


class ReviewNoteDeleteView(DeleteView):
    template_name = "people/reviewnote_confirm_delete.html"
    model = ReviewNote
    success_url = reverse_lazy('dashboard')
