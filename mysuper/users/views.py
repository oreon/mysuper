# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
import django_filters
from mysuper.users.forms import ActorSearchForm
from mysuper.users.models import Department

from .models import User, Department


class ListFilteredMixin(object):
    """
    Mixin that adds support for django-filter
    """

    filter_set = None
    
    def get_filter_set(self):
        if self.filter_set:
            return self.filter_set
        else:
            raise Exception(
                "ListFilterMixin requires either a definition of "
                "'filter_set' or an implementation of 'get_filter()'")

    def get_filter_set_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.request.GET,
            'queryset': self.get_base_queryset(),
        }

    def get_base_queryset(self):
        """
        We can decided to either alter the queryset before or after applying the
        FilterSet
        """
        return super(ListFilteredMixin, self).get_queryset()

    def get_constructed_filter(self):
        # We need to store the instantiated FilterSet cause we use it in
        # get_queryset and in get_context_data
        if getattr(self, 'constructed_filter', None):
            return self.constructed_filter
        else:
            f = self.get_filter_set()(**self.get_filter_set_kwargs())
            self.constructed_filter = f
            return f

    def get_queryset(self):
        return self.get_constructed_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.update({'filter': self.get_constructed_filter()})
        return super(ListFilteredMixin, self).get_context_data(**kwargs)



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    
from django.db import models

class DepartmentFilter(django_filters.FilterSet):
    
    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_type': 'icontains',
            }
        }
    }
    
    
    class Meta:
        model = Department


    
class DepartmentListView(LoginRequiredMixin, ListFilteredMixin,  ListView):
    model = Department
    paginate_by = 3
    filter_set = DepartmentFilter
    
    ''' use this if not using listfiltermixin
     def get_queryset(self):
        try:
            name = self.kwargs['name']
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(name__icontains = name)
        else:
            object_list = self.model.objects.all()
        return object_list
    
    '''
      
    slug_field = "name"
    slug_url_kwarg = "name"
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        context['current_request'] = self.request.META['QUERY_STRING']
        context['form'] = ActorSearchForm()
        
        return context

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):

    class Meta:
        model = Department
        fields = '__all__'
   
    
class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    # These next two lines tell the view to index lookups by username
    slug_field = "name"
    slug_url_kwarg = "name"