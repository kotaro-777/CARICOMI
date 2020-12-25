#viewsのgeneric（汎用ビューが沢山あるモジュール）
from django.views import generic
#forms.pyから使用するフォームクラスをインポート
from .forms import ReviewsCreateForm
#URLの逆引きを行えて、URLのハードコーディングを防げる
from django.urls import reverse_lazy
#送信が成功した際にメッセージを表示するメソッド
from django.contrib import messages
#loggingをインポート
import logging
#ログインしていないとアクセスできない状態にするもの
from django.contrib.auth.mixins import LoginRequiredMixin
#models.pyのReviewsモデルをインポート
from .models import CustomUser, Reviews


from . import views

###################################################################
#loggerを取得
logger = logging.getLogger(__name__)



#日記一覧表示機能
class ReviewsList(LoginRequiredMixin, generic.ListView):
    model = Reviews
    template_name = 'review_list.html'
    paginate_by = 2
    
    #投稿された日記を作られた順に並べて表示するメソッド
    def get_queryset(self):
        reviews= Reviews.objects.all().order_by('-created_at')
        #ページネイションを指定 クラスベースView使ったらヤバいほど簡単
        return reviews



#レビューの詳細表示
class ReviewsDetail(LoginRequiredMixin, generic.DetailView):
    model = Reviews
    template_name = 'review_detail.html'
    
    
#レビュー作成機能
class ReviewsCreate(LoginRequiredMixin, generic.CreateView):
    model = Reviews
    template_name = 'review_create.html'
    form_class = ReviewsCreateForm
    #正常に処理が終わった時の遷移先
    success_url = reverse_lazy('reviews:review_list')

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


#レビュー編集機能
class ReviewsUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Reviews
    template_name = 'review_update.html'
    #フォームフィールドはCreateフォームと変わらないため使いまわす
    form_class = ReviewsCreateForm
    
    
    def get_success_url(self):
        """逆引きメソッド"""
        return reverse_lazy('reviews:review_detail', kwargs={'pk':self.kwargs['pk']})
    
    def form_valid(self, form):
        """正常にフォームが入力された時に実行されるメソッド"""
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """正常にフォームが入力されなかった時に実行されるメソッド"""
        messages.success(self.request, '日記を更新できませんでした。')
        return super().form_invalid(form)

#レビュー削除機能
class ReviewsDelete(LoginRequiredMixin, generic.DeleteView):
    model = Reviews
    template_name = 'review_delete.html'
    #削除を正常に行えたら日記一覧ページへと遷移する
    success_url = reverse_lazy('reviews:reviews_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)