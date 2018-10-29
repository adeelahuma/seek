
import random
import bokeh.sampledata
from bokeh.sampledata import us_states, us_counties, unemployment
from bokeh.sampledata.stocks import AAPL
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.embed import file_html
from bokeh.resources import CDN
from flask import Flask, render_template
from bokeh.io import show
import pandas as pd


app = Flask(__name__)


@app.route("/")
def begin():
    return render_template('index.html')


@app.route('/trend')
def trend_html():
    return render_template('trend.html')


def trend_graph():

    df = pd.DataFrame(AAPL)
    df['date'] = pd.to_datetime(df['date'])

    # create a new plot with a datetime axis type
    p = figure(title="Job Trend", plot_width=800, plot_height=250, x_axis_type="datetime")

    p.line(df['date'], df['close'], color='navy', alpha=0.5)

    html = file_html(p, CDN, 'trend')
    # script, div = components(p)
    #
    # return render_template('trend.html', the_div=div, the_script=script)
    with open("templates/trend.html", 'w') as f:
        f.write(html)


def create_hover_tool():
    #yet to be coded
    return None


def create_bar_chart(data, title, x_title, y_title,
                     hover_tool=None, width=1200, height=1000):
    # source = ColumnDataSource(data)
    # print(data[x_title])
    # xdr = FactorRange(data[x_title])
    # ydr = Range1d(start=0, end=max(data[y_title]) * 1.5)
    #
    # tools = []
    # if hover_tool:
    #     tools = [hover_tool, ]
    #
    # plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
    #               plot_height=height, h_symmetry=False, v_symmetry=False, min_border=0,
    #               toolbar_location="above", tools=tools, responsive=True,
    #               outline_color="#666666")
    #
    # # glyph = VBar(x=x_title, top=y_title, bottom=0, width=.8,
    # #              fill_color="#e12127")
    # # plot.add_glyph(source, glyph)
    #
    #
    #
    # xaxis = LinearAxis()
    # yaxis = LinearAxis()
    #
    # plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    # plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    # plot.toolbar.logo = None
    # plot.min_border_top = 0
    # plot.xgrid.grid_line_color = None
    # plot.ygrid.grid_line_color = "#999999"
    # plot.yaxis.axis_label = "Bugs found"
    # plot.ygrid.grid_line_alpha = 0.1
    # plot.xaxis.axis_label = "Days after app deployment"
    # plot.xaxis.major_label_orientation = 1

    plot = figure(plot_width=400, plot_height=400)

    # add a circle renderer with a size, color, and alpha
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

    return plot


def job_map():

    states = us_states.data.copy()
    print(states)

    counties = us_counties.data.copy()

    print(counties)

    unemployment_us = unemployment.data

    print(unemployment_us)

    del states["HI"]
    del states["AK"]

    EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

    state_xs = [states[code]["lons"] for code in states]
    state_ys = [states[code]["lats"] for code in states]

    county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
    county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]

    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

    county_colors = []
    for county_id in counties:
        if counties[county_id]["state"] in EXCLUDED:
            continue
        try:
            rate = unemployment_us[county_id]
            idx = int(rate / 6)
            county_colors.append(colors[idx])
        except KeyError:
            county_colors.append("black")

    p = figure(title="Job Map", toolbar_location="left",
               plot_width=1100, plot_height=700)

    p.patches(county_xs, county_ys,
              fill_color=county_colors, fill_alpha=0.7,
              line_color="white", line_width=0.5)

    p.patches(state_xs, state_ys, fill_alpha=0.0,
              line_color="#884444", line_width=2, line_alpha=0.3)

    html = file_html(p, CDN, 'job')

    with open("templates/job_map.html", 'w') as f:
        f.write(html)

    # output_file("choropleth.html", title="choropleth.py example")

    # show(p)
    # show(plot)
    # script, div = components(p)
    # return render_template('job_map.html', the_div=div, the_script=script)


@app.route('/job_map')
def job_html():
    return render_template('job_map.html')


if __name__ == '__main__':
    #app.run(debug=True)
    # job_map()
    # trend_graph()
    app.run(port=33507)