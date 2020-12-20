from forms import LoginForm, RegisterForm, SearchForm
import requests

class Apis():
    def search_api(search_variable):
        searchUrl = 'https://api.itbook.store/1.0/search/'
        r = requests.get(searchUrl + search_variable) 
        result = r.json()
        return result
    
    def numeric_search(last_number):
        book_api_url = "https://api.itbook.store/1.0/books/"
        r = requests.get(book_api_url + last_number)
        return r
