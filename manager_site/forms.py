from django import forms


class CategoryForm(forms.Form):
    name = forms.CharField(required=True, max_length=200)
    imageUrl = forms.CharField(required=True, max_length=500)


class DishForm(forms.Form):
    name = forms.CharField(required=True, max_length=200)
    price = forms.IntegerField(required=True)
    description = forms.CharField(required=True, max_length=500)
    imageUrl = forms.CharField(required=True, max_length=500)
    is_gluten_free = forms.BooleanField(default=False)
    is_vegeterian = forms.BooleanField(default=False)
