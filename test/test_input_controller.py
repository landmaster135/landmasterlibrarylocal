# Library by default
# nothing
# Library by third party
import pytest
# Library by landmasterlibrarylocal
from src.landmasterlibrarylocal.input_controller import check_whether_sjis_exists, repeat_input_with_multi_choices

class Test_input_controller:
    def test_check_whether_sjis_exists_1_1(self):
        target_str_list = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
        actual = check_whether_sjis_exists(target_str_list)
        expected = False
        assert actual == expected

    def test_check_whether_sjis_exists_1_2(self):
        target_str_list = ['abcdefghijklXYZ', '1234']
        actual = check_whether_sjis_exists(target_str_list)
        expected = False
        assert actual == expected

    def test_check_whether_sjis_exists_1_3(self):
        target_str_list = ['abcdefghijklXYZ', 'あss']
        actual = check_whether_sjis_exists(target_str_list)
        expected = True
        assert actual == expected

    def test_check_whether_sjis_exists_1_4(self):
        target_str_list = ['abcdefghijklXYZ', '！']
        actual = check_whether_sjis_exists(target_str_list)
        expected = True
        assert actual == expected

    def test_check_whether_sjis_exists_1_5(self):
        target_str_list = ['ー', '！']
        actual = check_whether_sjis_exists(target_str_list)
        expected = True
        assert actual == expected

    def test_check_whether_sjis_exists_2_1(self):
        target_str_list = [1, 'あss']
        with pytest.raises(TypeError) as e:
            actual = check_whether_sjis_exists(target_str_list)

    def test_check_whether_sjis_exists_2_2(self):
        target_str_list = ['abcdefghijklXYZ', True]
        with pytest.raises(TypeError) as e:
            actual = check_whether_sjis_exists(target_str_list)

    def test_check_whether_sjis_exists_2_3(self):
        target_str_list = [str, True]
        with pytest.raises(TypeError) as e:
            actual = check_whether_sjis_exists(target_str_list)

    def test_check_whether_sjis_exists_3_1(self):
        with pytest.raises(TypeError) as e:
            actual = check_whether_sjis_exists("asdfg")

    def test_check_whether_sjis_exists_3_2(self):
        with pytest.raises(TypeError) as e:
            actual = check_whether_sjis_exists()

    def test_repeat_input_with_multi_choices_1_1(self, monkeypatch):
        first_message = "Select!"
        choice_list = ["A", "B", "C"]
        monkeypatch.setattr('builtins.input', lambda _: "A")
        actual = repeat_input_with_multi_choices(first_message, choice_list)
        expected = choice_list[0]
        assert actual == expected

    def test_repeat_input_with_multi_choices_1_2(self, monkeypatch):
        first_message = "Select!"
        choice_list = ["A", "B", "C"]
        monkeypatch.setattr('builtins.input', lambda _: "B")
        actual = repeat_input_with_multi_choices(first_message, choice_list)
        expected = choice_list[1]
        assert actual == expected

    def test_repeat_input_with_multi_choices_1_3(self, monkeypatch):
        first_message = "Select!"
        choice_list = ["A", "B", "C"]
        monkeypatch.setattr('builtins.input', lambda _: "C")
        actual = repeat_input_with_multi_choices(first_message, choice_list)
        expected = choice_list[2]
        assert actual == expected

    def test_repeat_input_with_multi_choices_2_1(self, monkeypatch):
        first_message = 1234
        choice_list = ["A", "B", "C"]
        monkeypatch.setattr('builtins.input', lambda _: "A")
        with pytest.raises(TypeError) as e:
            actual = repeat_input_with_multi_choices(first_message, choice_list)

    def test_repeat_input_with_multi_choices_2_2(self, monkeypatch):
        first_message = "Select!"
        choice_list = "A"
        monkeypatch.setattr('builtins.input', lambda _: "A")
        with pytest.raises(TypeError) as e:
            actual = repeat_input_with_multi_choices(first_message, choice_list)

    def test_repeat_input_with_multi_choices_2_3(self, monkeypatch):
        first_message = "Select!"
        choice_list = ["A", 1, "C"]
        monkeypatch.setattr('builtins.input', lambda _: "A")
        with pytest.raises(TypeError) as e:
            actual = repeat_input_with_multi_choices(first_message, choice_list)

    def test_repeat_input_with_multi_choices_3_1(self, monkeypatch):
        first_message = 1234
        monkeypatch.setattr('builtins.input', lambda _: "A")
        with pytest.raises(TypeError) as e:
            actual = repeat_input_with_multi_choices(first_message)

    def test_repeat_input_with_multi_choices_3_2(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "A")
        with pytest.raises(TypeError) as e:
            actual = repeat_input_with_multi_choices()
