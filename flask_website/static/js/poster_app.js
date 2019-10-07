// Declare the data variable
const data = '/json';

// Using d3, fetch the JSON data
d3.json(data).then((data) => {
       
    var randomNum = Math.floor(Math.random() * (250)) + 1;
    
    buildPoster(randomNum)
    
    function buildPoster(num) {
        var start = num-1
        var end = num
        data.slice(start,end).forEach((movie) => {
            var poster = movie.Poster;
            var x = document.createElement("IMG");
            x.setAttribute("src", "poster");
            x.setAttribute("width", "200px");
            x.setAttribute("alt", "poster");
            document.getElementById("item").appendChild(x);
        })    
    }
});




