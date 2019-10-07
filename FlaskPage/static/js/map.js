// Declare the data variable
const data = "/filterLessEq_IG_Rank/1";
const data2 = "/filterLessEq_IG_Dom/500000000";
const data3 = "/filterLessEq_IG_Int/500000000";

// Using d3, fetch the JSON data
d3.json(data).then(data => {
  console.log(data);
  showMap(data);
});

// Using d3, fetch the JSON data
d3.json(data2).then(data2 => {
  console.log(data2);
});

d3.json(data3).then(data3 => {
  console.log(data3);
});

function tableList(data) {}

function showMap(data) {
  // Create a map object
  var myMap = L.map("map", {
    center: [15.5994, -28.6731],
    zoom: 3
  });

  L.tileLayer(
    "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox.streets-basic",
      accessToken: API_KEY
    }
  ).addTo(myMap);

  var countryApi = "https://restcountries.eu/rest/v2/name/" + "Argentina";

  d3.json(countryApi, function(response) {
    console.log(response);
  });
  for (var i = 0; i < data.length; i++) {
    // get the first 10 countries
    var count = 0;
    var totalForeign = data[0].foreign_total_gross;
    for (var j = 0; j < data[i].Foreign.length; i++) {
      var city = data[i].Foreign[j].country;
      var localTotal = data[i].Foreign[j].total_gross;
      var percent = (localTotal / localTotal) * 100;
      var countryApi = "https://restcountries.eu/rest/v2/name/" + city;

      d3.json(countryApi, function(response) {
        // Create a new marker cluster group
        var markers = L.markerClusterGroup();

        // Set the data location property to a variable
        var location = response[0].latlng;
        var population = response[0].population;

        // Check for location property
        if (location) {
          // Add a new marker to the cluster group and bind a pop-up
          markers.addLayer(
            L.marker([location[1], location[0]]).bindPopup(
              "<h1>" + city + "</h1> <hr> <h3> Percent: " + percent + "%"
            )
          );
        }

        // Add our marker cluster layer to the map
        myMap.addLayer(markers);
      });
    }
  }
  // for (var i = 0; i < countries.length; i++) {
  //   // Conditionals for countries points
  //   var color = "";
  //   if (countries[i].points > 200) {
  //     color = "yellow";
  //   } else if (countries[i].points > 100) {
  //     color = "blue";
  //   } else if (countries[i].points > 90) {
  //     color = "green";
  //   } else {
  //     color = "red";
  //   }

  //   // Add circles to map
  //   L.circle(countries[i].location, {
  //     fillOpacity: 0.75,
  //     color: "white",
  //     fillColor: color,
  //     // Adjust radius
  //     radius: countries[i].points * 1500
  //   })
  //     .bindPopup(
  //       "<h1>" +
  //         countries[i].name +
  //         "</h1> <hr> <h3>Points: " +
  //         countries[i].points +
  //         "</h3>"
  //     )
  //     .addTo(myMap);
  // }
}
