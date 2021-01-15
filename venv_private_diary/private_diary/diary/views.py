#viewsのgeneric（汎用ビューが沢山あるモジュール）
from django.views import generic
#forms.pyから使用するフォームクラスをインポート
from .forms import InquiryForm, CareerDiaryCreateForm
#URLの逆引きを行えて、URLのハードコーディングを防げる
from django.urls import reverse_lazy
#送信が成功した際にメッセージを表示するメソッド
from django.contrib import messages
#loggingをインポート
import logging
#ログインしていないとアクセスできない状態にするもの
from django.contrib.auth.mixins import LoginRequiredMixin
#models.pyのCareerDiaryモデルをインポート
from .models import CustomUser, CareerDiary


from . import views

#########################################################


#loggerを取得
logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'diary/index.html'
    
class InquiryView(generic.FormView):
    #テンプレートとして使用するhtmlファイルを指定
    template_name = 'diary/inquiry.html'
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
    
    

#日記一覧表示機能
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = CareerDiary
    template_name = 'diary/diary_list.html'
    paginate_by = 2
    
    #投稿された日記を作られた順に並べて表示するメソッド
    def get_queryset(self):
        diaries = CareerDiary.objects.filter(user=self.request.user).order_by('-created_at')
        #ページネイションを指定 クラスベースView使ったらヤバいほど簡単
        return diaries



#日記の詳細表示
class CareerDiaryDetail(LoginRequiredMixin, generic.DetailView):
    model = CareerDiary
    template_name = 'diary/diary_detail.html'
    
    
#CareerDiary作成機能
class CareerDiaryCreate(LoginRequiredMixin, generic.CreateView):
    model = CareerDiary
    template_name = 'diary/diary_create.html'
    form_class = CareerDiaryCreateForm
    #正常に処理が終わった時の遷移先
    success_url = reverse_lazy('diary:diary_list')

    #フォームのバリデーションに以上がなかった時の処理
    def form_valid(self, form):
        #commit=falseを指定するとデータにまだ保存されていない状態のオブジェクトが返される
        diary = form.save(commit=False)
        #diaryのuserIdに自動生成されるuseIDを代入
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)
    
    #フォームのバリデーションにエラーがなかった場合の処理
    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)


#日記編集機能
class CareerDiaryUpdate(LoginRequiredMixin, generic.UpdateView):
    model = CareerDiary
    template_name = 'diary/diary_update.html'
    #フォームフィールドはCreateフォームと変わらないため使いまわす
    form_class = CareerDiaryCreateForm
    
    
    def get_success_url(self):
        """逆引きメソッド"""
        return reverse_lazy('diary:diary_detail', kwargs={'pk':self.kwargs['pk']})
    
    def form_valid(self, form):
        """正常にフォームが入力された時に実行されるメソッド"""
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """正常にフォームが入力されなかった時に実行されるメソッド"""
        messages.success(self.request, '日記を更新できませんでした。')
        return super().form_invalid(form)

#日記削除機能
class CareerDiaryDelete(LoginRequiredMixin, generic.DeleteView):
    model = CareerDiary
    template_name = 'diary/diary_delete.html'
    #削除を正常に行えたら日記一覧ページへと遷移する
    success_url = reverse_lazy('diary:diary_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)