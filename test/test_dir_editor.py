# Library by default
import os
import sys
import shutil
import platform
# Library by third party
import pytest
# Library by landmasterlibrarylocal
from src.landmasterlibrarylocal.dir_editor import *

class Test_dir_editor:
    def test_generate_file_name_1_1(self):
        dir_name = "usr/app"
        sep = "/"
        filename_with_ext = "test1.txt"
        actual = generate_file_name(dir_name, sep, filename_with_ext)
        expected = f'{dir_name}{sep}{filename_with_ext}'
        assert actual == expected

    def test_generate_file_name_1_2(self):
        dir_name = "usr/app"
        sep = "/"
        filename_with_ext = "Dockerfile"
        actual = generate_file_name(dir_name, sep, filename_with_ext)
        expected = f'{dir_name}{sep}{filename_with_ext}'
        assert actual == expected

    def test_generate_file_name_2_1(self):
        dir_name = "usr/app"
        sep = "/"
        filename_with_ext = 1
        with pytest.raises(TypeError) as e:
            actual = generate_file_name(dir_name, sep, filename_with_ext)

    def test_generate_file_name_2_2(self):
        dir_name = "usr/app"
        sep = 2
        filename_with_ext = "test1.txt"
        with pytest.raises(TypeError) as e:
            actual = generate_file_name(dir_name, sep, filename_with_ext)

    def test_generate_file_name_2_3(self):
        dir_name = 3
        sep = "/"
        filename_with_ext = "test1.txt"
        with pytest.raises(TypeError) as e:
            actual = generate_file_name(dir_name, sep, filename_with_ext)

    def test_generate_file_name_3_1(self):
        dir_name = "usr/app"
        sep = "/"
        with pytest.raises(TypeError) as e:
            actual = generate_file_name(dir_name, sep)

    def test_generate_file_name_3_2(self):
        dir_name = "usr/app"
        with pytest.raises(TypeError) as e:
            actual = generate_file_name(dir_name)

    def test_generate_file_name_3_3(self):
        with pytest.raises(TypeError) as e:
            actual = generate_file_name()

    def test_generate_file_name_4_1(self):
        dir_name = "usr/app/test2.csv"
        sep = "/"
        filename_with_ext = "test1.txt"
        actual = generate_file_name(dir_name, sep, filename_with_ext)
        expected = f'{dir_name}{sep}{filename_with_ext}'
        assert actual == expected

class Test_make_directory:
    test_dir = "test_data"
    does_test_dir_exist = os.path.isdir(f'{os.getcwd()}/{test_dir}')

    @pytest.mark.skipif(does_test_dir_exist == False, reason=f'current directory is not "{test_dir}"')
    def test_make_directory_1_1(self, monkeypatch):
        func_name = sys._getframe().f_code.co_name
        dir_name = "./test_data"
        sep = "/"
        filename_with_ext = "test_スクショ_01_01.jpg"
        monkeypatch.setattr('builtins.input', lambda _: func_name)
        file_name = f'{dir_name}{sep}{filename_with_ext}'
        made_path = make_directory(file_name)
        actual = os.path.isdir(made_path)
        expected = True
        shutil.rmtree(made_path)
        assert actual == expected

    @pytest.mark.skipif(does_test_dir_exist == False, reason=f'current directory is not "{test_dir}"')
    def test_make_directory_1_2(self, monkeypatch):
        func_name = sys._getframe().f_code.co_name
        dir_name = "./test_data"
        sep = "/"
        filename_with_ext = "test_screencapture_03_01_あ.mov"
        monkeypatch.setattr('builtins.input', lambda _: func_name)
        file_name = f'{dir_name}{sep}{filename_with_ext}'
        made_path = make_directory(file_name)
        actual = os.path.isdir(made_path)
        expected = True
        shutil.rmtree(made_path)
        assert actual == expected

    def test_make_directory_2_1(self, monkeypatch):
        func_name = sys._getframe().f_code.co_name
        monkeypatch.setattr('builtins.input', lambda _: func_name)
        file_name = 123
        with pytest.raises(TypeError) as e:
            made_path = make_directory(file_name)


class Test_decide_seperator:
    def test_decide_seperator_1_1(self, mocker):
        pf = 'Windows'
        mocker.patch.object(platform, 'system', return_value=pf)
        actual = decide_seperator()
        expected = '\\'
        assert actual == expected

    def test_decide_seperator_1_2(self, mocker):
        pf = 'Darwin'
        mocker.patch.object(platform, 'system', return_value=pf)
        actual = decide_seperator()
        expected = '/'
        assert actual == expected

    def test_decide_seperator_1_3(self, mocker):
        pf = 'Linux'
        mocker.patch.object(platform, 'system', return_value=pf)
        actual = decide_seperator()
        expected = '/'
        assert actual == expected

    def test_decide_seperator_2_1(self, mocker):
        pf = 'test'
        mocker.patch.object(platform, 'system', return_value=pf)
        with pytest.raises(OSError) as e:
            actual = decide_seperator()
