var ws = new WebSocket("ws://localhost:8080")

ws.onmessage = function(event) {
  console.log(event.data)
  var latLong = JSON.parse("[" + event.data + "]");

  var group = d3.select("svg").append("g")
  group.append('circle')
    .attr('r', 4)
    .attr("transform", function(d) {return "translate(" + projection(latLong)[0] + ',' + projection(latLong)[1] + ")";})
    .style('fill', 'red')
    .style('opacity', 1)
    .transition()
    .duration(5000)
    // To keep the dots in place, you could, in theory, comment out/remove this line. 
    .style("opacity", 0); 
  }