from django.forms import ModelForm, forms, BaseInlineFormSet, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'maker')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Наименование не должно содержать данное слово')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Описание не должно содержать данное слово')

        return cleaned_data


class ProductModeratorForm(ModelForm):
    class Meta:
        model = Product
        fields = ("category", "description", "is_published")



class VersionForm(StyleFormMixin, ModelForm):
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
