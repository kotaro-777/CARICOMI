from django import forms

#models.pyからDiaryモデルクラスをインポート
from .models import Review



#Review作成フォーム
class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'service',
            'quality',
            'content',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SearchForm(forms.Form):
    service_name = forms.CharField(initial="",
                                    required=False, 
                                    label="サービス名",
                                    widget=forms.TextInput(attrs={"placeholder":"サービス名を検索"})
    )
