from django.shortcuts import render
import json
from django.http import HttpResponse
import nltk
from nltk.stem.isri import ISRIStemmer
import re
from django.http import JsonResponse
from .models import DailyWords
import json
from django.shortcuts import render

inverted_dict = {}

def index(request):
    return render(request, 'index.html')



def get_daily_words(day):
    global inverted_dict
    try:
        word_index_instance = DailyWords.objects.get(day=day)
        data_dict = json.loads(word_index_instance.words)
        inverted_dict = {v: k for k, v in data_dict.items()}
        return inverted_dict
    except DailyWords.DoesNotExist:
        return {}

def update_daily_words(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        day = request.POST.get('day')
        updated_data = get_daily_words(day)
        return JsonResponse({'success': True, 'data': updated_data})
    return JsonResponse({'success': False})



def day_select(request):
    days = DailyWords.objects.values_list('day', flat=True).distinct()
    last_day = days.last() if days else None
    context = {
        'days': days,
        'last_day': last_day,
    }

    return render(request, 'index.html', context)

def store_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Create a new record in the database with the content of the text file
    text_storage = DailyWords(words=text_content, day=3)
    text_storage.save()
    return text_storage
'''
file_path = "C:\\Users\\iisha\Downloads\\wordsShip.txt"
stored_text = store_text_file(file_path)'''


def search_word_index(request):
    word_to_search = request.GET.get('word', '').strip()

    if word_to_search:
        word_to_search = replace_last_ha(word_to_search)
        # Assuming you have only one instance of WordIndex or you know which one to use
        #word_index_instance = DailyWords.objects.first()
        # Convert the JSON string back to a dictionary
        #data_dict = json.loads(word_index_instance.words)
        # Invert the dictionary for fast lookup
        #inverted_dict = {v: k for k, v in data_dict.items()}
        index = inverted_dict.get(word_to_search, None)
        if index is not None:
            return JsonResponse({'word': word_to_search, 'index': index})
        else:
            # If the word is not found, stem it and search again
            st = ISRIStemmer()
            stemmed_word = st.stem(word_to_search)
            index = inverted_dict.get(stemmed_word, "Word not found")
            return JsonResponse({'word': stemmed_word, 'index': index})
    return JsonResponse({'error': 'Invalid request'}, status=400)

    #return render(request, 'index.html', {'result': result})


def replace_last_ha(word):
    # Regular expression to match a word ending with 'ه'
    regex = r'ه$'
    # Replace 'ه' at the end of the word with 'ة'
    return re.sub(regex, 'ة', word)