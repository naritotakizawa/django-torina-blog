from django import forms


class SimpleCaptchaField(forms.CharField):

    def __init__(self, label='人かどうかの確認', **kwargs):
        super().__init__(label=label, required=True, **kwargs)
        self.widget.attrs['placeholder'] = '「いぬ」を漢字で書いてください'

    def clean(self, value):
        value = super().clean(value)
        if value == '犬':
            return value
        else:
            raise forms.ValidationError('答えが違います!')
