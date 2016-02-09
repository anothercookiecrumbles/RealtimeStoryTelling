<!-- Creates the initial world map. --> 

var projection; 

function drawMap() {
  var width = 970,
  height = 800;

  var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

  d3.json("world.json", function(error, world) {
    var path = d3.geo.path();
    var featureCollection = topojson.feature(world, world.objects.places);
    var bounds = d3.geo.bounds(featureCollection);

    var centerX = d3.sum(bounds, function(d) {return d[0];}) / 2
    var centerY = d3.sum(bounds, function(d) {return d[1];}) / 2

    projection = d3.geo.mercator()
      .scale(130)
      .center([centerX, centerY+75]); // Added offset to Y-axis to ensure it looks properly centered. 

    path.projection(projection);
    svg.selectAll("path")
      .data(featureCollection.features)
      .enter().append("path")
      .attr("d", path);
  }); 
}