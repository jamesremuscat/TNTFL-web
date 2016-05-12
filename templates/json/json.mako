<%!
import re
def stripNewlines(text):
  return text.replace("\r", "").replace("\n", "")

def collapseWhitespace(text):
  rex = re.compile(r' +')
  return rex.sub(' ', text)
%><%namespace name="blocks" file="../blocks.mako" inheritable="True"/>
${capture(self.body) | stripNewlines, collapseWhitespace}
