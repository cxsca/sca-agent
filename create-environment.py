#!/usr/bin/env python

import string
import random
import sys
import re


def get_random_hex_string():
    return ''.join(random.choice(string.hexdigits) for i in range(12))


placeHolder = "{GenKey()}"
txtInput = sys.stdin
txtOutput = sys.stdout
txtInput = open(".env.defaults")
txtOutput = open(".env", 'w')

for envLine in txtInput.readlines():
    for match_position in [match.start() for match in re.finditer(re.escape(placeHolder), envLine)]:
        envLine = envLine.replace(placeHolder, get_random_hex_string(), 1)
    txtOutput.write(envLine)

txtOutput.close()
txtInput.close()
