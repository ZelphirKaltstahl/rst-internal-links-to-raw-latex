import re

class RSTInternalLinksParser():
    """parses rst files and exchanges internal links with latex internal hyperlinks"""

    def __init__(self):
        super().__init__()

        self.rst_anonymous_link_definition = re.compile(r'^\.\. __: .+$|^__ .+$')
        self.rst_link_definition = re.compile(r'^\.\. _(?P<link_key>[^\[\]_`\s][^\[\]\s`]*):')
        self.internal_link_single_word_target = re.compile(
            r'''
            [\s^]+                    # at least one whitespace or beginning of
                                      # the line

            (?<!\.\. )                # not ".. " in front, because it would be
                                      # a link definition and not a target.

            (?<!``)                   # not double backtick in front because
                                      # this is verbatim text of rst

            _                         # the literal underscore

            (?P<link_key>[^\[\]\s`]+) # the link key:
                                      # no brackets [ ]
                                      # no whitespace
                                      # no backtick `
            ''', re.VERBOSE)
        self.internal_link_multi_word_target = re.compile(
            r'[\s^]+_`(?P<link_key>[^\[\]`]+)`')
        self.internal_link_single_word_reference = re.compile(
            r'[\s^]+(?P<link_key>[^\[\]\s`]+)_(?!_)')
        self.internal_link_multi_word_reference = re.compile(
            r'[\s^]+`(?P<link_key>[^\[\]`]+)`_(?!_)')

    def parse(self, rst_file_content, heading_labels):
        return rst_file_content


#     def add_raw_latex_rst_role(self, rst_file_content):
#         rst_file_content.insert(0, '')
#         rst_file_content.insert(0, '   :format: latex')
#         rst_file_content.insert(0, '.. role:: raw-latex(raw)')
#         return rst_file_content
#
#     def parse(self, rst_file_content):
#         found_rst_headings = self.headings_parse.parse_headings(rst_file_content)
#         print('[DEBUG:Result] found headings:', found_rst_headings)
#         found_rst_link_definitions_keys = self.find_link_definitions(rst_file_content)
#         print('[DEBUG:Result] found link definition keys:', found_rst_link_definitions_keys)
#
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
#
#
#
#     def find_link_definitions(self, rst_file_content):
#         rst_link_definitions_keys = []
#         for line in rst_file_content:
#             # there can only be one definition per line
#             if self.rst_link_definition.search(line) is not None:
#                 print('[DEBUG:FirstRun] found link definition in line:', line)
#                 rst_link_definitions_keys.append(
#                     self.rst_link_definition.match(line).group('link_key')
#                 )
#             elif self.rst_anonymous_link_definition.search(line) is not None:
#                 print('[DEBUG:FirstRun] found anonymous link definition in line:', line)
#                 return rst_link_definitions_keys
#
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
#     def to_rst_raw_latex(self, latex_content, match):
#         return match.group()[0] + ':raw-latex:`' + latex_content + '`'
