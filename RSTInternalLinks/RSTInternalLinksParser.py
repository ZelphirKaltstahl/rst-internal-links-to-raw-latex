import re

class RSTInternalLinksParser():
    """parses rst files and exchanges internal links with latex internal hyperlinks"""

    def __init__(self, headings):
        super().__init__()

        self.headings = headings

        self.rst_link_definition = re.compile(r'\.\. _(?P<link_key>[^\[\]_`:]+):', re.UNICODE)
        self.rst_link_multi_word = re.compile(
            r'''
            `       # literal backtick
            (?P<link_key>          # start of named group
            [a-zA-Z0-9ßäöüÄÖÜ() -]+  # letter or
                                   # number or
                                   # umlaut or
                                   # space or
                                   # dash
            )                      # end of named group
            `       # literal backtick
            _       # literal underscore
            ''', re.VERBOSE|re.UNICODE)

#         self.rst_anonymous_link_definition = re.compile(r'^\.\. __: .+$|^__ .+$')
#         self.internal_link_single_word_target = re.compile(
#             r'''
#             [\s^]+                    # at least one whitespace or beginning of
#                                       # the line
#
#             (?<!\.\. )                # not ".. " in front, because it would be
#                                       # a link definition and not a target.
#
#             (?<!``)                   # not double backtick in front because
#                                       # this is verbatim text of rst
#
#             _                         # the literal underscore
#
#             (?P<link_key>[^\[\]\s`]+) # the link key:
#                                       # no brackets [ ]
#                                       # no whitespace
#                                       # no backtick `
#             ''', re.VERBOSE)
#         self.internal_link_multi_word_target = re.compile(
#             r'[\s^]+_`(?P<link_key>[^\[\]`]+)`')
#         self.internal_link_single_word_reference = re.compile(
#             r'[\s^]+(?P<link_key>[^\[\]\s`]+)_(?!_)')
#         self.internal_link_multi_word_reference = re.compile(
#             r'[\s^]+`(?P<link_key>[^\[\]`]+)`_(?!_)')


    def parse(self, rst_file_content):
        found_rst_link_definitions_keys = self.find_link_definitions(rst_file_content)
        print('[DEBUG:Result] found link definition keys:', found_rst_link_definitions_keys)

        self.replace_heading_references(rst_file_content)

        return rst_file_content

#         for lineno, line in enumerate(rst_file_content):
#             if self.rst_anonymous_link_definition.search(line) is not None:
#                 continue
#
#             if self.rst_link_definition.search(line) is not None:
#                 continue
#
#             # SINGLE WORD TARGET
#             if self.internal_link_single_word_target.search(line) is not None:
#                 print('[DEBUG] single word target in:', line)
#                 line = self.replace_internal_single_word_targets(line, found_rst_link_definitions_keys)
#
#             # SINGLE WORD REFERENCE
#             if self.internal_link_single_word_reference.search(line) is not None:
#                 print('[DEBUG] single word reference in:', line)
#                 line = self.replace_internal_single_word_references(line, found_rst_link_definitions_keys)
#
#             # MULTI WORD TARGET
#             if self.internal_link_multi_word_target.search(line) is not None:
#                 print('[DEBUG] multi word target in:', line)
#                 line = self.replace_internal_multi_word_targets(line, found_rst_link_definitions_keys)
#
#             # MULTI WORD REFERENCE
#             if self.internal_link_multi_word_reference.search(line) is not None:
#                 print('[DEBUG] multi word reference in:', line)
#                 line = self.replace_internal_multi_word_references(line, found_rst_link_definitions_keys)
#
#             rst_file_content[lineno] = line
#
#
#         return rst_file_content



    def find_link_definitions(self, rst_file_content):
        rst_link_definitions_keys = []

        for lineno, line in enumerate(rst_file_content):
            if self.rst_link_definition.match(line):
                rst_link_definitions_keys.append(self.rst_link_definition.match(line).group('link_key'))

            # elif self.rst_anonymous_link_definition.match(line):
            #     print('[DEBUG:FirstRun] found anonymous link definition in line:', line)

        return rst_link_definitions_keys

    def replace_heading_references(self, rst_file_content):
        print('[DEBUG]: searching for heading references ...')

        for lineno, line in enumerate(rst_file_content):
            # print(lineno, line)
            match_objects = self.rst_link_multi_word.finditer(line)

            for match_object in match_objects:
                print(match_object.group())
                link_key = match_object.group('link_key')

                if link_key in self.headings.keys():
                    # if there is such a heading then it is actually a link to a HEADING!!!
                    heading_link = link_key

                    print('[DEBUG]:', 'found a link to a heading!', heading_link)
                    # get the latex code for the reference to the heading (to
                    # the label at the heading)
                    latex_heading_label_reference = self.heading_link_to_latex_label_reference(heading_link)
                    # get the raw latex text role of rst with the filled in
                    # latex code
                    rst_raw_latex_link_reference = self.to_rst_raw_latex(latex_heading_label_reference)
                    # replace the match object in the line
                    print('[DEBUG]:', ' now replacing heading reference in line:\n|', line, '|', sep='')
                    rst_file_content[lineno] = line.replace(match_object.group(), rst_raw_latex_link_reference)
                    line = rst_file_content[lineno]
                    print('[DEBUG]:', ' line is now:\n|', rst_file_content[lineno], '|', sep='')

    def heading_link_to_latex_label_reference(self, heading_link):
        return '\hyperref[{key}]{{{text}}}' \
            .format(
                key = self.headings[heading_link],
                text = heading_link
            )


