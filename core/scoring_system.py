import psycopg2
import re
import threading

import psycopg2

from .models import Problem, SubProblemSubmission


# This function will sort a 2D-list based on axis = 1 (columns),
# it starts from column 0 and traverses to the last column and sorts.
def general_sort(list):
    for i in range(len(list[0])):
        list = sorted(list, key=lambda l: (l[i] is None, l[i]))
    return list


# This function provides access to a sandboxed PostgreSQL server.
# Index must be between 1 and 10 since there are 10 running servers available.
# This method is set to be removed as soon as a proper solution
# for load-balancing is provided.
def get_sandboxed_db(index):
    # Check if index is out of range
    if not 1 <= index <= 10:
        return None

    # Connect to PostgreSQL server
    connection = psycopg2.connect(database="postgres", user="postgres",
                                  password="postgres",
                                  host="worker_db_" + str(1), port="5432")
    # Initialize cursor to run queries
    cursor = connection.cursor()

    return cursor


class Score:
    # main_result represents the correct result gained through executing
    # the user(setter)-desired queries which will be compared to judge_result to
    # finally establish the rate and generate results.

    def __init__(self):

        # validators are methods (maybe changed to class in future) that
        # ensures the correctness of submission queries.
        # The validators execute by order of the list
        self.validators = []

        # Custom validator set
        self.validators = [{'f': self.shape_comparison, 'w': 0.1},
                           {'f': self.general_comparison, 'w': 0.9}]

    def set_validators(self, *args):
        # Every argument must be a dictionary consisting of:
        # 1. Name of the validator (function),
        # 2. Desired weight factor of the validator
        # Example: {'f':shape_comparison, 'w':0.5}
        for arg in args:
            self.validators.append(arg)
        return self.validators

    @staticmethod
    def shape_comparison(main_result, judge_result):
        return (len(main_result) == len(judge_result)) and \
               (len(main_result[0]) == len(judge_result[0]))

    @staticmethod
    def general_comparison(main_result, judge_result):
        main_result_sorted = general_sort(main_result)
        judge_result_sorted = general_sort(judge_result)
        judge_result_sorted_with_list_objects = [list(t) for t in judge_result]
        return main_result_sorted == judge_result_sorted_with_list_objects

    def get_score(self, main_result, judge_result):
        rate = 0
        for v in self.validators:
            rate += 100 * v['w'] * v['f'](main_result, judge_result)
        return int(rate)


def acquire_sandboxed_db():
    global sandboxed_db_trun
    free_cursor = get_sandboxed_db(sandboxed_db_trun)
    sandboxed_db_trun += 1
    if sandboxed_db_trun > 10:
        sandboxed_db_trun = 1
    return free_cursor


def problem_check_init_queries(problem):
    # Return values: code_status, "OK" or (if some exception happened)
    # the error.
    # code_status values:
    # 0: everything good
    # 2: error with queries(maybe in syntax maybe in logic)

    cursor = acquire_sandboxed_db()
    init_queries = problem.init_queries
    try:
        cursor.execute(init_queries)
        problem.init_queries_status = 0
        problem.init_queries_error_details = "OK"
        problem.save()
    except (Exception, psycopg2.Error) as error:
        problem.init_queries_status = 2
        problem.init_queries_error_details = error
        problem.save()
        return 2, error
    return 0, "OK"


def subproblem_check_queries(subproblem):
    # Return values: code_status, "OK" or (if some exception happened)
    # the error.
    # code_status values:
    # 0: everything good
    # 2: error with queries(maybe in syntax maybe in logic)

    cursor = acquire_sandboxed_db()
    problem = subproblem.problem
    init_queries = problem.init_queries
    dump_queries = subproblem.dump_queries
    final_query = subproblem.final_query
    try:
        execute_query(cursor, init_queries)
        problem.init_queries_status = 0
        problem.init_queries_error_details = "OK"
        problem.save()
    except (Exception, psycopg2.Error) as error:
        problem.init_queries_status = 2
        problem.init_queries_error_details = error
        problem.save()
        return 2, error
    try:
        execute_query(cursor, dump_queries)
        subproblem.dump_queries_status = 0
        subproblem.dump_queries_error_details = "OK"
        subproblem.save()
    except (Exception, psycopg2.Error) as error:
        subproblem.dump_queries_status = 2
        subproblem.dump_queries_error_details = error
        subproblem.save()
        return 2, error
    try:
        execute_query(cursor, final_query)
        record = cursor.fetchall()
        subproblem.result = record
        subproblem.final_query_status = 0
        subproblem.final_query_error_details = "OK"
        subproblem.save()
    except (Exception, psycopg2.Error) as error:
        subproblem.final_query_status = 2
        subproblem.final_query_error_details = error
        subproblem.save()
        return 2, error
    return 0, "OK"


