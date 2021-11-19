var dataset = {
    children: [
        {Name:language_key[0], Count:language_value[0]}
    ]
};
for(var i=1;i<language_len;i++){
    dataset.children.push({Name:language_key[i], Count:language_value[i]});
}

var diameter = 650;

var color = d3.scaleOrdinal(d3.schemeCategory20);

var bubble = d3.pack(dataset)
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select("body")
    .append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

var nodes = d3.hierarchy(dataset)
    .sum(function(d) { return d.Count; });

var node = svg.selectAll(".node")
    .data(bubble(nodes).descendants())
    .enter()
    .filter(function(d){
        return !d.children
    })
    .append("g")
    .attr("class", "node")
    .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

node.append("title")
    .text(function(d) {
        return d.Name + ": " + d.Count;
    });

node.append("circle")
    .attr("r", function(d) {
        return d.r*1.01;
    })
    .style("fill", function(d,i) {
        return color(i);
    })
    .on("mouseover", function() { 
        d3.select(this)
        .attr("stroke", "gray")
        .attr("stroke-width", 6)
    })
    .on("mouseout", function() { 
        d3.select(this)
        .attr("stroke", "white")
        .attr("stroke-width", 1)
    })
    .on("click", function() {
        location.href = 'http://127.0.0.1:5000/Working/Users';
    }) ;

node.append("text")
    .attr("dy", "0")
    .attr("text-anchor", "middle")
    .text(function(d) {
        return d.data.Name;
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", function(d){
        return d.r/7;
    })
    .attr("fill", "white");

node.append("text")
    .attr("dy", "1.5em")
    .attr("text-anchor", "middle")
    .text(function(d) {
        return d.data.Count;
    })
    .attr("font-family",  "Gill Sans", "Gill Sans MT")
    .attr("font-size", function(d){
        return d.r/7;
    })
    .attr("fill", "white");

d3.select(self.frameElement)
    .style("height", diameter + "px");