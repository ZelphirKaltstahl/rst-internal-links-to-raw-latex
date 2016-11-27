import sys
import os

class FileWriter():
    """writes resulting rst files"""

    def __init__(self):
        super().__init__()

    def write(self, rst_out_file_path, rst_file_content):
        try:
            with open(rst_out_file_path, 'w') as opened_file:
                opened_file.write(os.linesep.join(rst_file_content))
        except IOError:
            sys.exit('Could not write file. (IOError)')
        except OSError:
            sys.exit('Could not write file. (OSError)')
        except FileNotFoundError:
            sys.exit('Could not write file. (FileNotFoundError)')
        except Exception as e:
            raise e
            sys.exit('An unknown error occurred when trying to write the output file.')
