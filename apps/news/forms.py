from django import forms

#Doesn't inherit from model, so using forms.Form instead of forms.ModelForm
class SummaryArticles(forms.Form):
    search_term = forms.CharField(max_length=45, required=True)
