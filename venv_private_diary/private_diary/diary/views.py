#viewsのgeneric（汎用ビューが沢山あるモジュール）
from django.views import generic
#forms.pyから使用するフォームクラスをインポート
from .forms import InquiryForm
#URLの逆引きを行えて、URLのハードコーディングを防げる
from django.urls import reverse_lazy
#送信が成功した際にメッセージを表示するメソッド
from django.contrib import messages

import logging
#########################################################


#loggerを取得
logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
class InquiryView(generic.FormView):
    #テンプレートとして使用するhtmlファイルを指定
    template_name = 'inquiry.html'
    #使用するフォームクラスを指定
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')
    
    def form_valid(self, form):
        #forms.pyでInquiryFormに定義したsend_email()メソッドを呼び出す
        form.send_email()
        #送信成功時のメッセージ表示
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info(f"Inquiry sent by{form.cleaned_data['name']}")
        return super().form_valid(form)