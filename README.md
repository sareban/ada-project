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
Events data were fetched from `BandsInTown`, `ResidentAdvisor`, `Events.ch` and `La Route des Festivals`, some which had API ready to use to query the data, other that needed to be scrapped manuallly using `BeautifulSoup`. In the end, we were left with **62'000 artists playing in 204'000 events, out in 22'000 venues**. Some more cleaning would be useful, especially with Venues names where tricky duplicates were left.

Furthermore, several music intelligence services like `MusicGraph` or `Spotify`, or broader platforms such as `Wikipedia`, were used to augment the data (music genre and origins of artists). Using `Google Places`, all of the venues were geocoded, to be able to present the data on interactive maps.

## Code description
With the Scrapper notebooks, we scrapped data from all the plateforms we used (BandsInTown, Discogs - abandoned, Events.ch, MusicGraph, ResidentAdvisor, RouteDesFestivals, Spotifiy, Wikipedia). Sometimes, they call on python scripts located in ./Scripts/, where they may also store partial results before we concatenate everything down to single csvs, either in ./Artists/, ./Events/, or ./Venues/.  In the Preprocessing notebooks is our preprocessing pipeline for cleaning and augmenting the data. Then in the Stats notebook, we produce a few graphs for our understanding of the dataset, and the poster too, while in Visualization we produce the interactive maps, and in Visualization2 we create some more viz.

## Results


* The final dat set, in `.csv` format [can be accessed here](https://github.com/sareban/ada-project/blob/master/FinalResults/total_eventsFinal.csv)

* The Interractive heatmap [can be accessed here](http://nbviewer.jupyter.org/github/sareban/ada-project/blob/master/FinalResults/heatmap_swissmusic.html)

[![Screen Shot 2017-02-06 at 10.12.57.png](https://s24.postimg.org/m3ngro1jp/Screen_Shot_2017_02_06_at_10_12_57.png)](http://nbviewer.jupyter.org/github/sareban/ada-project/blob/master/FinalResults/heatmap_swissmusic.html)

* The Interractive map with the details of the places [can be accessed here](http://nbviewer.jupyter.org/github/sareban/ada-project/blob/master/FinalResults/detailedmap_swissmusic.html)

[![Screen Shot 2017-02-06 at 10.10.40.png](https://s29.postimg.org/mi1ssoe3r/Screen_Shot_2017_02_06_at_10_10_40.png)](http://nbviewer.jupyter.org/github/sareban/ada-project/blob/master/FinalResults/detailedmap_swissmusic.html)

* Evolution of genres from 2006 to 2016
<a href="https://plot.ly/~cyril.pecoraro/1/" target="_blank" title="Plot 1" style="display: block; text-align: center;"><img src="https://plot.ly/~cyril.pecoraro/1.png" alt="Plot 1" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
<script data-plotly="cyril.pecoraro:1"  src="https://plot.ly/embed.js" async></script>


* Wordcloud of genres

[![genres.png](https://s28.postimg.org/iy6ryv9ul/genres.png)](https://postimg.org/image/uajdgnijd/)

* Wordcloud of origins of artists

[![orig.png](https://s27.postimg.org/mek3y958z/orig.png)](https://postimg.org/image/ch9356xn3/)

* Final poster of the project presentation at the Applied Machine Learning Days, EPFL, 31/01/17 [can be accessed here](https://github.com/sareban/ada-project/blob/master/poster%20ada.jpg)

[![Screen Shot 2017-02-06 at 10.50.43.png](https://s24.postimg.org/bl0fg8p1x/Screen_Shot_2017_02_06_at_10_50_43.png)](http://nbviewer.jupyter.org/github/sareban/ada-project/blob/master/poster%20ada.jpg)



## Code description

The scrapper notebooks presnts the code used to scrap the data from the platforms (BandsInTown, Discogs - abandoned, Events.ch, MusicGraph, ResidentAdvisor, RouteDesFestivals, Spotifiy, Wikipedia). Sometimes, they call on python scripts located in ./Scripts/, where they may also store partial results before they are concatenate to single csvs, either in `./Artists/`, `./Events/`, or `./Venues/`. The `Preprocessing` notebooks is the preprocessing pipeline for cleaning and augmenting the data. Then in the `Stats` notebook, there are few stats about the dataset, while in `Visualization` the interactive maps are produced using `Folium`, and in `Visualization2` plots and wordclouds are shown.

## Interesting links
- [Mapping the hometowns of billboard hot 100 artists](http://thedataface.com/mapping-the-hometowns-of-billboard-hot-100-artsts/)
- [Le bilan des festivals de l'année 2016](http://www.touslesfestivals.com/actualites/le-bilan-des-festivals-de-lannee-2016-121216)
- [Stats soci-demographiques musique suisse](https://www.bfs.admin.ch/bfs/fr/home/statistiques/culture-medias-societe-information-sport.assetdetail.282381.html)
- [Carte des festivals suisses](https://www.festigo.ch/#!/fr/festimap/all)
- [Evolution of genres in the montreux jazz festival](http://kirellbenzi.com/blog/evolution-of-genres-in-the-montreux-jazz-festival/)
- [Data analysis Montreux Jazz Festival](http://kirellbenzi.com/blog/hello-montreux-jazz-festival/)
- [Artist Map of Montreux Jazz Festival](http://kirellbenzi.com/blog/montreux-jazz-festival-artists-map/)
- [Music API in 2016 - all the API related to music](https://www.acrcloud.com/blog/music-apis-the-list-of-2016)
