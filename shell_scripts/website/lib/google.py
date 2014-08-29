from datetime import datetime
import os
import json
from lib import stats


def create_line_chart(data, template='template/google-line-chart.html', html_output_file='google-line-chart.html'):
    chart_data = [data[0].keys()]
    for stat in data:
        stat[stats.TIMESTAMP_MILLIS_KEY] = datetime.fromtimestamp(stat[stats.TIMESTAMP_MILLIS_KEY]/1000.0).strftime('%Y-%m-%d %H:%M:%S')
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
