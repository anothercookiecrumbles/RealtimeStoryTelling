var ws = new WebSocket("ws://localhost:8080")

/**
  * Invoked when we receive a message over websocket from the server. 
  * @param: event: The MessageEvent received from the server that contains the data that we are 
      interested in. 
*/
ws.onmessage = function(event) {
  data = JSON.parse(event.data)
  console.log(data)
  var hashtag = data["hashtag"].toLowerCase() // easier for string comparisons 
  var coordinates = data["coordinates"]

  // The colour codes are based on the logo colours of each of the organisations. 
  // The hex codes have been picked using the eyedrop on each company's logo (in Pixelmator).
  if (hashtag === 'apple') {
    color = 'white' // well, we've all seen Apple products. 
  } else if (hashtag === 'facebook') {
    color = '#3c5998'
  } else if (hashtag === 'netflix') {
    color = '#e42113'
  } else if (hashtag === 'amazon') {
    color = '#fd9a18'
  } else if (hashtag === 'alphabet' || hashtag == 'google') {
    color = '#35a953' // As the other colours of the Google/Alphabet logo are taken, using green. 
  }

  /* Finds the map in d3 and projects a circle of radius 4 on the map, which is displayed and then 
  fades out five seconds later. */ 
  var group = d3.select("svg").append("g")
  group.append('circle')
    .attr('r', 4) // radius of the circle 
    // ensure that the circle is projected correctly based on how the map was initially constructed. 
    .attr("transform", function(d) {return "translate(" + projection(coordinates)[0] + ',' + 
      projection(coordinates)[1] + ")";}) 
    .style('fill', color) 
    .style('opacity', 1) 
    .transition()
    .duration(5000) 
    // To keep the dots in place, you could, in theory, comment out/remove this line. 
    .style("opacity", 0); 
  }