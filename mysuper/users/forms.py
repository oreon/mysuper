
from django import forms

class ActorSearchForm(forms.Form):
    
    name =  forms.CharField(
                    required = False,
                    label='Search name or surname!', 
                    widget=forms.TextInput(attrs={'placeholder': 'search here!'})
                  )

    search_cap_exact = forms.IntegerField(
                    required = False,
                    label='Search age (exact match)!'
                  )

    search_cap_min = forms.IntegerField(
                    required = False,
                    label='Min age'
                  )


    search_cap_max = forms.IntegerField(
                    required = False,
                    label='Max age'
                  )