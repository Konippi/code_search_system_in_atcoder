let beginner = 0;

let dataset = {
    "children": []
};

for(let i=0;i<user_len;i++){
    if(user_value[i] == 0){
        beginner++;
    }
    dataset.children.push({"Name":user_key[i], "Count":user_value[i]});
}

document.getElementById("beginner").innerHTML = "コンテスト未参加者: " + beginner + "名"; 

let diameter = 650;

let color = d3.scaleOrdinal(d3.schemeCategory20);

let bubble = d3.pack(dataset)
    .size([diameter, diameter])
    .padding(1.5);

let svg = d3.select("body")
    .append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

let nodes = d3.hierarchy(dataset)
    .sum(function(d) { return d.Count; });

let node = svg.selectAll(".node")
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

node.append("circle")
    .attr("r", function(d) {
        return 0;
    })
    .style("fill", function(d,i) {
        return color(i);
    })
    .on("mouseover", function() { 
        d3.select(this)
        .attr("stroke", "gray")
        .attr("stroke-width", 4)
    })
    .on("mouseout", function() { 
        d3.select(this)
        .attr("stroke", "white")
        .attr("stroke-width", 1)
    })
    .on("click", function(d) {
        d3.select(this)
        .attr("stroke", "black")
        .attr("stroke-width", 4)
        document.getElementById("user").value = d.data.Name;
        document.getElementById("submit").type = "submit";
    }) ;

node.append("text")
    .attr("dy", "0")
    .attr("text-anchor", "middle")
    .text(function(d) {
        return d.data.Name;
    })
    .attr("font-family", "sans-serif")
    .attr("font-size", function(d){
        return d.r/5;
    })
    .attr("fill", "white");

node.append("text")
    .attr("dy", "1.5em")
    .attr("text-anchor", "middle")
    .text(function(d) {
        return d.data.Count;
    })
    .attr("font-family",  "arial")
    .attr("font-size", function(d){
        return d.r/7;
    })
    .attr("fill", "white");

d3.select(self.frameElement)
    .style("height", diameter + "px");

d3.selectAll("circle")
    .transition()
    .duration(500)
    .delay(function(d, i){
        return i*100;
    })
    .attr("r", function(d) {
        return d.r*1.01;
    })