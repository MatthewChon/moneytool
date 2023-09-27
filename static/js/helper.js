function construct_new_graph(graph_name, graph_type, label, data_json) {
    const graph = document.getElementById(graph_name);
    const components = parse_json_to_components(data_json);
    const data = {
        labels: components[0],
        datasets: [{
            label: label,
            data: components[1],
            borderWidth: 1
        }]
    }
    new Chart(graph, {type: graph_type, data: data} );
}
function parse_json_to_components(category_demographic) {
    const labels = []
    const data = []
    for (key in category_demographic) {
        labels.push(key);
        data.push(category_demographic[key]);
    }
    return [labels, data]
}