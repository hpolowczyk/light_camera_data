const url = "/map";
data = d3.json(url).then(dataInitial => {
  data = dataInitial;
  console.log(data);
});

console.log("test");
