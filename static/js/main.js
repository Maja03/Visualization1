fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Create Pie Chart for Male data
        createPieChart('males-pie-chart', data.pie.male_counts, data.pie.categories, "Males");

        // Create Pie Chart for Female data
        createPieChart('females-pie-chart', data.pie.female_counts, data.pie.categories, "Females");

        // Create Venn Diagram
        createVennDiagram(data.venn);
    });

function createPieChart(containerId, counts, categories, title) {
    const width = 450, height = 450;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', width + 200) // Adjust for legend space
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const pie = d3.pie().value(d => d.value);
    const arc = d3.arc().outerRadius(radius).innerRadius(0);

    const color = d3.scaleOrdinal(d3.schemeSet3);

    const data = categories.map((label, i) => ({
        label: label,
        value: counts[i]
    }));

    const arcData = pie(data);

    // Draw slices
    svg.selectAll('path')
        .data(arcData)
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => color(i))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

    // Add slice labels
    svg.selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .style('font-size', '10px')
        .style('fill', '#000')
        .text(d => `${d.data.value}`);

    // Add legend with percentage only (no numbers)
    const legend = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', 200)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(10, 20)`); // Move legend slightly to the left

    legend.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', 0)
        .attr('y', (d, i) => i * 20)
        .attr('width', 15)
        .attr('height', 15)
        .attr('fill', (d, i) => color(i));

    legend.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .attr('x', 20)
        .attr('y', (d, i) => i * 20 + 12)
        .style('font-size', '12px')
        .attr('fill', '#333')
        .text(d => `${d.label}: ${((d.value / d3.sum(counts)) * 100).toFixed(2)}%`); // Only percentage

    // Add chart title
    svg.append('text')
        .attr('x', 0)
        .attr('y', -radius - 20)
        .attr('text-anchor', 'middle')
        .style('font-size', '16px')
        .style('font-weight', 'bold')
        .text(`Pie Chart for ${title}`);
}

function createVennDiagram(data) {
    const width = 500, height = 500;
    const svg = d3.select("#venn-diagram")
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const circleRadius = 120; // Increased radius for better clarity
    const circlePadding = 50; // Padding between the circles to make room for the labels and intersections

    const circles = [
        { cx: 160, cy: 200, r: circleRadius, fill: "red", label: "Depressed", count: data.depressed },
        { cx: 340, cy: 200, r: circleRadius, fill: "blue", label: "Anxious", count: data.anxious },
        { cx: 250, cy: 350, r: circleRadius, fill: "green", label: "Panic Attack", count: data.panicking }
    ];

    // Draw the circles for each condition
    circles.forEach(circle => {
        svg.append('circle')
            .attr('cx', circle.cx)
            .attr('cy', circle.cy)
            .attr('r', circle.r)
            .attr('fill', circle.fill)
            .attr('opacity', 0.5) // Make circles semi-transparent
            .attr('stroke', '#000')
            .attr('stroke-width', 2);

        svg.append('text')
            .attr('x', circle.cx)
            .attr('y', circle.cy - circle.r - 10) // Place label above the circle
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', 'bold')
            .style('fill', '#333')
            .text(circle.label);

        svg.append('text')
            .attr('x', circle.cx)
            .attr('y', circle.cy)
            .attr('dy', 20)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px') // Increased font size for count
            .style('fill', '#333')
            .text(circle.count);
    });

    // Remove the intersection in the center
    // No intersection label in the center, keeping only the circle counts

    // Ensure the title for "Panic Attack" is under the green circle
    svg.append('text')
        .attr('x', 250)
        .attr('y', 350 + circleRadius + 15) // Title positioned below the green circle
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .style('fill', '#333')
        .text("Panic Attack");
}
