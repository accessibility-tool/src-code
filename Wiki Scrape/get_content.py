import wikipedia
import re

test = wikipedia.page("Mathematics")
title = test.title
links = test.links
test = test.content

test = re.sub(" == ", "[==]", test)
test = re.sub(" === ", "[===]", test)

#print(test)

test = re.sub("=====","-----", test)
test = re.sub("====","----", test)
test = re.sub("===","---", test)
test = re.sub("== ", " ==", test)

test = test.split(" ==")
n = len(test)
for i in range(0,n):
    test[i] = (test[i]).strip()

dic = {}
link = {}
dic[title] = test[0]
link[title] = []
for l in links:
        if l.lower() in test[0].lower():
            link[title].append(l)

for i in range(1,n,2):
    for l in links:
        if l.lower() in test[i+1].lower():

            if test[i] in link:
                link[test[i]].append(l)
            else:
                f = []
                f.append(l)
                link[test[i]] = (f)
    dic[test[i]] = test[i+1]
