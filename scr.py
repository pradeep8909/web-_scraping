import requests,pprint
from bs4 import BeautifulSoup
import os
import time,random
import json
IMBD_URL = "https://www.imdb.com/india/top-rated-indian-movies/"

def scrape_top_list(URL):
	if os.path.exists("movies.json"):
		pass
	else:	
		sample = requests.get(URL)
		soup = BeautifulSoup(sample.text,"html.parser")

		movie=soup.find("tbody",class_="lister-list")
		f=movie.find_all("tr")

		top_mov = []
		dic = {}
		for tr in f:
			a=tr.find("td",class_="titleColumn")
			b=a.find('a').get_text()
			rate=tr.find("td",class_="ratingColumn imdbRating")
			rate_find=rate.find("strong")
			strong=rate_find.get_text()
			half_url=a.find('a')['href']
			half_url = half_url[:17]
			b=a.get_text().strip().split("\n")
			dic["position"]=b[0].strip(".")
			dic["name"]=b[1].strip()
			dic["year"]=int(b[2][1:5])
			dic["rating"]=float(strong)
			dic['url']="https://www.imdb.com" + half_url
			dic_copy = dic.copy()
			top_mov.append(dic_copy)
		# p top_mov
		with open ('movies.json',"w") as data:
			json.dump(top_mov,data)
	with open ('movies.json',"r") as data:
		read = data.read()
		top_mov = json.loads(read)
	return top_mov
final=(scrape_top_list(IMBD_URL))
# pprint.pprint(final)


def group_by_year(top_mov_list):
	year_dic = {}
	for movie in top_mov_list:
		year = movie['year']
		year_dic[year] = []
	for movie in top_mov_list:
		year = movie['year']
		year_dic[year] += [movie]
	return year_dic
 # pprint.pprint(group_by_year(final))
k=(group_by_year(final))
# print(k)

#decade fuction
def group_by_dec(movies):
	decade_list=[]
	move_dec={}
	for i in movies:
		index= i %10 
		decade= i-index
		if decade not in decade_list:
			decade_list.append(decade)
	list1=(decade_list)	
	list1.sort()
	for x in list1:
		move_dec[x]=[]
	for i in move_dec:
		range_= i +9
		for y in movies:
			if y<=range_ and  y>=i:
				for z in movies[y]:
					move_dec[i].append(z)
	return(move_dec)
final1=(group_by_dec(k))
# print(final1)		
###details of the movies
##task12
def scrape_movie_cast( movie_caste_url):
	half_cast_url=movie_caste_url+"fullcredits?ref_=tt_cl_sm#cast"
	castee = requests.get(half_cast_url)
	soup = BeautifulSoup(castee.text,"html.parser")
	a_name=soup.find("table",class_="cast_list")
	tds=a_name.find_all("td",class_="")
	cast_dic={}
	cast_list=[]
	for x in range(len(tds)):
		actors=tds[x].find('a').get('href')[6:15]
		cast_dic["imbd_id"]=actors
		actor_name=tds[x].get_text().strip()
		cast_dic["name"]=actor_name
		cast_list.append(cast_dic.copy())
	return cast_list
# cast_data=scrape_movie_cast(final)
# print(cast_data)



