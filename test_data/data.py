# How to add data to database with django shell: run below command in project
# root directory...
# sudo docker-compose exec -T web python manage.py shell < test_data/data.py

from core.models import Problem, Submission, Subproblem, SubproblemSubmission

p = Problem.objects
s = Submission.objects
sp = Subproblem.objects
sp_s = SubproblemSubmission.objects
p.create(title="problem #1", text="find x1", problem_setter_id=1,
         init_queries="create table test1(id int,\
                                               name varchar(20));\ninsert\
                                               into test1(id, name) values(1,\
                                               'ali');",
         );

p.create(title="problem #2", text="find x2", problem_setter_id=2,
         init_queries="create table tes2(id int,\
                                               name varchar(20));\ninsert\
                                               into test2(id, name) values(1,\
                                               'ali');",
         );
p.create(title="problem #3", text="find x3",
         init_queries="create table test3(id int,\
                                               name varchar(20));\ninsert\
                                               into test3(id, name) values(1,\
                                               'ali');",
         );
p.get(pk=1).subproblem_set.create(dump_queries="insert into test1(id, name)\
                                  values(2, 'zahra');", final_query="select\
                                  * from test1;", index=1)
p.get(pk=1).subproblem_set.create(final_query="select * from test1;", index=2)

p.get(pk=1).submission_set.create(contender_username="yasin",
                                  input_query="--Section1\n\
                                  sekect * from\
                                  test1\n\
                                  --Section2\n\
                                  select * from test1")

sp_s.create(subproblem=sp.get(id=1), submission=s.get(id=1), input_query=
"sekect * from test1;")
sp_s.create(subproblem=sp.get(id=2), submission_id=1, input_query=
"select * from test1;")
