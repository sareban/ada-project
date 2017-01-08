# ada-project
Repository for our ADA class project.

Cyril Pecoraro, Charlotte Burki, Mathieu Clavel

# Musical landscape of Switzerland

## Abstract
For our project, we want to look into the cultural aspects of Swizerland, more specifically its musical life. We will gather informations from the web about concerts happening throughout the country and the artists related, and try to get useful insights out of it, which has been little done here so far according to our sources.

## Data description 
To this purpose, we will look into mainsteams platforms of today and before, such as [lastfm](http://www.last.fm), which also has an [API](http://www.last.fm/api) or [bandsintown](http://news.bandsintown.com/home) which also has an [API](https://www.bandsintown.com/api/overview), as well as Swiss ticketsale platforms and online cultural agendas such as [PetziTicket](https://www.petzitickets.ch/index.php?research_date=02%2F02%2F2014&surch_go=), (where data can get accessed by specifying a date).

The idea is to get the events happening in Switzerland, their dates and artists.

## Feasibility and Risks, 
Data wrangling will most probably be one of the main challenge of this project, given we won't be able to work solely through a well furnished API such as Twitter's or Amazon's, although would we be optimistic, we will be able to get and process the data early enough to raise and answer interesting questions about it.
It will be possible to link the artists found with their [wikipedia page](https://www.wikipedia.org) and obtain information about their genre, country of origin.
It will also be possible to link the artists to their position in the billboard.

Finally, it is aslo possible to compare the situation in Switzerland and the situation in other countries of Europe.

**UPDATE 01/2017 : Main problem**
- Most of the API don't allow to search event by localization, they need to have the artist name.
- Hard to find data for the previous years.

## Deliverables
The dataset that will be built and which doens't exist yet according to our researches, will be one of the delivrable.
Another delivrable will be an interractive map.

## Timeplan
The first part of the project will be spent in defining clearer objective. Then we will spend a substancial ammount of time dor data wrangling, scrapping and cleaning. The questions we can raise with the data we obtain will be clearer once we get data.

## Interesting links
- [Mapping the hometowns of billboard hot 100 artists](http://thedataface.com/mapping-the-hometowns-of-billboard-hot-100-artsts/)
- [Le bilan des festivals de l'année 2016](http://www.touslesfestivals.com/actualites/le-bilan-des-festivals-de-lannee-2016-121216)
- [Stats soci-demographiques musique suisse](https://www.bfs.admin.ch/bfs/fr/home/statistiques/culture-medias-societe-information-sport.assetdetail.282381.html)
- [Carte des festivals suisses](https://www.festigo.ch/#!/fr/festimap/all)
- [Evolution of genres in the montreux jazz festival](http://kirellbenzi.com/blog/evolution-of-genres-in-the-montreux-jazz-festival/)
- [Data analysis Montreux Jazz Festival](http://kirellbenzi.com/blog/hello-montreux-jazz-festival/)
- [Artist Map of Montreux Jazz Festival](http://kirellbenzi.com/blog/montreux-jazz-festival-artists-map/)
- [Music API in 2016 - all the API related to music](https://www.acrcloud.com/blog/music-apis-the-list-of-2016)
