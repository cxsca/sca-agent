#!/usr/bin/env python

import string
import random
import re


def getRandomHexString():
    return ''.join(random.choice(string.hexdigits) for i in range(12))


placeHolder = "%AUTO_GENERATED_PASSWORD%"
txtInput = open(".env.defaults")
txtOutput = open(".env", 'w')

for envLine in txtInput.readlines():
    for match_position in [match.start() for match in re.finditer(re.escape(placeHolder), envLine)]:
        envLine = envLine.replace(placeHolder, getRandomHexString(), 1)
    txtOutput.write(envLine)

txtOutput.close()
txtInput.close()
