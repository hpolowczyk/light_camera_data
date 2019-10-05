// Declare the data variable
const data = '/json';

// Using d3, fetch the JSON data
d3.json(data).then((data) => {
    console.log(data)
});
