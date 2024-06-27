import os
import random
import re

from universal_profanity._patterns import _PATTERNS

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

_COUNTRY_CODES = (
    'th', 'fr', 'uk', 'gr', 'ge', 'cz',
    'sp', 'bu', 'tc', 'da', 'po', 'en', 'br', 'du',
    'la', 'fi', 'no', 'in', 'ja', 'tu', 'ru', 'ro',
    'sc', 'it', 'ko', 'sw', 'vi', 'hu'
)

_DEFAULT_REPLACE_CHARS = '@#!*$^%'


class UniversalProfanity:
    def __init__(self, country: str = 'en', replace_chars: str = _DEFAULT_REPLACE_CHARS):
        if country not in _COUNTRY_CODES:
            raise ValueError(f"Invalid country code. Allowed codes are: {_COUNTRY_CODES}")

        self._censor_chars = replace_chars
        self._censor_pool = []
        self._country = country
        self._profanity_pattern = self._pattern_generator()

    @staticmethod
    def get_data(path):
        return os.path.join(_ROOT, '', path)

    def get_censor_char(self):
        """Plucks a letter out of the censor_pool. If the censor_pool is empty,
        replenishes it. This is done to ensure all censor chars are used before
        grabbing more (avoids ugly duplicates).
        """
        if not self._censor_pool:
            # Censor pool is empty. Fill it back up.
            self._censor_pool = list(self._censor_chars)
        return self._censor_pool.pop(random.randrange(len(self._censor_pool)))

    def set_censor_characters(self, censor_chars):
        """Sets the pool of censor characters. Input should be a single string
        containing all the censor characters you'd like to use.
        Example: "@#$%^"
        """
        self._censor_chars = censor_chars

    def _pattern_generator(self):
        """ Takes the pattern which will be used for finding and replacing
        bad words in a text.
        """
        pattern = _PATTERNS[self._country]
        return re.compile(pattern, re.IGNORECASE)

    def contains_profanity(self, input_text):
        """Checks the input_text for any profanity and returns True if it does.
        Otherwise, returns False.
        """
        return input_text != self.censor(input_text)

    def censor(self, input_text):
        """Returns the input string with profanity replaced with a random string
        of characters plucked from the censor_characters pool.
        """
        clean_text = input_text

        for curse_word in re.finditer(self._profanity_pattern, input_text):
            censor_text = [self.get_censor_char() for _ in curse_word.group()]
            clean_text = clean_text.replace(curse_word.group(), ''.join(censor_text))

        return clean_text
