from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ponytoon import views as uploader_views
from ponytoon.views import ArtsDetailView, ArtsDeleteView
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('gallery/', views.gallery , name='gallery'),
    path('upload/', uploader_views.upload , name='upload'),
    path('terms/', views.terms , name='terms'),
    path('privacy/', views.privacy , name='privacy'),
    path('faq/', views.faq , name='faq'),
    path('contact/', views.contact , name='contact'),

    path('arts/<str:arts>/', include([
        path('', views.ArtsDetailView.as_view(), name='arts_detail'),
        path('pos', views.reppos, name='pos'),
        path('neg', views.repneg, name='neg'),
        path('edit', views.artsdetailview_edit, name='arts_edit'),
        path('remove', views.file_toggle_visibility, name='arts_visibility'),
        path('delete', login_required(views.ArtsDeleteView.as_view()), name='arts_delete'),
        path('addcom', views.CommentCreateView.as_view(), name='arts_comment'),
        # path('repcom/<int:number>/', views.repcom, name='arts_comment_grant'),
        path('report/', views.report, name='arts_report'),
        # path('report/<int:number>/', views.report, name='arts_report_comment'),
    ])),
    path('comments/<int:number>/', include ([
        path('reputation/<str:arts>', views.comment_reputation, name='arts_comment_grant'),
        path('report/<str:arts>', views.report, name='arts_report_comment'),
    ])),

	]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
