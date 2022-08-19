from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='landing_page'),
    path('v1/problems/', views.all_problems, name='all_problems'),
    path('v1/problems/create/', views.create_problem, name='create_problem'),
    path('v1/contests/', views.all_contests, name='all_contests'),
    path('v1/contests/score_table', views.score_table, name='score_table'),
    path('v1/classes/', views.all_classes, name='all_classes'),
    path('v1/classes/<int:class_id>/display/', views.single_class, name='single_class'),
    path('v1/problems/<int:problem_id>/display/', views.problem_display_mode,
         name='problem_display_mode'),
    path('v1/problems/<int:problem_id>/edit/', views.problem_edit_mode,
         name='problem_edit_mode'),
    path('v1/problems/<int:problem_id>/subproblems/add/',
         views.add_subproblem, name='add_subproblem'),
    path('v1/problems/<int:problem_id>/subproblems/<int:subproblem_id>/',
         views.delete_subproblem, name='delete_subproblem'),
    path('v1/problems/<int:problem_id>/submissions/submit',
         views.submit_submission, name='submit_submission'),
    path('v1/submissions/', views.list_submissions, name='list_submissions')
]
