import imdb

def get_top_10_imdb():
    lst = []
    ia = imdb.IMDb()
    search = ia.get_top250_movies()
    for i in range(15):
        lst.append(search[i])
    return lst

if __name__ == '__main__':
    for i in get_top_10_imdb():
        print(i)
