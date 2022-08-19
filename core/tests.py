from django.test import TestCase

from .scoring_system import Score, general_sort


# Scoring_system tests
class ScoreClassTest(TestCase):

    def test_general_sort_on_int_values(self):
        list1 = [[1, 5, 3], [4, 3, 6]]
        # print(genera_lsort(list1))
        self.assertSequenceEqual(general_sort(list1), [[1, 5, 3], [4, 3, 6]])

    def test_general_sort_on_int_values_with_duplicates(self):
        list1 = [[4, 3, 6], [1, 2, 6], [1, 1, 5]]
        self.assertSequenceEqual(general_sort(list1), [[1, 1, 5], [1, 2, 6],
                                                       [4, 3, 6]])

    def test_general_sort_special_sample1(self):
        list1 = [[1, 5, 3, 2], [4, 3, 6, 1]]
        self.assertSequenceEqual(general_sort(list1), [[4, 3, 6, 1],
                                                       [1, 5, 3, 2]])

    def test_general_sort_on_string_values(self):
        list1 = [['monkey', 'banana'], ['tiger', 'apple']]
        self.assertSequenceEqual(general_sort(list1), [['tiger', 'apple'],
                                                       ['monkey', 'banana']])

    def test_general_sort_on_string_with_duplicates(self):
        list1 = [['monkey', 'banana'], ['tiger', 'apple'], ['monkey', 'apple']]
        self.assertSequenceEqual(general_sort(list1), [['monkey', 'apple'],
                                                       ['tiger', 'apple'], ['monkey', 'banana']])

    def test_shape_comparison_valid_data(self):
        score = Score()
        l1 = [[1, 2], [4, 5], [4, 6]]
        l2 = [[1, 2], [4, 4], [3, 6]]
        self.assertIs(score.shape_comparison(l1, l2), True)

    def test_shape_comparison_invalid_data(self):
        score = Score()
        l1 = [[1, 2], [4, 5], [4, 6]]
        l2 = [[1, 2], [4, 5]]
        self.assertIs(score.shape_comparison(l1, l2), False)

    def test_general_comparison_valid_data(self):
        score = Score()
        l1 = [[1, 2], [4, 5], [4, 6]]
        l2 = [[1, 2], [4, 5], [4, 6]]
        self.assertIs(score.general_comparison(l1, l2), True)

    def test_general_comparison_invalid_data(self):
        score = Score()
        l1 = [[1, 2], [4, 5], [4, 6]]
        l2 = [[1, 2], [3, 5], [4, 6]]
        self.assertIs(score.general_comparison(l1, l2), False)

    def test_score_correct_query(self):
        list1 = [[1, 5, 3, 2], [4, 3, 6, 1]]
        score = Score()
        score.set_validators({'f': score.shape_comparison, 'w': 0.1},
                             {'f': score.general_comparison, 'w': 0.9})
        self.assertIs(score.get_score([[4, 3, 6, 1], [1, 5, 3, 2]], list1), 100)

    def test_score_incorrect_query(self):
        list1 = [[1, 5, 3, 2], [4, 3, 6, 1]]
        score = Score()
        score.set_validators({'f': score.shape_comparison, 'w': 0.1},
                             {'f': score.general_comparison, 'w': 0.9})
        self.assertIs(score.get_score([[1, 5, 3, 2]], list1), 0)

    def test_score_with_equal_shapes_only(self):
        list1 = [[1, 5, 3, 2], [4, 3, 6, 1]]
        score = Score()
        score.set_validators({'f': score.shape_comparison, 'w': 0.1},
                             {'f': score.general_comparison, 'w': 0.9})
        self.assertIs(score.get_score([[4, 2, 6, 1], [1, 5, 3, 2]], list1), 10)
