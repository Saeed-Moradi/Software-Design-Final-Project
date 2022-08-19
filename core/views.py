from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .models import Submission
from .scoring_system import *
import hashlib
import urllib
from django import template
from django.utils import safestring


# import code for encoding urls and generating md5 hashes
# import urllib, hashlib

# # Set your variables here
# email = "someone@somewhere.com"
# default = "https://www.example.com/default.jpg"
# size = 40
#
# # construct the url
# gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
# gravatar_url += urllib.urlencode({'d': default, 's': str(size)})

# register = template.library()
#
#
# @register.filter
# def gravatarـurl(email, size=40):
#     default = "https://"

def index(request):
    form = AuthenticationForm(request.POST)
    return render(request, 'core/landing_page.html', {'form': form})


def delete_subproblem(request, problem_id, subproblem_id):
    return HttpResponse("")


def all_problems(request):
    return render(request, 'core/all_problems.html')


def all_contests(request):
    return render(request, 'core/all_contests.html')


def all_classes(request):
    return render(request, 'core/all_classes.html')


def create_problem(request):
    return render(request, 'core/create_problem.html')


def list_submissions(request):
    submissions = Submission.objects.all()
    return render(request, 'core/submissions.html', {'submissions': submissions})


def score_table(request):
    return render(request, 'core/score_table.html')


def single_class(request):
    return render(request, 'core/single_class.html')


def problem_edit_mode(request, problem_id):
    # TODO
    # uncomment below lines when authentication packages implement & also check if
    # the authenticate user is the same with the person who had set the
    # problem.
    # if not request.user.is_authenticated:
    #    return HttpResponse("You must log in to be able to update a problem")

    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == "POST":
        return handle_problem_change(request, problem)
    subproblems = problem.subproblem_set.all().order_by("index")

    # Here I try to restructure result field to show different row of data
    # on successive lines with different ways like transferring result field
    # into string, add alternative field to the form(I also comment the
    # relative codes in forms.py). But i fail:|, so i let it go at the
    # moment without that structure.

    # subproblems_edited = []
    # for subproblem in subproblems:
    #    subproblems_edited.append(prepare_output_subproblem(subproblem))
    #    print(subproblems_edited[subproblems_edited.__len__()-1].result_output)

    subproblems_forms = [SubProblemEditModeForm(
        instance=object, prefix="subproblem#{0}".format(object.index)
    ) for index, object in
        enumerate(subproblems)
    ]
    form = ProblemEditModeForm(instance=problem)
    context = {'page_title': problem.title.capitalize(),
               'problem_id': problem.id,
               'form': form,
               'subproblems_forms': subproblems_forms
               }
    return render(request, 'core/problem_edit_mode.html', context)


def handle_problem_change(request, problem):
    form = ProblemEditModeForm(request.POST, request.FILES)

    subproblems_forms = []
    subproblem_index = 1
    subproblem_form = SubProblemEditModeForm(request.POST, prefix=
    'subproblem#{0}'.format(subproblem_index))
    subproblem_existence = subproblem_form.is_valid()
    while subproblem_existence:
        subproblems_forms.append(subproblem_form)
        subproblem_index += 1
        subproblem_form = SubProblemEditModeForm(request.POST, prefix=
        'subproblem#{0}'.format(subproblem_index))
        subproblem_existence = subproblem_form.is_valid()

    if form.is_valid():
        problem.title = form.cleaned_data['title']
        problem.text = form.cleaned_data['text']
        if len(request.FILES) != 0:
            file = request.FILES['init_queries_file']
            file_data = file.read()
            file_data = file_data.decode('utf-8')
            problem.init_queries = file_data
        else:
            data = form.cleaned_data['init_queries']
            problem.init_queries = data
        problem.save()
        judge_status_code, judge_status_body = problem_check_init_queries(problem)

    subproblems = problem.subproblem_set.all().order_by('index')
    for i in range(subproblems.__len__()):
        print(subproblems.__len__())
        print(subproblems_forms.__len__())
        subproblem = subproblems[i]
        form = subproblems_forms[i]
        subproblem.title = form.cleaned_data['title']
        subproblem.text = form.cleaned_data['text']
        subproblem.dump_queries = form.cleaned_data['dump_queries']
        subproblem.final_query = form.cleaned_data['final_query']
        subproblem.save()
        subproblem_check_queries(subproblem)
    return HttpResponseRedirect(reverse('core:problem_edit_mode', args=(problem.id,)))


def add_subproblem(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    problem.number_of_subproblems += 1
    problem.subproblem_set.create(index=problem.number_of_subproblems)
    problem.save()
    return HttpResponseRedirect(reverse('core:problem_edit_mode', args=(problem.id,)))


def problem_display_mode(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    subproblems = [SubProblemEditModeForm(
        instance=object, prefix="subproblem#{0}".format(index)
    ) for index, object in
        enumerate(problem.subproblem_set.all().order_by("index"))
    ]

    form = ProblemDisplayModeForm(instance=problem)
    submission_form = SubmissionForm()
    context = {'form': form,
               'problem_id': problem.id,
               'subproblems_forms': subproblems,
               'submission_form': submission_form}
    return render(request, 'core/problem_display_mode.html', context)


def submit_submission(request, problem_id):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            input_file_data = handle_uploaded_file(request.FILES['submission_file'])

            # TODO
            # find correct username according to user authentication
            username_id = -1

            instance = Submission(problem_id=problem_id,
                                  contender_id=username_id, input_query=input_file_data)
            instance.input_query_status = 1
            instance.save()
            submissions.append(instance)
            server_judge_submission_process(submissions.__len__() - 1)
            return HttpResponseRedirect(reverse('core:list_submissions'))


def handle_uploaded_file(f):
    query_string = str('')
    for chunk in f.chunks():
        query_string += str(chunk.decode('utf-8'))
    return query_string

# def map_init_queries_data_to_model(data):
#    queries = data.split(";")
#    queries = [query+";" for query in queries]
#    if data[data.__len__()-1] == ';':
#        queries.pop()
#    else:
#        queries[queries.__len__()-1] = queries[queries.__len__()-1][:-1]
#    return queries


# def prepare_output_subproblem(subproblem):
#    rows = []
#    #edited_subproblem = subproblem
#    #edited_subproblem.result = []
#    for row in subproblem.result:
#                rows.append(", ".join(row))
#    subproblem.result_output = "\n".join(rows)
#    print("*"+subproblem.result_output)
#    return subproblem


# def map_init_queries_data_to_model(data):
#    queries = data.split(";")
#    queries = [query+";" for query in queries]
#    if data[data.__len__()-1] == ';':
#        queries.pop()
#    else:
#        queries[queries.__len__()-1] = queries[queries.__len__()-1][:-1]
#    return queries


# def prepare_output_subproblem(subproblem):
#    rows = []
#    #edited_subproblem = subproblem
#    #edited_subproblem.result = []
#    for row in subproblem.result:
#                rows.append(", ".join(row))
#    subproblem.result_output = "\n".join(rows)
#    print("*"+subproblem.result_output)
#    return subproblem
