#!/usr/bin/env python3

import logging
import os
from .helpers import clamp

class Completer:

    class Context:
        def __init__(self, index, last_text, completions):
            self.index = index
            self.last_text = last_text
            self.completions = completions

    def __init__(self, commands, edit_widget):
        self.commands = sorted(commands)
        self.edit_widget = edit_widget
        self.logger = logging.getLogger('Completer')

    def _handle_no_context(self, last_word, words_count, edit_text):
        if words_count > 1:
            matched_commands = [c for c in sorted(os.listdir('.')) if c.startswith(last_word)]
        else:
            matched_commands = [c for c in self.commands if c.startswith(last_word)]
        self.logger.debug('For {} found {}'.format(last_word, matched_commands))
        if len(matched_commands) == 0: return None
        self.edit_widget.insert_text(matched_commands[0][len(last_word):])
        return self.Context(0, last_word, matched_commands)

    def _handle_context(self, context, last_word, words_count, edit_text):
        if context.last_text != last_word and not last_word in context.completions or words_count == 0:
            self.logger.debug('Context invalidated')
            return self._handle_no_context(last_word, words_count, edit_text)
        context.index = 0 if (context.index == len(context.completions) - 1) else context.index + 1
        new_edit_text = self._replace_last_word(edit_text, context.completions[context.index])
        self.edit_widget.set_edit_text(new_edit_text)
        self.edit_widget.set_edit_pos(len(new_edit_text))
        return context

    def _replace_last_word(self, string, word):
        words = string.split()
        words[-1] = word
        return ' '.join(words)

    def _get_last_word_and_words_count(self, string):
        words = string.split()
        if len(string):
            return ('', len(words) + 1) if string[-1] == ' ' else (words[-1], len(words))
        else:
            return ('', 0)

    def complete(self, context):
        edit_text = self.edit_widget.get_edit_text()
        last_word, words_count = self._get_last_word_and_words_count(edit_text)
        return self._handle_context(context, last_word, words_count, edit_text) \
                if context else self._handle_no_context(last_word, words_count, edit_text)

