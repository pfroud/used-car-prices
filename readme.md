# Used car prices

Scrapes data on used cars for graphing. View results of 700+ cars at **[https://plot.ly/dashboard/pfroud0:4/present](https://plot.ly/dashboard/pfroud0:4/present)**.

<p align="center" style="text-align: center">
<a href="https://plot.ly/dashboard/pfroud0:4/present">
<img src="dashboard-screenshot.png?raw=true" alt="screenshot of graphs"></a>
</p>

To keep things boring, I only look at Camrys from Toyota dealerships and Accords from Honda dealerships, both in the San Francisco Peninsula.


### Dealerships scraped

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

\* Toyota of Palo Alto [doesn't list](https://www.toyotapaloalto.com/used-toyota-camry-palo-alto-ca) mileage for each car when viewing search results. I don't reward bad design, so I don't use their data.

\*\* Stevens Creek Toyota [loads data](http://www.stevenscreektoyota.com/used-vehicles/certified-pre-owned-vehicles/#action=im_ajax_call&perform=get_results&_post_id=6&make%5B%5D=Toyota&page=1&show_all_filters=false&model%5B%5D=Camry) with an awful asyncronous request that uses cookies and a nonce. I couldn't (be bothered to) get around it.

