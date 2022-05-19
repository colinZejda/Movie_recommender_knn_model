from bs4 import BeautifulSoup
import requests
import urllib
import threading

def get_google_1st_link(search_term):
    url = 'https://www.google.com/search'
    headers = {
        'Accept' : '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67',
    }
    search_term = "imdb" + str(search_term)
    parameters = {'q': search_term}
    content = requests.get(url, headers = headers, params = parameters).text
    soup = BeautifulSoup(content, "lxml")
    search_term = soup.find(id = 'search')
    first_link = search_term.find('a')
    #print(first_link['href'])
    return first_link['href']

def get_google_page(search_term):
    lnk = "https://www.google.com/search?q="
    search_term = str(search_term)
    search_term = "+".join(search_term.split())
    lnk = lnk + search_term
    #print(lnk)
    return lnk

def get_image(url):
    # used this tutorial: https://pythonprogramminglanguage.com/get-all-links-from-webpage/ 
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, 'lxml')
    images = soup.findAll('img')
    img_link = images[0].get('src')
    #print(img_link)
    return img_link

def compute_three(movie_name, results, index):
    try:
        L1 = get_google_1st_link(movie_name)
        L2 = get_google_page(movie_name)
        L3 = get_image(get_google_1st_link(movie_name))
        results[index] = (L1, L2, L3)
    except:
        results[index] = (None, None, None)

def compute_array(all_movie_titles):
    threads = [None] * len(all_movie_titles)
    results = [None] * len(all_movie_titles)
    for i, movie in enumerate(all_movie_titles):       # go thru movies, get integers too
        t = threading.Thread(target=compute_three, args=(movie, results, i))   # each index avoids collisions (mixing up the order) when storing back
        t.start()
        threads[i] = t
    for t in threads:
        t.join()
    return results

if __name__ == "__main__":
    movie_name = "The Shawshank Redemption"
    print(compute_array(["Next Karate Kid, The", "Jury Duty", "Adventures of Elmo in Grouchland, The", "Kazaam", "Kiss of Death"]))
    #print(get_google_page(movie_name))
    #print(get_google_1st_link(movie_name))
    #print(get_image(get_google_1st_link(movie_name)))
