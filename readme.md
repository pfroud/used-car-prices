# Used car prices

View results of 700+ cars at **[https://chart-studio.plotly.com/dashboard/pfroud0:4/view](https://chart-studio.plotly.com/dashboard/pfroud0:4/view)**!

<p align="center" style="text-align: center">
<a href="https://chart-studio.plotly.com/dashboard/pfroud0:4/view">
<img src="dashboard-screenshot.png?raw=true" alt="screenshot of graphs"></a>
</p>

## Background

When shopping for a used car, how does model year and odometer mileage affect price? To find out, I wrote scripts to scrape data from the websites of car dealerships.

## Data source

I was shopping for a midsize sedan. To minimize the number of variables, I only looked at Camrys from Toyota dealerships and Accords from Honda dealerships, both in the San Francisco Peninsula.

Here are the Toyota and Honda dealerships in the area. I scraped data from almost all of them.

<table><tr><td>
AutoNation Toyota Hayward                        <br>
Capitol Toyota (San Jose)                        <br>
City Toyota (Daly City)                          <br>
Fremont Toyota                                   <br>
<del>Magnussen's Toyota of Palo Alto</del>*      <br>
Melody Toyota (San Bruno)                        <br>
Piercey Toyota (Milpitas)                        <br>
Putnam Toyota (Burlingame)                       <br>
San Francisco Toyota                             <br>
<del>Stevens Creek Toyota (San Jose)</del>**     <br>
Toyota 101 (Redwood City)                        <br>
Toyota Sunnyvale                                 <br>
</td><td>                                        <br>
Anderson Honda (Palo Alto)                       <br>
AutoNation Honda Fremont                         <br>
Capitol Honda (San Jose)                         <br>
Honda Redwood City                               <br>
Honda of Hayward                                 <br>
Honda of Serramonte (Colma, close to Daly City)  <br>
Honda of Stevens Creek                           <br>
Larry Hopkins Honda (Sunnyvale)                  <br>
Ocean Honda of Burlingame                        <br>
San Francisco Honda                              <br>
South Bay Honda (Milpitas)                       <br>
Victory Honda of San Bruno                       <br>
</td></tr></table>

\* At the time this tool was written, Toyota of Palo Alto didn't list the mileage for each car when viewing search results. This was extremely stupid, so I didn't use data from that dealership.

\*\* Stevens Creek Toyota [loads data](http://www.stevenscreektoyota.com/used-vehicles/certified-pre-owned-vehicles/#action=im_ajax_call&perform=get_results&_post_id=6&make%5B%5D=Toyota&page=1&show_all_filters=false&model%5B%5D=Camry) with an asynchronous request that uses cookies and a nonce. I couldn't be bothered to bypass it.

## Vizualization

I tried [Plotly](https://plot.ly/) for generating and hosting my plots. It works but the web-based backend is terrible. The plots are made from the [July 30th 2017 dataset](output%2007-30-2017/output.csv).

The data has three dimensions, so a 3D scatter plot seemed like an obvious choice. It turns out 3D plots are difficult to understand when viewed on a 2D screen.

I also made 2D scatter plots with for each combination of dimensions. These plots use two spacial dimensions and one color dimension, so they contain all the information but are much easier to digest.

- [2D scatter plot of price vs year](https://plot.ly/~pfroud0/5.embed)
- [2D scatter plot of miles vs year](https://plot.ly/~pfroud0/3.embed)
- [2D scatter plot of price vs miles](https://plot.ly/~pfroud0/2.embed)
- [3D scatter plot of price vs miles vs year](https://plot.ly/~pfroud0/1.embed)

## Discussion

I observed these trends:

* Odometer mileage is inversely proportional to price ([view plot](https://plot.ly/~pfroud0/2.embed)). This makes sense&mdash;lower miles demand high prices. 
* Model year is directly proportial to price ([view plot](https://plot.ly/~pfroud0/5.embed)). This also makes sense&mdash;newer cars sell for more.
* For model years 2011 and newer, odometer mileage is inversely proportional to model year ([view plot](https://plot.ly/~pfroud0/3.embed)). This makes sense&mdash;newer models have less time to accumulate miles.
* For model years 2005 and older, odometer mileage is directly proportional to model year ([view plot](https://plot.ly/~pfroud0/3.embed)). This is unexpected&mdash;in some cases, newer cars have more odometer miles than older cars.
