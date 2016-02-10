var ws = new WebSocket("ws://localhost:8080")

ws.onmessage = function(event) {
  data = JSON.parse(event.data)
  console.log(data)
  var hashtag = data["hashtag"].toLowerCase()
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

  var group = d3.select("svg").append("g")
  group.append('circle')
    .attr('r', 4)
    .attr("transform", function(d) {return "translate(" + projection(coordinates)[0] + ',' + projection(coordinates)[1] + ")";})
    .style('fill', color)
    .style('opacity', 1)
    .transition()
    .duration(5000)
    // To keep the dots in place, you could, in theory, comment out/remove this line. 
    .style("opacity", 0); 
  }