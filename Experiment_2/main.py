from lexical_analyzer import core

test = core.lexical_analyzer('((AC+BD)+1.27)')
for _ in range(10):
    print(test.getToken())
