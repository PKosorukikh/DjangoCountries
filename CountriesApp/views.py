from django.shortcuts import render, HttpResponse, Http404
from django.core.paginator import Paginator
from pathlib import Path
from string import ascii_uppercase
from CountriesApp.models import Country, Language, countries_languages


def home_page(request):
    p = Path('.')
    return render(request, "index.html", {'path': p})


def countries_page(request):
    context = {'countries': load_countries_list(), 'letters': list(ascii_uppercase)}
    return render(request, "countries.html", context)


def listing(request, type):
    data_for_paginator = load_all_data() if type == 'countries' else load_languages_list()
    page = 'countries_paginated.html' if type == 'countries' else 'languages_paginated.html'

    page_obj = paginate_by(data_for_paginator, request.GET.get('page'), 15)

    context = {'page_obj': page_obj, 'letters': list(ascii_uppercase)}

    return render(request, page, context)


def paginate_by(data, page_number, split_by):
    paginator = Paginator(data, split_by)
    return paginator.get_page(page_number)


def load_all_data():
    from json import load
    file_countries = open(r'CountriesApp/json/countries.json', 'r')
    countries = []
    for ind, country in enumerate(load(file_countries)):
        country['id'] = ind + 1
        countries.append(country)
    return countries


def filtred_page(request, type, letter):
    dict_flters = {'countries': "country", 'languages': 'language'}
    if type in dict_flters.keys():
        if letter in ascii_uppercase:
            filtred_dict = {'letter': letter}
            temp_list = []
            if dict_flters[type] == "country":
                for country_data in load_all_data():
                    if country_data[dict_flters[type]][0] == letter:
                        temp_list.append(country_data[dict_flters[type]])
                filtred_dict['text'] = 'Countries'
            else:
                for lang in load_languages_list():
                    if lang[0] == letter:
                        temp_list.append(lang)
                filtred_dict['text'] = 'Languages'

            filtred_dict['page_obj'] = paginate_by(temp_list, request.GET.get('page'), 10)
            filtred_dict['link'] = type
            filtred_dict['page_name'] = f'{dict_flters[type]}-page'
            return render(request, "filtred_page.html", filtred_dict)
        else:
            raise Http404(f"Letter={letter} isn't in eng alphabet")


def load_countries_list():
    country_list = []
    for country_data in load_all_data():
        country_list.append(country_data['country'])
    return list(set(country_list))


def load_languages_list():
    lang_list = []
    for country_data in load_all_data():
        for lang in country_data['languages']:
            lang_list.append(lang)
    new_l = list(set(lang_list))
    new_l.sort()
    return new_l


def load_data_by_lang():
    data_by_lang = {lang: [] for lang in load_languages_list()}
    for country_data in load_all_data():
        cross_langs = set(data_by_lang.keys()) & set(country_data['languages'])
        for lang in cross_langs:
            data_by_lang[lang].append(country_data['country'])
    return data_by_lang


def language_page(request, letter):
    for language, country_list in load_data_by_lang().items():
        if language == letter:
            context = {'language': language, 'page_obj': paginate_by(country_list, request.GET.get('page'), 10)}
            return render(request, "language_page.html", context)
    raise Http404(f"Language {letter} doesn't exist")


def country_page(request, letter):
    for country_data in load_all_data():
        if country_data["country"] == letter:
            context = {'country': letter,
                       'page_obj': paginate_by(country_data["languages"], request.GET.get('page'), 10)}
            return render(request, "country_page.html", context)
    raise Http404(f"Country with name={letter} didn't found")


# def add_data_to_db(data, tab):
#     tab_name = 'CountryApp_' + tab
#     if tab_name == 'CountryApp_country':
#         for c in data:
#             Country(name=c)
#             Country.save()
#     elif tab_name == 'CountryApp_language':
#         for c in data:
#             Language(name=c)
#             Language.save()
#     elif tab_name == 'CountryApp_country_language':
#         for country_data in data:
#             for lang in country_data['languages']:
#                 countries_languages(country_name=country_data['country'], language_name=lang)
#                 countries_languages.save()



# print(load_all_data())

# def detect_filter(page_path):
#     list_of_links = page_path.split('/')
#     return list_of_links[-2]
#
# def items_page(request, page_type, letter):
#     if page_type == 'language':
#         for language, country_list in load_data_by_lang().items():
#             if language == letter:
#                 context = {'language': language, 'countries': country_list}
#                 return render(request, "language_page.html", context)
#         raise Http404(f"Language {letter} doesn't exist")
#     else:
#         for country_data in load_countries_list():
#             if country_data["country"] == letter:
#                 return render(request, "country_page.html", country_data)
#         raise Http404(f"Country with name={letter} didn't found")
#
