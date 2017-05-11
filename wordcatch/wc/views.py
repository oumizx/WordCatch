from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
import happybase
import language_check
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import boto3

tool = language_check.LanguageTool('en-US')

session = boto3.Session(profile_name='dev')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.

dynamodb = session.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")

table = dynamodb.Table('FourThird')

def Index(request):
    return render(request, 'wc/index.html')

class Grammar_check_view(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'wc/grammar_check.html')

    def post(self, request, *args, **kwargs):
        sentences = request.POST['sentences']
        # sentences = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'
        matches = tool.check(sentences)
        suggestion = language_check.correct(sentences, matches)
        print(sentences)
        context = {
            "sentences": sentences,
            "matches": matches,
            "suggestion": suggestion
        }
        print(matches)
        return render(request, 'wc/grammar_check_result.html', context)

@csrf_exempt
def Speech_search(request):
    if request.method == "GET":
        return render(request, 'wc/speech_search.html')

    if request.method == "POST":
        json_req = request.POST.get('json', None)
        data = json.loads(json_req)
        # print(data['parameters']['any'])
        words1 = data['result']['parameters']['any']
        words2 = data['result']['parameters']['any']
        location = data['result']['parameters']['find']['location']
        print(words1)




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
            str_input = ''
            pos = 0
            i = 0
            for w in wordarr:
                if (w == '_'):
                    pos = i
                else:
                    str_input = str_input + w
                    if (i < wordlen - 1):
                        str_input = str_input + ' '
                i = i + 1
            str_input = str_input.strip()
            print(str_input + "end")
            if (wordlen == 2):
                if (pos == 0):
                    table = connection.table('one_first')
                elif (pos == 1):
                    table = connection.table('one_second')
            elif (wordlen == 3):
                if (pos == 0):
                    table = dynamodb.Table('ThreeFirst')
                elif (pos == 1):
                    table = dynamodb.Table('ThreeMiddle')
                elif (pos == 2):
                    table = dynamodb.Table('ThreeLast')
            elif (wordlen == 4):
                if (pos == 0):
                    table = dynamodb.Table('FourFirst')
                elif (pos == 1):
                    table = dynamodb.Table('FourSecond')
                elif (pos == 2):
                    table = dynamodb.Table('FourThird')
                elif (pos == 3):
                    table = dynamodb.Table('FourLast')
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
            row = table.get_item(Key={'Keyword': str_input})

            if (row == {}):
                template = "wc/error_wrong.html"
            else:
                length = len(row['Item']['content']) / 2
                template = "wc/search_result.html"
                for i in range(length):
                    #   length ? i  ?
                    word_tag = str(i + 1) + "word"
                    wordnum_tag = str(i + 1) + "num"
                    wordlist.append(row['Item']['content'][word_tag])
                    countlist.append(row['Item']['content'][wordnum_tag])
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

                totalAmount = 0
                for num in countlist:
                    totalAmout = totalAmout + num

                for i in range(length):
                    percentlist.append(countlist[i]/totalAmout)

                # percentlist.append(row[b'first:percent'].decode("utf-8"))
                # percentlist.append(row[b'second:percent'].decode("utf-8"))
                # percentlist.append(row[b'third:percent'].decode("utf-8"))
                # percentlist.append(row[b'fourth:percent'].decode("utf-8"))
                # percentlist.append(row[b'fifth:percent'].decode("utf-8"))

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
