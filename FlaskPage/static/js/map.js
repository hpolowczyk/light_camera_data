// Declare the data variable
d3.selectAll("#selDataset").on("change", populateList);

var valueSelect = d3.select("#selDataset").node().value;
var data = "/filterLessEq_IG_Rank/" + valueSelect;
// Using d3, fetch the JSON data
d3.json(data).then(data => {
  console.log(data);
  populateList(data);
  showMap(data);
});

function populateList(data) {
  for (var i = 0; i < data.length; i++) {
    var selectValues = data[i].movie_name;

    var selectOpt = d3.select("#selList");
    selectOpt
      .append("option")
      .text(selectValues)
      .attr("value", function() {
        return selectValues;
      });
  }
}

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

  for (var i = 0; i < data.length; i++) {
    // get the first 10 countries
    var count = 0;
    var totalForeign = data[i].foreign_total_gross;

    for (var j = 0; j < data[i].Foreign.length; j++) {
      var city = data[i].Foreign[j].country;
      var localTotal = data[i].Foreign[j].total_gross;
      var percent = (localTotal / totalForeign) * 100;

      // Create a new marker cluster group
      var markers = L.markerClusterGroup();

      // Set the data location property to a variable
      var latitude = data[i].Foreign[j].latitude;
      var longitude = data[i].Foreign[j].longitude;
      var population = data[i].Foreign[j].population;
      var language = data[i].Foreign[j].language;

      // Check for location property
      if (location) {
        // Add a new marker to the cluster group and bind a pop-up
        markers.addLayer(
          L.marker([latitude, longitude]).bindPopup(
            "<table>" +
              "<tr><td>" +
              "<img src=" +
              data[i].img_movie +
              "width='100' height='110'></td>" +
              "<td> <h3>City: " +
              city +
              "</h3><h4>Language: " +
              language +
              "<p>Toal value: " +
              localTotal +
              "<p>Global percent: " +
              percent.toString().substring(0, 4) +
              "%" +
              "<p>Population: " +
              population +
              "</h4></td></table>"
          )
        );
      }

      // Add our marker cluster layer to the map
      myMap.addLayer(markers);
    }
  }
}
