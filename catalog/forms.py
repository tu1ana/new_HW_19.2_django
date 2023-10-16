from django import forms

from catalog.models import Product, Version, BlogEntry


class StyleFormMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        """
        валидацию названия и описания продукта таким образом, чтобы нельзя было в них добавлять слова:
        казино, криптовалюта, крипта, биржа, дёшево, бесплатно, обман, полиция, радар.
        """
        cleaned_data = self.cleaned_data.get('name')
        if cleaned_data in ('казино', 'криптовалюта', 'крипта', 'биржа', 'дёшево', 'бесплатно', 'обман', 'полиция', 'радар'):
            raise forms.ValidationError('Apparently you have used banned words, please, replace them')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        if cleaned_data in ('казино', 'криптовалюта', 'крипта', 'биржа', 'дёшево', 'бесплатно', 'обман', 'полиция', 'радар'):
            raise forms.ValidationError('Apparently you have used restricted words, please, replace them')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = ('name', 'number')


class BlogEntryForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = BlogEntry
        fields = ('heading', 'content')
