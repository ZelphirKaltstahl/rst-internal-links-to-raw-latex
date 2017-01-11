import sys
import os.path

import RSTInternalLinks.FileReader
import RSTInternalLinks.FileWriter
import RSTInternalLinks.RSTInternalLinksParser
import RSTInternalLinks.HeadingsParser


class App():
    """application class"""

    def __init__(self):
        super().__init__()

        self.file_reader = RSTInternalLinks.FileReader.FileReader()
        self.file_writer = RSTInternalLinks.FileWriter.FileWriter()
        self.headings_parser = RSTInternalLinks.HeadingsParser.HeadingsParser()

    def parse(self, rst_file_path):
        print('Now reading input file ...')
        rst_file_content = self.file_reader.read_file(rst_file_path)

        print('Parsing input file for headings ...')
        headings_dict = self.headings_parser.parse(rst_file_content)
        print('[DEBUG]: HEADINGS FOUND:')
        for key, value in headings_dict.items():
            print('KEY:|{key}|, VALUE:|{value}|'.format(key=key, value=value))

        print('Parsing input file for references ...')
        self.rst_parser = RSTInternalLinks.RSTInternalLinksParser.RSTInternalLinksParser(headings_dict)
        rst_file_content = self.rst_parser.parse(rst_file_content)

        print('Writing output file ...')
        self.file_writer.write(rst_file_path + '.out', rst_file_content)
        print('Successfully wrote output file.')


def print_help():
    print('call syntax:')
    print('python <program> <rst file>')


def main(params):
    if len(params) != 2:
        print_help()
    else:
        rst_file_path = params[1]
        if not os.path.isfile(rst_file_path):
            sys.exit('The file you specified does not exist or is not a file.')

        app = App()
        app.parse(rst_file_path)


if __name__ == '__main__':
    main(sys.argv)
