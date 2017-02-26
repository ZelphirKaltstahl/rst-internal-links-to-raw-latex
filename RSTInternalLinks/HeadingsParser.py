import re

class HeadingsParser():
    """
    The HeadingParser parses the document for headings.

    NOT YET: converts headings to raw latex headings in the correct way, so that they can be referrenced to later
    see https://www.sharelatex.com/learn/Sections_and_chapters for info about the levels"""

    def __init__(self):
        super().__init__()

        self.title = None
        self.subtitle = None
        self.heading = []

        # regexes
        self.title_start_marker_regex = re.compile(r'[=]{3,}')
        self.title_end_marker_regex = re.compile(r'[=]{3,}')
        self.title_content_regex = re.compile(
            r'''
            ^                               # beginning of line
            [ ]                             # one whitespace
            [A-Za-z0-9äöüÄÖÜ]+              # alphanumerical string, no whitespace
            (?P<title>[A-Za-z0-9äöüÄÖÜ ]+)  # alphanumerical string, whitespace ok
            [A-Za-z0-9äöüÄÖÜ]+              # alphanumerical string, no whitespace
            [ ]                             # one whitespace
            $                               # end of line
            ''', re.VERBOSE|re.UNICODE
        )

        self.subtitle_start_marker_regex = re.compile(r'[-]{3,}')
        self.subtitle_end_marker_regex = re.compile(r'[-]{3,}')
        self.subtitle_content_regex = re.compile(
            r'''
            ^                                  # beginning of line
            [ ]                                # one whitespace
            [A-Za-z0-9äöüÄÖÜ]+                 # alphanumerical string, no whitespace
            (?P<subtitle>[A-Za-z0-9äöüÄÖÜ ]+)  # alphanumerical string, whitespace ok
            [A-Za-z0-9äöüÄÖÜ]+                 # alphanumerical string, no whitespace
            [ ]                                # one whitespace
            $                                  # end of line
            ''', re.VERBOSE|re.UNICODE
        )

        # Headings cannot begin with whitespace
        self.h_content_regex = re.compile(
            r'''
            ^                        # beginning of line
            [A-Za-z0-9äöüÄÖÜß(]       # alphanum
            [A-Za-z0-9äöüÄÖÜß,() -]*  # alphanum or space
            [A-Za-z0-9äöüÄÖÜß)]       # alphanum
            $                        # end of line
            ''', re.VERBOSE|re.UNICODE
        )

        # chapter
        self.h1_underlining_regex = re.compile(r'[=]{3,}')
        # section
        self.h2_underlining_regex = re.compile(r'[-]{3,}')
        # subsection
        self.h3_underlining_regex = re.compile(r'[~]{3,}')
        # subsubsection
        self.h4_underlining_regex = re.compile(r'[\^]{3,}')
        # paragraph
        self.h5_underlining_regex = re.compile(r'[*]{3,}')
        # subparagraph
        self.h6_underlining_regex = re.compile(r'[.]{3,}')

    def parse(self, rst_file_content):
        self.title = self.find_title(rst_file_content)
        self.subtitle_content_regex = self.find_subtitle(rst_file_content)
        return self.find_heading_labels(rst_file_content)

    def find_title(self, rst_file_content):
        print('looking for title ...')
        title = None
        for lineno, line in enumerate(rst_file_content):
            previous_line = ""
            if lineno > 0:
                previous_line = rst_file_content[lineno - 1]

            next_line = ""
            if lineno < len(rst_file_content) - 1:
                next_line = rst_file_content[lineno + 1]

            # title
            if (
                self.title_start_marker_regex.match(previous_line) and
                self.title_end_marker_regex.match(next_line) and
                (
                    len(self.title_start_marker_regex.match(previous_line).group()) ==
                    len(self.title_end_marker_regex.match(next_line).group())
                ) and
                self.title_content_regex.match(line) and
                not title
            ):
                title = self.title_content_regex.match(line).group('title')
                print('title is:|', title, '|', sep='')
                break

        if not title: print('Could not find title in document.')
        return title

    def find_subtitle(self, rst_file_content):
        print('looking for subtitle ...')
        subtitle = None
        for lineno, line in enumerate(rst_file_content):
            previous_line = ""
            if lineno > 0:
                previous_line = rst_file_content[lineno - 1]

            next_line = ""
            if lineno < len(rst_file_content) - 1:
                next_line = rst_file_content[lineno + 1]

            if (
                self.subtitle_start_marker_regex.match(previous_line) and
                self.subtitle_end_marker_regex.match(next_line) and
                (
                    len(self.subtitle_start_marker_regex.match(previous_line).group()) ==
                    len(self.subtitle_end_marker_regex.match(next_line).group())
                ) and
                self.subtitle_content_regex.match(line) and
                not subtitle
            ):
                subtitle = self.subtitle_content_regex.match(line).group('subtitle')
                print('subtitle is:|', subtitle, '|', sep='')
                break

        if not subtitle: print('Could not find subtitle in document.')
        return subtitle

    def find_heading_labels(self, rst_file_content):
        print('looking for headings ...')
        headings_dict = {}
        # heading_labels = []
        for lineno, line in enumerate(rst_file_content):
            # print('current line:', lineno)
            # print('current line:', line)
            # if line.startswith("Schlussfolgerungen"):
            #     print('current line:', line)
                
            previous_line = ""
            if lineno > 0:
                previous_line = rst_file_content[lineno - 1]

            next_line = ""
            if lineno < len(rst_file_content) - 1:
                next_line = rst_file_content[lineno + 1]

            # headings level 1
            # print('looking for h1 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h1_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h1_underlining_regex.match(next_line).group())
            ):
                print('found a h1:', line)
                print('replacing chapter heading')
                headings_dict[line] = self.heading_to_label(line, 'chapter')
                # heading_labels.append(self.heading_to_label(line, 'chapter'))
                rst_file_content[lineno] = ':raw-latex:`\chapter{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'chapter') + '}`'

            # headings level 2
            # print('looking for h2 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h2_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h2_underlining_regex.match(next_line).group())
            ):
                print('found a h2:', line)
                headings_dict[line] = self.heading_to_label(line, 'section')
                # heading_labels.append(self.heading_to_label(line, 'section'))
                rst_file_content[lineno] = ':raw-latex:`\section{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'section') + '}`'

            # headings level 3
            # print('looking for h3 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h3_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h3_underlining_regex.match(next_line).group())
            ):
                print('found a h3:', line)
                # heading_labels.append(self.heading_to_label(line, 'subsection'))
                headings_dict[line] = self.heading_to_label(line, 'subsection')
                rst_file_content[lineno] = ':raw-latex:`\subsection{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'subsection') + '}`'

            # headings level 4
            # print('looking for h4 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h4_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h4_underlining_regex.match(next_line).group())
            ):
                print('found a h4:', line)
                # heading_labels.append(self.heading_to_label(line, 'subsubsection'))
                headings_dict[line] = self.heading_to_label(line, 'subsubsection')
                rst_file_content[lineno] = ':raw-latex:`\subsubsection{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'subsubsection') + '}`'

            # headings level 5
            # print('looking for h5 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h5_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h5_underlining_regex.match(next_line).group())
            ):
                print('found a h5:', line)
                # heading_labels.append(self.heading_to_label(line, 'paragraph'))
                headings_dict[line] = self.heading_to_label(line, 'paragraph')
                rst_file_content[lineno] = ':raw-latex:`\paragraph{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'paragraph') + '}`'

            # headings level 6
            # print('looking for h6 ...')
            if (
                (previous_line.isspace() or previous_line == '') and
                self.h_content_regex.match(line) and
                self.h6_underlining_regex.match(next_line) and
                len(self.h_content_regex.match(line).group()) == len(self.h6_underlining_regex.match(next_line).group())
            ):
                print('found a h6:', line)
                # heading_labels.append(self.heading_to_label(line, 'subparagraph'))
                headings_dict[line] = self.heading_to_label(line, 'subparagraph')
                rst_file_content[lineno] = ':raw-latex:`\subparagraph{' + line + '}`'
                rst_file_content[lineno + 1] = ':raw-latex:`\label{' + self.heading_to_label(line, 'subparagraph') + '}`'

        return headings_dict

    def heading_to_label(self, heading_text, level):
        heading_text = heading_text.lower()
        replaced_chars = {
            ' ': '-',
            '(': '',
            ')': ''
        }
        for key,value in replaced_chars.items():
            heading_text = heading_text.replace(key, value)

        return '{0}:{1}'.format(level, heading_text)

        # self.chapter_delimiter_regex = re.compile(r'={3,}')          # =============
        # self.section_delimiter_regex = re.compile(r'-{3,}')          # -------------
        # self.subsection_delimiter_regex = re.compile(r'~{3,}')       # ~~~~~~~~~~~~~
        # self.subsubsection_delimiter_regex = re.compile(r'\^{3,}')   # ^^^^^^^^^^^^^
        # self.heading_text_regex = re.compile(
        #     r'''
        #     ^
        #     \s*
        #     (?P<title_text>
        #         [a-zA-Z0-9]
        #         [a-zA-Z0-9_ -]*
        #         [a-zA-Z0-9]
        #     )
        #     \s*
        #     $''',
        #     re.VERBOSE)

        # self.heading_keys = []

#     def parse_headings(self, rst_file_content):
#         for lineno, line in enumerate(rst_file_content):
#
#             # search for title
#             if self.title_delimiter_regex.search(line) is not None:
#                 if (lineno >= 2):
#                     if (
#                         self.title_delimiter_regex.search(rst_file_content[lineno - 2]) is not None and
#                         self.heading_text_regex.search(rst_file_content[lineno - 1]) is not None
#                     ):
#                         title_text = self.heading_text_regex.findall(rst_file_content[lineno - 1])[0].strip()
#                         self.heading_keys.append(re.sub('\s+', '-', title_text.lower()))
#                         print('[DEBUG:HEADINGS]', self.heading_keys)
#                         print('[DEBUG:HEADINGS] !!! found a title in the document:', title_text, sep='')
#
#             # TODO: elif subtitle
