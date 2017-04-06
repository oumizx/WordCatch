from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
import happybase


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "wc/index.html", {})

    def post(self, request, *args, **kwargs):
        connection = happybase.Connection('52.88.150.200')
        words = request.POST["words"]
        context = {}
        if(words == ""):
            template = "wc/error_empty.html"
        else:
            wordarr = words.split(' ')
            wordlen = len(wordarr)
            wordlist = []
            countlist = []
            percentlist = []
            str = ''
            pos = 0
            i = 0
            for w in wordarr:
                if (w == '_'):
                    pos = i
                else:
                    str = str + w
                    if (i < wordlen - 1):
                        str = str + ' '
                i = i + 1
            str = str.strip()
            print(str + "end")
            if (wordlen == 2):
                if (pos == 0):
                    table = connection.table('one_first')
                elif (pos == 1):
                    table = connection.table('one_second')
            elif (wordlen == 3):
                if (pos == 0):
                    table = connection.table('two_first')
                elif (pos == 1):
                    table = connection.table('two_second')
                elif (pos == 2):
                    table = connection.table('two_third')
            elif (wordlen == 4):
                if (pos == 0):
                    table = connection.table('three_first')
                elif (pos == 1):
                    table = connection.table('three_second')
                elif (pos == 2):
                    table = connection.table('three_third')
                elif (pos == 3):
                    table = connection.table('three_fourth')
            elif (wordlen == 5):
                if (pos == 0):
                    table = connection.table('four_first')
                elif (pos == 1):
                    table = connection.table('four_second')
                elif (pos == 2):
                    table = connection.table('four_third')
                elif (pos == 3):
                    table = connection.table('four_fourth')
                elif (pos == 4):
                    table = connection.table('four_fifth')
            row = table.row(str)
            if (row == {}):
                template = "wc/error_wrong.html"
            else:
                template = "wc/search_result.html"
                wordlist.append(row[b'first:word'].decode("utf-8"))
                wordlist.append(row[b'second:word'].decode("utf-8"))
                wordlist.append(row[b'third:word'].decode("utf-8"))
                wordlist.append(row[b'fourth:word'].decode("utf-8"))
                wordlist.append(row[b'fifth:word'].decode("utf-8"))
                print(wordlist)
                k = 0
                for wd in wordlist:
                    temp = ""
                    j = 0
                    for origin_part in wordarr:
                        if (pos == j):
                            temp = temp + wd
                        else:
                            temp = temp + origin_part
                        if (j < wordlen - 1):
                            temp = temp + ' '
                        j = j + 1
                    wordlist[k] = temp
                    k = k + 1

                print(wordlist)

                countlist.append(row[b'first:count'].decode("utf-8"))
                countlist.append(row[b'second:count'].decode("utf-8"))
                countlist.append(row[b'third:count'].decode("utf-8"))
                countlist.append(row[b'fourth:count'].decode("utf-8"))
                countlist.append(row[b'fifth:count'].decode("utf-8"))
                percentlist.append(row[b'first:percent'].decode("utf-8"))
                percentlist.append(row[b'second:percent'].decode("utf-8"))
                percentlist.append(row[b'third:percent'].decode("utf-8"))
                percentlist.append(row[b'fourth:percent'].decode("utf-8"))
                percentlist.append(row[b'fifth:percent'].decode("utf-8"))

            context = {
                "searchword": words,
                "word": wordlist,
                "count": countlist,
                "percent": percentlist,
            }
        #
        # if (words == "offer advice _"):
        #     template = "wc/search_last.html"
        # elif (words == "catch _ with"):
        #     template = "wc/search_middle.html"
        # elif (words == ""):
        #     template = "wc/error_empty.html"
        # else: template = "wc/error_wrong.html"
        return render(request, template, context)
