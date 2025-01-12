fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Create Pie Chart for Male data
        createPieChart('males-pie-chart', data.pie.male_counts, data.pie.categories);

        // Create Pie Chart for Female data
        createPieChart('females-pie-chart', data.pie.female_counts, data.pie.categories);

        // Create Venn Diagram
        createVennDiagram(data.venn);
    });

function createPieChart(containerId, data, categories) {
    const width = 400, height = 400;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const pie = d3.pie().value(d => d.value);
    const arc = d3.arc().outerRadius(radius).innerRadius(0);

    const arcData = pie(data.map((value, i) => ({
        value: value,
        label: categories[i]
    })));

    svg.selectAll('path')
        .data(arcData)
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => d3.schemeSet3[i]);

    svg.selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('dy', '.35em')
        .style('text-anchor', 'middle')
        .text(d => `${d.data.label}: ${d.data.value}`);
}

function createVennDiagram(vennData) {
    const width = 500, height = 500;
    const svg = d3.select("#venn-diagram")
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Simple Venn diagram for three sets
    const circles = [
        { cx: 150, cy: 150, r: 100, fill: "red", label: "Depressed", count: vennData.depressed },
        { cx: 250, cy: 150, r: 100, fill: "blue", label: "Anxious", count: vennData.anxious },
        { cx: 200, cy: 250, r: 100, fill: "green", label: "Panicking", count: vennData.panicking }
    ];

    circles.forEach(circle => {
        svg.append('circle')
            .attr('cx', circle.cx)
            .attr('cy', circle.cy)
            .attr('r', circle.r)
            .attr('fill', circle.fill)
            .attr('opacity', 0.5);

        svg.append('text')
            .attr('x', circle.cx)
            .attr('y', circle.cy)
            .attr('dy', -10)
            .attr('text-anchor', 'middle')
            .text(circle.label);

        svg.append('text')
            .attr('x', circle.cx)
            .attr('y', circle.cy)
            .attr('dy', 20)
            .attr('text-anchor', 'middle')
            .text(circle.count);
    });
}
