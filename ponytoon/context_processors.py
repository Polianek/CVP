from django.db.models import Sum
from ponytoon.models import Upload, Comment
from adminpanel.models import Report, Suggestions

def extras(request):
    report_warning = Report.objects.filter(verified=False).order_by('-date').count()
    suggestions_warning = Suggestions.objects.filter(verified=False).order_by('-date').count()
    if request.user.is_authenticated:
        u = request.user.id
        user_reputation_art = Upload.objects.filter(author_id=u, visible=1).aggregate(Sum('reputation')).get("reputation__sum")
        user_reputation_comment = Comment.objects.filter(author_id=u, visible=1).aggregate(Sum('points')).get("points__sum")
        user_reputation = (user_reputation_art or 0) + (user_reputation_comment or 0)
        # if user_reputation_art or user_reputation_comment is None:
        #     user_reputation = user_reputation_art + user_reputation_comment

        return {'user_reputation':user_reputation, 'report_warning':report_warning, 'suggestions_warning':suggestions_warning}
    else:
        return {'report_warning':report_warning, 'suggestions_warning':suggestions_warning}
