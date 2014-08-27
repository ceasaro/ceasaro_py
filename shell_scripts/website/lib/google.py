def create_line_chart(data):
    chart_data = [data[0].keys()]
    for stat in data:
        chart_data.append(stat.values())

    print chart_data