#     def replace_internal_single_word_targets(self, line, found_rst_link_definitions_keys):
#         match_object_list = self.internal_link_single_word_target.finditer(line)
#         for match_object in match_object_list:
#             link_key = match_object.group('link_key')
#             if link_key in found_rst_link_definitions_keys:
#                 print('[DEBUG:Replace] Ignoring key |', link_key, '| because it is a reST link definition key', sep='')
#                 continue
#             latex_link_target = self.link_key_to_latex_link_target(link_key)
#             rst_raw_latex_link_target = self.to_rst_raw_latex(latex_link_target, match_object)
#             line = line.replace(match_object.group(), rst_raw_latex_link_target)
#         return line
#
#     def replace_internal_single_word_references(self, line, found_rst_link_definitions_keys):
#         match_object_list = self.internal_link_single_word_reference.finditer(line)
#         for match_object in match_object_list:
#             link_key = match_object.group('link_key')
#             if link_key in found_rst_link_definitions_keys:
#                 print('[DEBUG:Replace] Ignoring key |', link_key, '| because it is a reST link definition key', sep='')
#                 continue
#             latex_link_target = self.link_key_to_latex_link_reference(link_key)
#             rst_raw_latex_link_target = self.to_rst_raw_latex(latex_link_target, match_object)
#             line = line.replace(match_object.group(), rst_raw_latex_link_target)
#         return line
#
#     def replace_internal_multi_word_targets(self, line, found_rst_link_definitions_keys):
#         match_object_list = self.internal_link_multi_word_target.finditer(line)
#         for match_object in match_object_list:
#             link_key = match_object.group('link_key')
#             if link_key in found_rst_link_definitions_keys:
#                 print('[DEBUG:Replace] Ignoring key |', link_key, '| because it is a reST link definition key', sep='')
#                 continue
#             latex_link_target = self.link_key_to_latex_link_target(link_key)
#             rst_raw_latex_link_target = self.to_rst_raw_latex(latex_link_target, match_object)
#             line = line.replace(match_object.group(), rst_raw_latex_link_target)
#         return line
#
#     def replace_internal_multi_word_references(self, line, found_rst_link_definitions_keys):
#         match_object_list = self.internal_link_multi_word_reference.finditer(line)
#         for match_object in match_object_list:
#             link_key = match_object.group('link_key')
#             if link_key in found_rst_link_definitions_keys:
#                 print('[DEBUG:Replace] Ignoring key |', link_key, '| because it is a reST link definition key', sep='')
#                 continue
#             latex_link_target = self.link_key_to_latex_link_reference(link_key)
#             rst_raw_latex_link_target = self.to_rst_raw_latex(latex_link_target, match_object)
#             line = line.replace(match_object.group(), rst_raw_latex_link_target)
#         return line
#
#     def link_key_to_latex_link_target(self, link_key):
#         return '\hypertarget{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_key)
#
#     def link_key_to_latex_link_reference(self, link_key):
#         return '\hyperlink{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_key)
#
    def to_rst_raw_latex(self, latex_content):
        return ':raw-latex:`' + latex_content + '`'
