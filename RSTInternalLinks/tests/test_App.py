import os
from unittest.mock import patch
import RSTInternalLinks.app as app

class TestApp():
    def test_main(self):
        # main requires an existing file
        file_path = 'somefile.rst'
        with open(file_path, mode='w') as testfile:
            testfile.write('')

        # main should call parse of App
        with patch.object(app.App, 'parse') as mock_method:
            program = 'program'
            app.main([program, file_path])
            mock_method.assert_called_once_with(file_path)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                assert False, "Could not remove testfile."

    def test_parse(self):
        # plan:
        # create a file with some rst content
        # parse it
        # check if the result is as expected
        pass
