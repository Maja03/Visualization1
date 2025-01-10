// Fetch data from the server
fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Venn Diagram Data
        const venn = data.venn;

        // Bar Chart Data
        const bar = data.bar;

        // Pie Chart Data
        const pie = data.pie;

        // Example Bar Chart
        const svg = d3.select("#visualization2")
            .append("svg")
            .attr("width", 500)
            .attr("height", 300);

        const x = d3.scaleBand()
            .domain(bar.labels)
            .range([0, 400])
            .padding(0.1);

        const y = d3.scaleLinear()
            .domain([0, d3.max(bar.male.concat(bar.female))])
            .range([300, 0]);

        svg.selectAll('.bar-male')
            .data(bar.male)
            .enter()
            .append('rect')
            .attr('x', (d, i) => x(bar.labels[i]))
            .attr('y', d => y(d))
            .attr('width', x.bandwidth())
            .attr('height', d => 300 - y(d))
            .attr('fill', 'blue');

        svg.selectAll('.bar-female')
            .data(bar.female)
            .enter()
            .append('rect')
            .attr('x', (d, i) => x(bar.labels[i]) + x.bandwidth() / 2)
            .attr('y', d => y(d))
            .attr('width', x.bandwidth() / 2)
            .attr('height', d => 300 - y(d))
            .attr('fill', 'orange');
    });
