from django import forms
# form control

# New Entry Form


class pgNewEntry(forms.Form):
    pageTitle = forms.CharField(widget=forms.TextInput)
    pageInfo = forms.CharField(label="", widget=forms.Textarea)
# New Entry Form


class pgSaveEntry(forms.Form):
    saveInfo = forms.CharField(widget=forms.Textarea)

# Search Bar Form


class searchBar(forms.Form):
    searchQ = forms.CharField(label="Search", widget=forms.TextInput
                              (attrs={'class': 'search', 'placeholder': 'Search Encyclopedia',
                                      'type': 'text'}))
# Search Bar Form
