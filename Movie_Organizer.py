from os import listdir
from os.path import isfile, join
from imdbpie import Imdb

imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests
# Creating an instance with caching enabled
# Note that the cached responses expire every 2 hours or so.
# The API response itself dictates the expiry time)
imdb = Imdb(cache=True)

def main():
    #Capture all the files available in the below path
    #Make sure the path only contain movie files
    #Replace the path with your own movie path
    path=r"G:\Movies"
    CapturedMovies=dirCapture(path)
    MovieList=[]
    MovieDict={'Movie':'','Year':''}
    for i in CapturedMovies:
        MovieDict={'Movie':i,'Year':''}
        MovieList.append(MovieDict)
    print(MovieList)
    MovieList=Name_Sanitizer(MovieList)
    #change the path to weherver you want to have the movie digest  file 
    MoviesDigested = open(r"E:/Misc/01. Tech/01. Programing/Movie Organizer/MovieDigested.csv", 'w')
    MoviesDigested.write('Local Name,Sanitized Name, imdp Name, Year, Rating, Plot')
    x=-1
 
    for m in MovieList:
        MovieObj= Specific_year(m)
        print (MovieObj)
        x=x+1
        if MovieObj:
            title =imdb.get_title_by_id(MovieObj['imdb_id'])
            print ('############### {0}'.format(title))
            # The next two line are made to replace any comma in the plot_outline to avoid messing up the csv format
            Plot= str(title.plot_outline)
            Plot=Plot.replace(',', ';')
            Outputline= '{0}{1}{2}, {3}, {4}, {5},{6},{7}'.format('=hyperlink("',join(path,CapturedMovies[x]),'")',m['Movie'] ,title.title,title.year, title.rating, Plot)
            Outputline = Outputline.replace('\n',' ')
            print (Outputline)
            MoviesDigested.write('\n')
            MoviesDigested.write(Outputline)
        else:
            MoviesDigested.write('\n')
            Outputline='{0}{1}{3}{4}, Movie Metadata not found'.format('=hyperlink("',join(path,CapturedMovies[x]),'")',m['Movie'])
            Outputline = Outputline.replace('\n','')
            MoviesDigested.write(Outputline)

    MoviesDigested.close

#Name_Sanitizer to take out the grabage from the name
#Snaitizer Function-Tested= OK 05-05-2016
def Name_Sanitizer(MovieList):
    print ("Sanitizer Function")
    #update the path to where the junk list is placed on your PC
    Junk_File = open(r"E:\Misc\01. Tech\01. Programing\Movie Organizer\Junk List.txt",'r')
    Junk_List=[]
    while 1:
        Junk_Word=Junk_File.readline()
        Junk_Word=Junk_Word.lower().replace("\n", "")
        if Junk_Word=="":
            break
        Junk_List.append(Junk_Word)
    Junk_File.close
    #Extract the Movie release year ,if available, which is usually between [] or () in the file name
    for m in MovieList:
        if m['Movie'].find('[') is not -1: m['Year']=m['Movie'][m['Movie'].find('[')+1:m['Movie'].rfind(']')]
        if m['Movie'].find('(') is not -1 :m['Year']=m['Movie'][m['Movie'].find('(')+1:m['Movie'].rfind(')')]
        
        for j in Junk_List:
            m['Movie']=m['Movie'].lower().replace(j," ")         
    return MovieList

# A function to caputre all files in directory
def dirCapture(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path,f)) ]
    return onlyfiles

def Specific_year(Movie):
    #Remove all Year numbers >1900 from the name string because it misleads the search engine on imdb 
    s=[int(s) for s in Movie['Movie'].split() if s.isdigit() and  int(s)>1900]      
    for item in s:
        Movie['Movie']=Movie['Movie'].replace(str(item),'')
    # The next line will return a list of dictionaries
    movies =imdb.search_for_title(Movie['Movie'])
    if Movie['Year'] is '' and movies: return movies[0]
    for m in movies:
        if m['year']==Movie['Year']:
            return m 

if __name__ == "__main__":
    main()
