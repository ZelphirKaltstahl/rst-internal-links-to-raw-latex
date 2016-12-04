import re

class HeadingsParser():
    """converts headings to raw latex headings in the correct way, so that they can be referrenced to later
    see https://www.sharelatex.com/learn/Sections_and_chapters for info about the levels"""

    def __init__(self):
        super().__init__()
        self.title_delimiter_regex = re.compile(r'={3,}')            # ============= over+below
        self.subtitle_delimiter_regex = re.compile(r'-{3,}')         # ------------- over+below
        self.chapter_delimiter_regex = re.compile(r'={3,}')          # =============
        self.section_delimiter_regex = re.compile(r'-{3,}')          # -------------
        self.subsection_delimiter_regex = re.compile(r'~{3,}')       # ~~~~~~~~~~~~~
        self.subsubsection_delimiter_regex = re.compile(r'\^{3,}')   # ^^^^^^^^^^^^^
        self.heading_text_regex = re.compile(
            r'''
            ^
            \s*
            (?P<title_text>
                [a-zA-Z0-9]
                [a-zA-Z0-9_ -]*
                [a-zA-Z0-9]
            )
            \s*
            $''',
            re.VERBOSE)

        self.heading_keys = []

    def parse_headings(self, rst_file_content):
        for lineno, line in enumerate(rst_file_content):

            # search for title
            if self.title_delimiter_regex.search(line) is not None:
                if (lineno >= 2):
                    if (
                        self.title_delimiter_regex.search(rst_file_content[lineno - 2]) is not None and
                        self.heading_text_regex.search(rst_file_content[lineno - 1]) is not None
                    ):
                        title_text = self.heading_text_regex.findall(rst_file_content[lineno - 1])[0].strip()
                        self.heading_keys.append(re.sub('\s+', '-', title_text.lower()))
                        print('[DEBUG:HEADINGS]', self.heading_keys)
                        print('[DEBUG:HEADINGS] !!! found a title in the document:', title_text, sep='')

            # TODO: elif subtitle