ananad_url= final[0]["url"]
def scrape_movie_details(movie_url):
	time_sleep=random.randint(1,3)
	file_url=movie_url[27:36]+".json"
	if os.path.exists("/home/pradeep/Desktop/DataBasa/movie_data/"+file_url):
		with open ("movie_data/"+file_url,"r") as data:
			read = data.read()
			details_dic = json.loads(read)
	else:		
		details_dic={}
		genre1=[]
		
		movie_details = requests.get(movie_url)
		soup = BeautifulSoup(movie_details.text,"html.parser")
		details=soup.find("div" ,class_="title_wrapper")
		director=soup.find("div",class_="credit_summary_item").get_text().strip().split('\n')
		director_name_title=(director[1:])
		country=soup.find("div",class_="article",id="titleDetails")
		country_name = country.find("div", class_="txt-block").get_text().split()
		langauge = country.find_all("div",class_="txt-block")
		
		poster= soup.find("div",class_="poster")
		poster_link=poster.find("img")
		url = poster_link.get("src")
		time=soup.find("div",class_="subtext")
		tot_time=time.find("time").get_text().strip().split()
		# print(tot_time)
		l=len(tot_time)
		if l==1:
			total=int(tot_time[0][0])*60
		else:
			minitue=int(tot_time[0][0])*60
			seconds=(tot_time[1])[:-3]
			seconds_final=int(seconds)
			total=minitue+seconds_final
		# print(total)
			
		bio=soup.find("div",class_="summary_text").get_text().strip()
		# print(bio)
		Genre= soup.find_all('div',class_='see-more inline canwrap')
		for x in Genre:
			a= x.get_text().strip().split()
			if a[0]=="Genres:":
				b=a[1:]
		for i in langauge:
			a = i.get_text().split()
			if a[0] == "Language:":
				langauge_title=(a[1:])	
		movie_name=details.find('h1').get_text().split()
		movie_name.pop()
		movie_name=(' ').join(movie_name)		
		details_dic["name"]=movie_name
		details_dic["country"] = country_name[1]
		details_dic["Director"]=director_name_title
		details_dic["Language"]=langauge_title
		details_dic["Genre"]=b
		details_dic["Poster_Link"]=url
		details_dic["Bio"]=bio
		details_dic["Runtime"]=total
		details_dic['cast']=scrape_movie_cast(movie_url)

		# a = details_dic	
		with open ("movie_data/"+file_url, "w") as data:
			json.dump(details_dic.copy(),data)
	return(details_dic)
# details_fun=scrape_movie_details(ananad_url)
# print(details_fun)


#details of 250 movies
def get_movie_list_details(movie_list):
	details_all=[]	
	for i in range (len(movie_list)):
		uurl= final[i]["url"]
		ffinal=scrape_movie_details(uurl)
		# pprint.pprint(ffinal)
		details_all.append(ffinal)
	return details_all
	# print(details_all)


all_details=(get_movie_list_details(final))
# print(all_details)


##seprated by the language(task6)
def Analyse_movie_language(movie_list):
	dic_lang={}
	for movie in movie_list:
		for lang in movie['Language']:
			dic_lang[lang]= 0
	for movie in movie_list:
		for lang in movie['Language']:
			dic_lang[lang]+= 1
	return dic_lang
by_lang=Analyse_movie_language(all_details)
# print(by_lang)


####seprated by director(task7)
def Analyse_movie_director(movie_list):
	director_dic={}
	for dictr in movie_list:
		for direct in dictr['Director']:
			director_dic[direct]= 0
			# print (direct)
	for dictr in movie_list:
		for direct in dictr['Director']:
			director_dic[direct]+= 1
	return director_dic
by_dirct=Analyse_movie_director(all_details)
# print(by_dirct)

######task 10(seprrated by director and language)
	
def analyse_language_and_directors(movies_list):
	directors_dict = Analyse_movie_director(movies_list)
	directors_lang = {director:{} for director in directors_dict}
	for i in range(len(movies_list)):
		for director in directors_lang:
			if director in movies_list[i]['Director']:
				for language in movies_list[i]['Language']:
					directors_lang[director][language] = 0
	for i in range(len(movies_list)):
		for director in directors_lang:
			if director in movies_list[i]['Director']:
				for language in movies_list[i]['Language']:
					directors_lang[director][language] += 1
	return directors_lang

# pprint.pprint(analyse_language_and_directors(all_details))

##task11 seprated by genera
def analyse_movies_genre(movies_list):		
	dic_genera={}
	for genera in movies_list:
		for gen in genera['Genre']:
			dic_genera[gen]= 0
	for genera in movies_list:
		for gen in genera['Genre']:
			dic_genera[gen]+=1
	return dic_genera
by_genra=(analyse_movies_genre(all_details))
# print(by_genra)


####task15
def analyse_actors( movies_list):
	actors_dic={}
	id_list=[]
	for movie in movies_list:
		for i in movie["cast"]:
			actors_dic[i["imbd_id"]]={'name':i["name"],"num_movies":0}
			id_list.append(i["imbd_id"])
			set_list=list(set(id_list))
	for movie in movies_list:
		for actor in movie["cast"]:
			actors_dic[actor['imbd_id']]['num_movies'] += 1
	# for movie in movies_list:
	# 	# print(movie['cast'])
	# 	for z in movie['cast']:
	# 		# print(z)	
	# 		for x in set_list:
	# 			actors_dic[z['imbd_id']]['num_movies'] = 0
	# 			for j in id_list:
	# 				if x==j:
	# 					actors_dic[z['imbd_id']]['num_movies']+=1		
	pprint.pprint(actors_dic)
analyse_actors(all_details)	