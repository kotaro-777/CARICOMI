from django import forms

#models.pyからDiaryモデルクラスをインポート
from .models import Reviews



#WordOfMouth作成フォーム
class ReviewsCreateForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = [
            'service_name',
            'support_quality',
            'subject',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
