from django.shortcuts import render
from django.views.generic import TemplateView

from conttudoweb.core.context_processors import PAGES


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #SEO
        context['page'] = PAGES.get("PAGE_HOME")
        return context


class PortifolioView(TemplateView):
    template_name = "home/portifolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #SEO
        context['page'] = PAGES.get("PAGE_HOME")
        return context


class ContatoView(TemplateView):
    template_name = "home/contato.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #SEO
        context['page'] = PAGES.get("PAGE_HOME")
        return context


class SobreView(TemplateView):
    template_name = "home/sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #SEO
        context['page'] = PAGES.get("PAGE_HOME")
        return context
