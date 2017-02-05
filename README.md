# ada-project
Repository for our ADA class project.
The Data of Music - An attempt at quantitizing the musical landscape of Switzerland

Cyril Pecoraro (MTE), Charlotte Burki (SIE), Mathieu Clavel (IC)

# Musical landscape of Switzerland

## Abstract
For our project, we want to look into the cultural aspects of Swizerland, more specifically its musical life. We will gather informations from the web about concerts that happened or will happen throughout the country and the artists related, and try to get useful insights out of it, which has been little done here so far according to our own researches.

We answered most key aspects in our poster (located at the root of this repo), as well as during our presentation. Nonetheless, for any question, feel free to ask any of us. But as we know there will be little time to review all projects, we try to keep it simple here (everyone wants her or his well deserved holidays, right ?)

### Feasibility and Risks, 
Data wrangling will most probably be one of the main challenge of this project, given we won't be able to work solely through a well furnished API such as Twitter's or Amazon's, although would we be optimistic, we will be able to get and process the data early enough to raise and answer interesting questions about it.
It will be possible to link the artists found with their [wikipedia page](https://www.wikipedia.org) and obtain information about their genre, country of origin.
It will also be possible to link the artists to their position in the billboard.

Finally, it is aslo possible to compare the situation in Switzerland and the situation in other countries of Europe.

**UPDATE 01/2017 : Main problem**
- Most of the API don't allow to search event by localization, they need to have the artist name.
- Hard to find data for the previous years.

### Deliverables
The dataset that will be built and which doens't exist yet according to our researches, will be one of the delivrable.
Another delivrable will be an interactive maps to explore the set.

### Timeplan
The first part of the project will be spent in defining clearer objective. Then we will spend a substancial ammount of time dor data wrangling, scrapping and cleaning. The questions we can raise with the data we obtain will be clearer once we get data.


## Data description 
We fetched event data from BandsInTown, ResidentAdvisor, Events.ch and La Route des Festivals, some which had API ready to use to query the data, other that we had to scrap manuallly using BeautifulSoup. In the end, we were left with 62'000 artists playing in 204'000 events, out in 22'000 venues. These numbers are already preprocessed, but we realised that they are not perfect, and some more cleaning would be useful, especially with Venues names where tricky duplicates were left.

Furthermore, we queried several music intelligence services like MusicGraph or Spotify, or broader platforms such as Wikipedia, to augment our data (most frequently only a name, a date and a place). We were mostly looking for music genre and origins of artists. Using Google Places, we geocoded all of our venues, to be able to present the data on interactive maps.

## Code description
With the Scrapper notebooks, we scrapped data from all the plateforms we used (BandsInTown, Discogs - abandoned, Events.ch, MusicGraph, ResidentAdvisor, RouteDesFestivals, Spotifiy, Wikipedia). Sometimes, they call on python scripts located in ./Scripts/, where they may also store partial results before we concatenate everything down to single csvs, either in ./Artists/, ./Events/, or ./Venues/.  In the Preprocessing notebooks is our preprocessing pipeline for cleaning and augmenting the data. Then in the Stats notebook, we produce a few graphs for our understanding of the dataset, and the poster too, while in Visualization we produce the interactive maps, and in Visualization2 we create some more viz.

## Results
In ./FinalResults/ are our complete dataset in total eventsFinal.csv, a wordcloud embedded in a Swiss map, and both interactive maps that we created (heatmap displaying heat across the map of Switzerland following events and genre density, while detailedmap precisly show the number of events happening per level of geographical zoom).

## Interesting links
- [Mapping the hometowns of billboard hot 100 artists](http://thedataface.com/mapping-the-hometowns-of-billboard-hot-100-artsts/)
- [Le bilan des festivals de l'année 2016](http://www.touslesfestivals.com/actualites/le-bilan-des-festivals-de-lannee-2016-121216)
- [Stats soci-demographiques musique suisse](https://www.bfs.admin.ch/bfs/fr/home/statistiques/culture-medias-societe-information-sport.assetdetail.282381.html)
- [Carte des festivals suisses](https://www.festigo.ch/#!/fr/festimap/all)
- [Evolution of genres in the montreux jazz festival](http://kirellbenzi.com/blog/evolution-of-genres-in-the-montreux-jazz-festival/)
- [Data analysis Montreux Jazz Festival](http://kirellbenzi.com/blog/hello-montreux-jazz-festival/)
- [Artist Map of Montreux Jazz Festival](http://kirellbenzi.com/blog/montreux-jazz-festival-artists-map/)
- [Music API in 2016 - all the API related to music](https://www.acrcloud.com/blog/music-apis-the-list-of-2016)
