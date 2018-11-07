
import random
from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral3
import numpy as np

app = Flask(__name__)

df = pd.read_pickle('data/application_data.pickle')
company_names = np.unique(df.company_name).tolist()


@app.route("/")
def begin():
    return render_template('index.html')


def plot_trend(c_name):
    # step-1: filter data by company
    # step-2: plot
    # c_name = 'Amazon'

    plot_df = df[df.company_name == c_name]


    ## bokeh plot

    source = ColumnDataSource(plot_df)

    p = figure(x_axis_type='datetime')

    p.line(x='year_month_01',
           y='emp_begin',
           source=source,
           legend='# of Employees (Start of month)',
           color=Spectral3[0],
           line_width=2)

    p.line(x='year_month_01',
           y='emp_end',
           source=source,
           legend='# of Employees (End of month)',
           color='red', line_width=2)

    p.title.text = 'Employee growth trend for ' + c_name
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of employees on platform'

    hover = HoverTool()
    hover.tooltips = [
        ('Employees at the start of month', '@emp_begin'),
        ('Employees at the end of month', '@emp_end'),
        ('Month/Year', '@year_month_01 ')
    ]

    p.add_tools(hover)

    return p


# function that'll be used during plotting so that left/join bars can be of different colors
def get_turn_over_data_by_color(df):
    df_left = df[['company_name', 'year_month_01', 'left_per_month']]
    df_left.rename(columns={'left_per_month': 'emp'}, inplace=True)
    df_left['color'] = 'red'
    df_left['legend'] = 'left'

    df_joined = df[['company_name', 'year_month_01', 'joined_per_month']]
    df_joined.rename(columns={'joined_per_month': 'emp'}, inplace=True)
    df_joined['color'] = 'blue'
    df_joined['legend'] = 'joined'

    df_emp_count = pd.concat([df_joined, df_left], axis=0)

    return df_emp_count


def emp_turn_over_plot(company, negativeAxis=False):

    plot_df = df[df.company_name == company]

    df_turn_over_plot = get_turn_over_data_by_color(plot_df)

    if negativeAxis:
        # for left employees multiply with -1 so that they appear on negative y-axis
        df_turn_over_plot['modified_emp'] = np.where(df_turn_over_plot.color == 'red',
                                                     df_turn_over_plot.emp * -1,
                                                     df_turn_over_plot.emp * 1)

    source = ColumnDataSource(df_turn_over_plot)
    p = figure(x_axis_type='datetime')

    if negativeAxis:
        p.vbar(x='year_month_01', width=5,
               top='modified_emp',
               source=source,
               color='color',
               legend='legend')
    else:
        p.vbar(x='year_month_01', width=5,
               top='emp',
               source=source,
               color='color',
               legend='legend')

    p.title.text = 'Employee Turn-over for ' + company
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Number of employees left or joined'

    hover = HoverTool()
    hover.tooltips = [
        ('Employees(left/joined)', '@emp'),
        ('Month/Year', '@year_month_01 ')
    ]

    p.add_tools(hover)

    return p

@app.route('/employee_turn_over')
def emp_turn_over():

    company = request.args.get('company_name')
    print('name: ', company)

    if company == None:
        company = 'Apple'

    p1 = emp_turn_over_plot(company, False)
    script1, div1 = components(p1)

    p2 = emp_turn_over_plot(company, True)
    script2, div2 = components(p2)

    return render_template('employee_turn_over.html',
                           the_div1=div1, the_script1=script1,
                           the_div2=div2, the_script2=script2,
                           company_names=company_names, selected_company=company)


@app.route('/trend')
def trend_graph():
    #
    # df = pd.DataFrame(AAPL)
    # df['date'] = pd.to_datetime(df['date'])
    #
    # # create a new plot with a datetime axis type
    # p = figure(title="Job Trend", plot_width=800, plot_height=250, x_axis_type="datetime")
    #
    # p.line(df['date'], df['close'], color='navy', alpha=0.5)
    p = plot_trend()

    script, div = components(p)

    return render_template('trend.html', the_div=div, the_script=script)


@app.route('/employee_growth_trend')
def emp_growth_trend():

    company = request.args.get('company_name')
    print('name: ', company)

    if company == None:
        company = 'Apple'

    p = plot_trend(company)

    script, div = components(p)

    return render_template('employee_growth_trend.html',
                           the_div=div, the_script=script,
                           company_names=company_names, selected_company=company)


@app.route('/job_map')
def job_map():
    print('job trend called')
    # states = us_states.data.copy()
    # print(states)
    #
    # counties = us_counties.data.copy()
    #
    # print(counties)
    #
    # unemployment_us = unemployment.data
    #
    # print(unemployment_us)
    #
    # del states["HI"]
    # del states["AK"]
    #
    # EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")
    #
    # state_xs = [states[code]["lons"] for code in states]
    # state_ys = [states[code]["lats"] for code in states]
    #
    # county_xs = [counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
    # county_ys = [counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]
    #
    # colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    #
    # county_colors = []
    # for county_id in counties:
    #     if counties[county_id]["state"] in EXCLUDED:
    #         continue
    #     try:
    #         rate = unemployment_us[county_id]
    #         idx = int(rate / 6)
    #         county_colors.append(colors[idx])
    #     except KeyError:
    #         county_colors.append("black")
    #
    # p = figure(title="Job Map", toolbar_location="left",
    #            plot_width=1100, plot_height=700)
    #
    # p.patches(county_xs, county_ys,
    #           fill_color=county_colors, fill_alpha=0.7,
    #           line_color="white", line_width=0.5)
    #
    # p.patches(state_xs, state_ys, fill_alpha=0.0,
    #           line_color="#884444", line_width=2, line_alpha=0.3)
    #
    #
    # script, div = components(p)
    #
    # return render_template('job_map.html', the_div=div, the_script=script)


# @app.before_request
# def before_request():
#     init_data()


if __name__ == '__main__':
    # app.run(port=33507)
    app.run(debug=True)
