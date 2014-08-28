import os
import json

def create_line_chart(data, template='template/google-line-chart.html', html_output_file='google-line-chart.html'):
    chart_data = [data[0].keys()]
    for stat in data:
        chart_data.append(stat.values())

    infile = open(os.path.join(os.getcwd(), template))
    outfile = open(os.path.join(os.getcwd(), html_output_file), 'w')

    replacements = {'{{ google_graph_data }}': json.dumps(chart_data)}

    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)
    infile.close()
    outfile.close()
