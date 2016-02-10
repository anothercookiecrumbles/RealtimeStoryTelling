<!-- Creates the initial world map. --> 

/** Needs to be accessed by the WebSocket layer to ensure that the circles are projected correctly. 
Hence, this is a global variable. */
var projection; 

function drawMap() {
  /** Specifies the dimensions in which the map will be drawn. */
  var width = 970,
  height = 800;

  var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

  /** Load the world.json file. This file was generated using: Natural Earth's 1:10m map, which 
      contains the country's polygons (http://www.naturalearthdata.com/http//www.naturalearthdata
      .com/download/10m/cultural/ne_10m_admin_0_map_subunits.zip)

      In order to generate the TopoJSON, I followed this tutorial: 
      https://bost.ocks.org/mike/map/. 
  */
  d3.json("world.json", function(error, world) {
    var path = d3.geo.path();
    // Pull out the country polygons from the (topo)json file. 
    var featureCollection = topojson.feature(world, world.objects.places);
    // ...and creates the bounds for these "features." 
    // @see https://github.com/mbostock/d3/wiki/Geo-Paths#bounds
    var bounds = d3.geo.bounds(featureCollection);

    // Necessary to center the map correctly based on the latitude/longitude returned. 
    var centerX = d3.sum(bounds, function(d) {return d[0];}) / 2
    var centerY = d3.sum(bounds, function(d) {return d[1];}) / 2

    console.log(centerX)
    console.log(centerY)

    projection = d3.geo.mercator()
      .scale(130)
      /* Added offset to Y-axis to ensure it looks properly centered. Essentially, this means 
         that Antarctica's dropped off the map. I _think_ this is acceptable considering no one's 
         tweeting from Antarctica, but...? */ 
      .center([centerX, centerY+75]);  

    // Add the projection to the path, and finally, draw the map. 
    path.projection(projection);
    svg.selectAll("path")
      .data(featureCollection.features)
      .enter().append("path")
      .attr("d", path);
  }); 
}