def judge_subproblem_submission(score, subproblem_submission):
    # Return values: code_status, rate or (if some exception happened)
    # the error.
    # code_ status values:
    # 0: everything good
    # 1: in-process
    # 2: error with queries(mabye in sintax maybe in logic)
    cursor = acquire_sandboxed_db()
    subproblem = subproblem_submission.subproblem
    problem = subproblem.problem
    init_queries = problem.init_queries
    dump_queries = subproblem.dump_queries
    input_query = subproblem_submission.input_query
    try:
        execute_query(cursor, init_queries)
        problem.init_queries_status = 0
        problem.init_queries_error_details = "OK"
        problem.save()
    except (Exception, psycopg2.Error) as error:
        problem.init_queries_status = 2
        problem.init_queries_error_details = error
        problem.save()
        return 2, error
    try:
        execute_query(cursor, dump_queries)
        subproblem.dump_queries_status = 0
        subproblem.dump_queries_error_details = "OK"
        subproblem.save()
    except (Exception, psycopg2.Error) as error:
        subproblem.dump_queries_status = 2
        subproblem.dump_queries_error_details = error
        subproblem.save()
        return 2, error
    try:
        execute_query(cursor, input_query)
        record = cursor.fetchall()
        subproblem_submission.result = record
        subproblem_submission.input_query_error_details = "OK"
        subproblem_submission.save()
    except (Exception, psycopg2.Error) as error:
        subproblem_submission.input_query_status = 2
        subproblem_submission.input_query_error_details = error
        subproblem_submission.save()
        return 2, error

    main_result = subproblem.result
    judge_result_string = [[str(column) if column is not None else column
                            for column in row] for row in subproblem_submission.result]
    rate = score.get_score(main_result, judge_result_string)

    subproblem_submission.input_query_status = 0
    subproblem_submission.rate = rate
    subproblem_submission.save()
    return 0, rate


def execute_query(cursor, query):
    if query != "":
        cursor.execute(query)


def judge_submission(submission_index):
    score = Score()
    submission = submissions[submission_index]
    status = subproblem_submission_generator(submission)
    if status:
        # The submission file had incorrect structure.
        # The rate of submission had set to zero and other settings had
        # configured, so nothing is need except ending the judge_submission.
        return

    problem = Problem.objects.get(id=submission.problem_id)
    # Return values: code_status, record or (if some exception happened)
    # the error.
    # code_ status values:
    # 0: everything good
    # 1: in-process
    # 2: error with queries(mabye in sintax maybe in logic)

    subproblem_submissions = SubProblemSubmission.objects.filter(
        submission_id=submission.id)
    final_rate = 0
    error_existence_in_subproblems_submissions = False
    for instance in subproblem_submissions:
        judge_status, judge_body = judge_subproblem_submission(score, instance)
        if judge_status:
            final_rate += 0
            error_structure = "subproblem#" + str(instance.subproblem.index) + "\n" + str(judge_body) + "\n"
            submission.input_query_error_details += error_structure
            error_existence_in_subproblems_submissions = True
        else:
            final_rate += judge_body
    submission.rate = final_rate / subproblem_submissions.__len__()
    if error_existence_in_subproblems_submissions:
        submission.input_query_status = 2
    else:
        submission.input_query_status = 0
    submission.save()
    submissions.pop(submission_index)


def server_judge_submission_process(submission_index):
    threading.Thread(target=judge_submission, args=(submission_index,)).start()


def subproblem_submission_generator(submission):
    try:
        subproblem_submissions = re.split("--Section\d+",
                                          submission.input_query)
        subproblem_submissions.pop(0)
        subproblems = Problem.objects.get(
            id=submission.problem_id).subproblem_set.all().order_by('index')

        instances = []
        for i in range(subproblems.__len__()):
            instances.append(
                SubProblemSubmission.objects.create(
                    subproblem_id=subproblems[i].id,
                    submission_id=submission.id,
                    input_query=subproblem_submissions[i])
            )
    except:
        submission.input_query_status = 2
        submission.input_query_error_details = "Incorrect file structure"
        submission.rate = 0
        submission.save()
        return 2
    for instance in instances:
        instance.input_query_status = 1
        instance.save()
    return 0


submissions = []
sandboxed_db_trun = 1

# How to judge an uploaded Submission:
# 1.Save it in database.
# 2.Also add it to submissions list.
# 3.Call a server_judge_submission_process to judge it with submission index in the submissions
# list as argument.
# Example:
# test_submission = Submission.objects.get(pk=1)
# submissions.append(test_submission)
# server_judge_submission_process(submissions.__len__()-1)
