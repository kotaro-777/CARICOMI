#viewsのgeneric（汎用ビューが沢山あるモジュール）
from django.views import generic
#forms.pyから使用するフォームクラスをインポート
from .forms import ReviewsCreateForm, SearchForm
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

from django.db.models import Q

from . import views

###################################################################
#loggerを取得
logger = logging.getLogger(__name__)



#日記一覧表示機能
class ReviewsList(LoginRequiredMixin, generic.ListView):
    model = Reviews
    template_name = 'review_list.html'
    paginate_by = 5
    
    #post通信時に行う処理
    def post(self, request, *args, **kwargs):
        #ページが変わってもフォームに値が残るようにする
        form_value = self.request.POST.get('service_name', None)
        request.session['form_value'] = form_value
        
        #検索時にページネーションに関連したエラーを防ぐ　※後で使わないとどうなるか試す
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        
        return self.get(request, *args, **kwargs)
    
    #ListViewが返すtemplateなどの表示するobject
    def get_context_data(self, **kwargs):
        #オーバーライドする
        context = super().get_context_data(**kwargs)
        
        #sessionに値がある場合、その値をセットする(ページングしても値が変わらないように)
        service_name = ''
        #ある場合
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            service_name = form_value
        default_data = {'service_name':service_name}
        
        search_form =SearchForm(initial=default_data)#検索フォーム
        #テンプレートで使えるようにする
        context['search_form'] = search_form
        
        return context
    
    
    
    #投稿された日記を作られた順に並べて表示するメソッド
    def get_queryset(self):
        #sessionnnに値がある場合、その値でクエリを発行する
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            service_name = form_value
            
            #検索条件
            condition_service_name = Q()
            
            if len(service_name != 0 and service_name):
                condition_service_name = Q(service_name__icontains=service_name)
                
            return Reviews.objects.select_related().filter(condition_service_name)

        else:
            return Reviews.objects.none()



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