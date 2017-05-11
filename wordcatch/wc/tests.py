from django.test import TestCase
import language_check
# Create your tests here.
tool = language_check.LanguageTool('en-US')
text = u'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
matches = tool.check(text)
for match in matches:
    print(match)