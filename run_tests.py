import unittest

loader = unittest.TestLoader()
suite = unittest.TestSuite()

for path in ["src", "src/functions"]:
    suite.addTests(loader.discover(path))

unittest.TextTestRunner().run(suite)
