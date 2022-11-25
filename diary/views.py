import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

# from .forms import InquiryForm, DiaryCreateForm , SukashiCreateForm , SukashiForm
from .forms import InquiryForm, DiaryCreateForm , SukashiCreateForm
from .models import Diary
from .models import Sukashi

from django.db.models import Q


logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)

class SukashiDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sukashi
    template_name = 'sukashi_detail.html'

class SukashiCreateView(LoginRequiredMixin, generic.CreateView):
    model = Sukashi
    template_name = 'sukashi_create.html'
    form_class = SukashiCreateForm
    success_url = reverse_lazy('diary:sukashi_list')

    def form_valid(self, form):
        Sukashi = form.save(commit=False)
        Sukashi.user = self.request.user
        Sukashi.save()
        messages.success(self.request, '透かしブロックを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "透かしブロックの作成に失敗しました。")
        return super().form_invalid(form)

class SukashiUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sukashi
    template_name = 'sukashi_update.html'
    form_class = SukashiCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:sukashi_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '透かしブロックを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "透かしブロックの更新に失敗しました。")
        return super().form_invalid(form)

class SukashiDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Sukashi
    template_name = 'sukashi_delete.html'
    success_url = reverse_lazy('diary:sukashi_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "透かしブロックを削除しました。")
        return super().delete(request, *args, **kwargs)

class SukashiRareListView(LoginRequiredMixin, generic.ListView):
    model = Sukashi
    template_name = 'sukashi_rarelist.html'
    # paginate_by = 3

    def get_queryset(self):
        sukashis = Sukashi.objects.all().order_by('-rare')
        return sukashis

class SukashiTimelineView(LoginRequiredMixin, generic.ListView):
    model = Sukashi
    template_name = 'sukashi_timeline.html'

    def get_queryset(self):
        # sukashies = Sukashi.objects.filter(user=self.request.user).order_by('-created_at')
        sukashies = Sukashi.objects.filter(Q(user=self.request.user)|Q(oflag=1)).order_by('-created_at')
        return sukashies


class SukashiList(LoginRequiredMixin, generic.ListView):
    model = Sukashi
    template_name = 'sukashi_list.html'
    # paginate_by = 12

    def get_context_data(self, **kwargs):
        # m_word = "1";
        # o_word = "1";
        q_word = self.request.GET.get('query')
        m_word = self.request.GET.get('my_c')
        o_word = self.request.GET.get('open_c')

        context = super().get_context_data(**kwargs)

        if m_word == "1" and o_word == "1":
            if q_word:
                context['count'] = Sukashi.objects.filter(Q(rare=q_word,user=self.request.user)|Q(rare=q_word,oflag=1)).count()
            else:
                context['count'] = Sukashi.objects.filter(Q(user=self.request.user)|Q(oflag=1)).count()
        elif m_word == "1" and o_word != "1":
            if q_word:
                context['count'] = Sukashi.objects.filter(rare=q_word,user=self.request.user).count()
            else:
                context['count'] = Sukashi.objects.filter(user=self.request.user).count()
        elif m_word != "1" and o_word == "1":
            if q_word:
                context['count'] = Sukashi.objects.filter(rare=q_word,oflag=1).exclude(user=self.request.user).count()
            else:
                context['count'] = Sukashi.objects.filter(oflag=1).exclude(user=self.request.user).count()
        elif m_word != "1" and o_word != "1":
            object_list = Sukashi.objects.none()
            # context['count'] = Sukashi.objects.filter(Q(user=self.request.user) | Q(oflag=1)).count()


        # context['count'] = Sukashi.objects.count()
        return context

    def get_queryset(self):
        m_word = "1";
        o_word = "1";
        q_word = self.request.GET.get('query')
        m_word = self.request.GET.get('my_c')
        o_word = self.request.GET.get('open_c')

        # object_list = Sukashi.objects.filter(Q(user=self.request.user)|Q(oflag=1))    
        # object_list = Sukashi.objects.none()
        object_list = Sukashi.objects.filter(Q(user=self.request.user) | Q(oflag=1))

        print("m_word",m_word)
        print("o_word",o_word)
        print("q_word",q_word)

        if m_word == "1" and o_word == "1":
            if q_word:
                object_list = Sukashi.objects.filter(Q(rare=q_word,user=self.request.user)|Q(rare=q_word,oflag=1))
            else:
                object_list = Sukashi.objects.filter(Q(user=self.request.user)|Q(oflag=1))
        elif m_word == "1" and o_word != "1":
            if q_word:
                object_list = Sukashi.objects.filter(rare=q_word,user=self.request.user)
            else:
                object_list = Sukashi.objects.filter(user=self.request.user)
        elif m_word != "1" and o_word == "1":
            if q_word:
                object_list = Sukashi.objects.filter(rare=q_word,oflag=1).exclude(user=self.request.user)
            else:
                object_list = Sukashi.objects.filter(oflag=1).exclude(user=self.request.user)
        elif m_word != "1" and o_word != "1":
            object_list = Sukashi.objects.none()
            # object_list = Sukashi.objects.filter(Q(user=self.request.user) | Q(oflag=1))

        return object_list
        
        
