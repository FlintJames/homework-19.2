
from django.forms import ModelForm, forms, BaseInlineFormSet

from catalog.models import Product, Version

forbidden_words = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at',)

    def clean_product_name(self):
        clean_data = self.cleaned_data.get('name')
        if clean_data in forbidden_words:
            raise forms.ValidationError(f'Наименование не должно содержать слова: {forbidden_words}')

        return clean_data

    def clean_product_description(self):
        clean_data = self.cleaned_data.get('description')
        if clean_data in forbidden_words:
            raise forms.ValidationError(f'Описание не должно содержать слова: {forbidden_words}')

        return clean_data


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class BaseVersionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('is_active', False):
                active_count += 1
        if active_count > 1:
            raise forms.ValidationError('Может быть только одна активная версия.')
