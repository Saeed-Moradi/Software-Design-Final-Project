from django.contrib.postgres.fields import ArrayField
from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=30, default="")
    text = models.TextField(default="")
    number_of_subproblems = models.IntegerField(default=0)

    # This option determines who has set the problem(-1 stands for admin(since
    # we don't have a single admin right now it will be -1. after configuration
    # of the admin panel the problem_setter_id will be -(admin_id)).
    problem_setter_id = models.EmailField(default="")

    # There are two general way to save dump(init) queries into database:
    # 1.List of init queries like create table, insert data $ etc.
    # 2.Not a list but a single TextFiled with the exact string convention user used.
    # I decide to choose the second one because it has better
    # user-experience(user feel better when we save his/her exact file
    # structure), Although the first one maybe makes more sense and more classified.

    # Status remains that the init_queries has been executed correctly or no or are
    # in-progress state yet;
    # definition of status values:
    # -1: no query has been uploaded yet(default)
    # 0: OK(the queries executed correctly)
    # 1: the uploaded queries are processing...
    # 2: some error(not specific at the current time(at this situations the
    # error_details field hold the errors, in previous situations this field
    # value equals to "OK").
    init_queries_status = models.IntegerField(default=-1)
    init_queries = models.TextField(default="")
    init_queries_error_details = models.TextField(default="")

    def __str__(self):
        return "title={0}, problem_setter_id={1}".format(self.title, self.problem_setter_id)


# TestCase entity was deleted for now, unless finding it necessary to implement
# in future. Also the definition of TestCase has been changed through time but
# the code is old yet.

# class TestCase(models.Model):
#    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
#
#    # Testcase-queries: the queries that are related to Testcase & necessary
#    # to define a specific TestCase
#    desired_queries = ArrayField(models.TextField(), default=list)
#
#    # result of a the desired_queries will be saved into a 2d array of Texts
#    # Text is a general type for other fields like integer, float & etc.
#    output = ArrayField(ArrayField(models.TextField()))


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contender_id = models.EmailField(default="")

    # Status remains that the input_queries has been executed correctly or no or are
    # in-progress state yet;
    # definition of status values:
    # -1: no query has been uploaded yet(default)
    # 0: OK(the queries executed correctly)
    # 1: the uploaded queries are processing...
    # 2: some error(not specific at the current time(at this situations the
    # error_details field hold the errors, in previous situations this field
    # value equals to "OK").

    input_query_status = models.IntegerField(default=-1)
    input_query = models.TextField(default="")
    input_query_error_details = models.TextField(default="")

    # Submission rate will be avg of it's SubProblemSubmission(s).
    rate = models.IntegerField(default=-1)

    def __str__(self):
        return "contender_id={0}, problem: {1}; rate={2}".format(
            self.contender_id, self.problem, self.rate)


class SubProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, default="")
    text = models.TextField(default="")

    # every problem may have zero or more subproblems which problem setter can
    # initialize or change or delete. We need to save index for each subproblem
    # Although we save id either. Purpose of saving index is to know how to
    # match every submission's subqueries into subproblems.

    index = models.IntegerField()

    # There are two general way to save dump(init) queries into database:
    # 1.List of init queries like create table, insert data $ etc.
    # 2.Not a list but a single TextFiled with the exact string convention user used.
    # I decide to choose the second one because it has better
    # user-experience(user feel better when we save his/her exact file
    # structure), Although the first one maybe makes more sense and more classified.

    # Status remains that the dump_queries has been executed correctly or no or are
    # in-progress state yet.
    # definition of status values:
    # -1: no query has been uploaded yet(default)
    # 0: OK(the queries executed correctly)
    # 1: the uploaded queries are processing...
    # 2: some error(not specific at the current time(at this situations the
    # error_details field hold the errors, in previous situations this field
    # value equals to "OK").

    dump_queries_status = models.IntegerField(default=-1)
    dump_queries = models.TextField(default="")
    dump_queries_error_details = models.TextField(default="")

    # Here is query(queries) that will be set to be judge and compare with
    # user submission's queries.

    # Status remains that the dump_queries has been executed correctly or no or are
    # in-progress state yet.
    # definition of status values:
    # -1: no query has been uploaded yet(default)
    # 0: OK(the queries executed correctly)
    # 1: the uploaded queries are processing...
    # 2: some error(not specific at the current time(at this situations the
    # error_details field hold the errors, in previous situations this field
    # value equals to "OK").

    final_query_status = models.IntegerField(default=-1)
    final_query = models.TextField(default="")
    final_query_error_details = models.TextField(default="")

    # The result of executing the final_query.
    # result of a the final_query will be saved as a 2d array of Texts.
    # Text is a general type for other fields like integer, float & etc.

    result = ArrayField(ArrayField(models.TextField()), default=list)

    def __str__(self):
        return "problem:{0}; title={1}, index={2}".format(self.problem,
                                                          self.title, self.index)


class SubProblemSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    subproblem = models.ForeignKey(SubProblem, on_delete=models.CASCADE)

    # Status remains that the input_queries has been executed correctly or no or are
    # in-progress state yet.
    # definition of status values:
    # -1: no query has been uploaded yet(default)
    # 0: OK(the queries executed correctly)
    # 1: the uploaded queries are processing...
    # 2: some error(not specific at the current time(at this situations the
    # error_details field hold the errors, in previous situations this field
    # value equals to "OK").

    input_query_status = models.IntegerField(default=-1)
    input_query = models.TextField(default="")
    input_query_error_details = models.TextField(default="")

    rate = models.IntegerField(default=-1)

    def __str__(self):
        return "submission#{0}, subproblem#{1}: rate={2}".format(
            self.submission, self.subproblem, self.rate)
