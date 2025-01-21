fetch('/data')
    .then(response => response.json())
    .then(data => {
        console.log("Fetched data:", data);

        // Render charts based on the available container elements
        if (document.querySelector('#males-pie-chart')) {
            createPieChart('males-pie-chart', data.pie.male_counts, data.pie.categories, "Males");
        }
        if (document.querySelector('#females-pie-chart')) {
            createPieChart('females-pie-chart', data.pie.female_counts, data.pie.categories, "Females");
        }
        if (document.querySelector('#venn-diagram')) {
            createVennDiagram(data.venn);
        }
    })
    .catch(error => console.error("Error fetching data:", error));

function createPieChart(containerId, counts, categories, title) {
    const width = 550, height = 550;
    const radius = Math.min(width, height) / 2;

    // Validate input data
    if (!categories || !counts || categories.length !== counts.length) {
        console.error(`Invalid data for ${title}: Categories and counts do not match.`, { categories, counts });
        return;
    }

    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', width + 200)
        .attr('height', height + 100)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const pie = d3.pie().value(d => d.value);
    const arc = d3.arc().outerRadius(radius).innerRadius(0);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const total = counts.reduce((sum, count) => sum + count, 0);
    const data = categories.map((label, i) => ({
        label: label || "Unknown",
        value: counts[i] || 0,
        percentage: counts[i] ? ((counts[i] / total) * 100).toFixed(2) : 0
    }));

    console.log(`Processed Data for ${title}:`, data);

    const arcData = pie(data);

    // Draw pie slices
    svg.selectAll('path')
        .data(arcData)
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', (d, i) => color(i))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

    // Add percentage labels inside the pie slices
    svg.selectAll('text')
        .data(arcData)
        .enter()
        .append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('fill', '#000')
        .text(d => `${d.data.percentage}%`);

    // Add legend
    const legendContainer = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', 300)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(20, 20)`);

    legendContainer.append('text')
        .attr('x', 0)
        .attr('y', 0)
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text("Legend (Number of People)");

    legendContainer.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', 0)
        .attr('y', (d, i) => i * 20 + 20)
        .attr('width', 15)
        .attr('height', 15)
        .attr('fill', (d, i) => color(i));

    legendContainer.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .attr('x', 20)
        .attr('y', (d, i) => i * 20 + 33)
        .style('font-size', '12px')
        .attr('fill', '#333')
        .text(d => `${d.label}: ${d.value} people`);
}


function createVennDiagram(data) {
    const width = 700, height = 700;
    const svg = d3.select("#venn-diagram")
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const circles = [
        { cx: 200, cy: 250, r: 150, color: "orange", label: "Depressed", value: data.depressed, labelX: 200, labelY: 90 },
        { cx: 400, cy: 250, r: 150, color: "purple", label: "Anxious", value: data.anxious, labelX: 400, labelY: 90 },
        { cx: 300, cy: 400, r: 150, color: "green", label: "Panic Attacks", value: data.panicking, labelX: 300, labelY: 580 }
    ];

    circles.forEach(circle => {
        svg.append('circle')
            .attr('cx', circle.cx)
            .attr('cy', circle.cy)
            .attr('r', circle.r)
            .attr('fill', circle.color)
            .attr('opacity', 0.5)
            .attr('stroke', '#000')
            .attr('stroke-width', 1.5);

        svg.append('text')
            .attr('x', circle.labelX)
            .attr('y', circle.labelY)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .style('font-weight', 'bold')
            .text(circle.label);

        svg.append('text')
            .attr('x', circle.cx)
            .attr('y', circle.cy + 10)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .text(circle.value);
    });

    const overlaps = [
        { x: 300, y: 230, value: data.depressed_anxious },
        { x: 350, y: 325, value: data.anxious_panicking },
        { x: 250, y: 325, value: data.depressed_panicking },
        { x: 300, y: 300, value: data.all_three }
    ];

    overlaps.forEach(overlap => {
        svg.append('text')
            .attr('x', overlap.x)
            .attr('y', overlap.y)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', 'bold')
            .style('fill', '#000')
            .text(overlap.value);
    });
}
