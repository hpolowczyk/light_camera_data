// Declare the data variable
d3.selectAll("#selDataset").on("change", getValue);
d3.selectAll("#selList").on("change", searchValue);

var myMap;

function getValue() {
  var valueSelect = d3.select("#selDataset").node().value;
  var data = "/filterLessRange_IG_Rank/" + valueSelect;
  // Using d3, fetch the JSON data
  d3.json(data).then(data => {
    // console.log(data);
    populateList(data);
  });
}

function searchValue() {
  var valueSelect = d3.select("#selList").node().value;
  getMovie(valueSelect);
}

function populateList(data) {
  var selectOpt = d3.select("#selList");
  selectOpt.html("");
  for (var i = 0; i < data.length; i++) {
    var selectValues = data[i].movie_name;
    selectOpt
      .append("option")
      .text("Rank: " + data[i].rank + " - " + selectValues)
      .attr("value", function() {
        return data[i].rank;
      });
  }
}

function getMovie(rank) {
  var dataMongo = "/filterLessEq_IG_Rank/" + rank;
  d3.json(dataMongo).then(dataMongo => {
    // console.log(data);
    showMap(dataMongo);
  });
}

function RemoveExistingMap(myMap) {
  if (myMap != null) {
    myMap.remove();
    myMap = null;
  }
}

function showMap(data) {
  RemoveExistingMap(myMap);
  // Create a map object
  myMap = L.map("map", {
    center: [15.5994, -28.6731],
    zoom: 2
  });

  L.tileLayer(
    "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox.light",
      accessToken: API_KEY
    }
  ).addTo(myMap);

  for (var i = 0; i < data.length; i++) {
    // get the first 10 countries
    var count = 0;
    var totalForeign = data[i].foreign_total_gross;

    d3.selectAll("#valueInt").text(
      "Total Amount Foreing: $" + data[i].foreign_total_gross
    );

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

      if (city == "South Korea") {
        latitude = 35.9;
        longitude = 127.76;
      } else if (city == "India") {
        latitude = 20.59;
        longitude = 78.96;
      }

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
