import re

class RSTInternalLinksParser():
    """parses rst files and exchanges internal links with latex internal hyperlinks"""

    def __init__(self, headings):
        super().__init__()

        self.headings = headings

        self.rst_reference_definition_regex = re.compile(r'\.\. _(?P<link_key>[^\[\]_`:]+):', re.UNICODE)
#         self.rst_reference_multi_word_regex = re.compile(
#             r'''
#             `                        # literal backtick
#
#             (?P<link_key>            # start of named group
#
#             [a-zA-Z0-9ßäöüÄÖÜ() -]+  # letter or
#                                      # number or
#                                      # umlaut or
#                                      # space or
#                                      # dash
#
#             )                        # end of named group
#
#             `                        # literal backtick
#
#             _                        # literal underscore
#             ''', re.VERBOSE|re.UNICODE)

        self.rst_target_single_word_regex = re.compile(
            r'''
            (?<!\.\.[ ])                           # exclude link definitions
            (?<!__[ ])                             # exclude anonymous link definitions
            (?<=[\s^])                             # there must be either the beginning of the line before OR whitespace
                                                   # (this excludes backticks for example)

            _                                      # underscore

            (?P<link_key>[a-zA-Z0-9ßäöüÄÖÜ()-]+)   # letters
                                                   # numbers
                                                   # parentheses
                                                   # underscores
                                                   # dashes
            ''',
            re.VERBOSE|re.UNICODE
        )

        self.rst_reference_single_word_regex = re.compile(
            r'''
            (?<!__[ ])                             # exclude anonymous link definitions
            (?<=[\s^])                             # there must be either the beginning of the line before OR whitespace
                                                   # (this excludes backticks for example)

            (?P<link_key>[a-zA-Z0-9ßäöüÄÖÜ()-]+)   # letters
                                                   # numbers
                                                   # parentheses
                                                   # underscores
                                                   # dashes

            _                                      # underscore

            (?=(\s|[.,:;/?!]|$))                   # not a word like: abc_def
            ''', re.VERBOSE|re.UNICODE)

        self.rst_target_multi_word_regex = re.compile(
            r'''
            (?<=[\s^])
            _

            `
            (?P<link_key>[a-zA-Z0-9ßäöüÄÖÜ()_ -]+)
            `
            ''',
            re.VERBOSE|re.UNICODE
        )

        self.rst_reference_multi_word_regex = re.compile(
            r'''
            (?<=[\s^])
            `
            (?P<link_key>[a-zA-Z0-9ßäöüÄÖÜ()_ -]+)
            `
            _
            (?=(\s|[\)\(.,:;/?!]|$))
            ''',
            re.VERBOSE|re.UNICODE
        )

    def parse(self, rst_file_content):
        found_rst_link_definitions_keys = self.find_reference_definitions(rst_file_content)
        print('[DEBUG:Result] found link definition keys:', found_rst_link_definitions_keys)

        rst_file_content = self.replace_heading_references(rst_file_content)

        rst_file_content = self.replace_single_word_targets(rst_file_content)
        rst_file_content = self.replace_single_word_references(rst_file_content)

        rst_file_content = self.replace_multi_word_targets(rst_file_content)
        rst_file_content = self.replace_multi_word_references(rst_file_content)

        return rst_file_content

    def find_reference_definitions(self, rst_file_content):
        rst_reference_definition_keys = []

        for lineno, line in enumerate(rst_file_content):
            if self.rst_reference_definition_regex.match(line):
                rst_reference_definition_keys.append(self.rst_reference_definition_regex.match(line).group('link_key'))

        return rst_reference_definition_keys

    def replace_heading_references(self, rst_file_content):
        print('[DEBUG]: searching for heading references ...')

        for lineno, line in enumerate(rst_file_content):
            match_objects = self.rst_reference_multi_word_regex.finditer(line)

            for match_object in match_objects:
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

        return rst_file_content

    def heading_link_to_latex_label_reference(self, heading_link):
        return '\hyperref[{key}]{{{text}}}' \
            .format(
                key = self.headings[heading_link],
                text = heading_link
            )

    def replace_single_word_targets(self, rst_file_content):
        print('[DEBUG]: searching for single word targets ...')
        for lineno, line in enumerate(rst_file_content):
            match_objects = self.rst_target_single_word_regex.finditer(line)
            for match_object in match_objects:
                link_key = match_object.group('link_key')
                print('[DEBUG]:', 'found a single word hypertarget!', link_key)
                latex_hypertarget = self.link_key_to_latex_hypertarget(link_key)
                rst_raw_latex_hypertarget = self.to_rst_raw_latex(latex_hypertarget)
                print('[DEBUG]:', ' now replacing hypertarget in line:\n|', line, '|', sep='')
                rst_file_content[lineno] = line.replace(match_object.group(), rst_raw_latex_hypertarget)
                line = rst_file_content[lineno]
                print('[DEBUG]:', ' line is now:\n|', rst_file_content[lineno], '|', sep='')

        return rst_file_content

    def replace_single_word_references(self, rst_file_content):
        print('[DEBUG]: searching for SINGLE word REFERENCES ...')
        for lineno, line in enumerate(rst_file_content):
            match_objects = self.rst_reference_single_word_regex.finditer(line)
            for match_object in match_objects:
                link_key = match_object.group('link_key')
                print('[DEBUG]: found a SINGLE word hyperlink! |', link_key, '|', sep='')
                latex_hyperlink = self.link_key_to_latex_hyperlink(link_key)
                rst_raw_latex_hyperlink = self.to_rst_raw_latex(latex_hyperlink)
                print('[DEBUG]:', ' now replacing hyperlink in line ', lineno, ':\n|', line, '|', sep='')
                rst_file_content[lineno] = line.replace(match_object.group(), rst_raw_latex_hyperlink)
                line = rst_file_content[lineno]
                print('[DEBUG]:', ' line is now:\n|', rst_file_content[lineno], '|', sep='')

        return rst_file_content

    def replace_multi_word_targets(self, rst_file_content):
        print('[DEBUG]: searching for MULTI word TARGETS ...')
        for lineno, line in enumerate(rst_file_content):
            match_objects = self.rst_target_multi_word_regex.finditer(line)
            for match_object in match_objects:
                link_key = match_object.group('link_key')
                print('[DEBUG]: found a MULTI word hyperTARGET! |', link_key, '|', sep='')
                latex_hypertarget = self.link_key_to_latex_hypertarget(link_key)
                rst_raw_latex_hypertarget = self.to_rst_raw_latex(latex_hypertarget)
                print('[DEBUG]:', ' now replacing hypertarget in line ', lineno, ':\n|', line, '|', sep='')
                rst_file_content[lineno] = line.replace(match_object.group(), rst_raw_latex_hypertarget)
                line = rst_file_content[lineno]
                print('[DEBUG]:', ' line is now:\n|', rst_file_content[lineno], '|', sep='')

        return rst_file_content

    def replace_multi_word_references(self, rst_file_content):
        print('[DEBUG]: searching for MULTI word REFERENCES ...')
        for lineno, line in enumerate(rst_file_content):
            match_objects = self.rst_reference_multi_word_regex.finditer(line)
            for match_object in match_objects:
                link_key = match_object.group('link_key')
                if link_key not in self.headings.keys():
                    print('[DEBUG]: found a MULTI word hyperREFERENCE! |', link_key, '|', sep='')
                    latex_hyperlink = self.link_key_to_latex_hyperlink(link_key)
                    rst_raw_latex_hyperlink = self.to_rst_raw_latex(latex_hyperlink)
                    print('[DEBUG]:', ' now replacing hyperlink in line ', lineno, ':\n|', line, '|', sep='')
                    rst_file_content[lineno] = line.replace(match_object.group(), rst_raw_latex_hyperlink)
                    line = rst_file_content[lineno]
                    print('[DEBUG]:', ' line is now:\n|', rst_file_content[lineno], '|', sep='')

        return rst_file_content


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
    def link_key_to_latex_hypertarget(self, link_key, link_text=None):
        if link_text:
            return '\hypertarget{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_text)
        else:
            return '\hypertarget{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_key)

    def link_key_to_latex_hyperlink(self, link_key, link_text=None):
        if link_text:
            return '\hyperlink{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_text)
        else:
            return '\hyperlink{{{link_key}}}{{{link_text}}}'.format(link_key=link_key, link_text=link_key)

    def to_rst_raw_latex(self, latex_content):
        return ':raw-latex:`' + latex_content + '`'
