import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

import collections

import numpy as np

# import unicodedata

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
# logging.basicConfig(level=logging.DEBUG)
# logging.info("Starting the MediaCloud example Flask app!")

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('mediacloud app')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('mediacloud app')

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("search-form.html")


@app.route("/search",methods=['POST'])

def search_results(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    keywords = request.form['keywords']
    startdate = request.form['startdate']
    enddate = request.form['enddate'] 
    now = datetime.datetime.now()

    results = mc.sentenceCount(keywords,
                               solr_filter=[mc.publish_date_query( datetime.date( 2016, 1, 1), now ),
                                            'tags_id_media:9139487'], split = True, split_start_date=startdate, split_end_date=enddate)
    
    dictwithcounts = results.values()
    datapoints = dictwithcounts[1]
    del datapoints['gap']
    del datapoints['end']
    del datapoints['start']
    datapoints = collections.OrderedDict(sorted(datapoints.items()))
    sorted_key_list = list(datapoints.keys())

    # for date in sorted_key_list:
    #     unicodedata.normalize('NFKD', date).encode('ascii','ignore')
    #     sorted_key_list_nounicode = []
    #     sorted_key_list_nounicode.append(date)
   

    sorted_value_list = list(datapoints.values())

    # final_data = []
    # for i in range(len(sorted_key_list_nounicode)):
    #     final_data.append(np.asarray( [sorted_key_list_nounicode[i],sorted_value_list[i]] ))
            

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Counts', "data": sorted_value_list}]
    title = {"text": 'Graphed Results'}
    xAxis = {"title": {"text": 'Weeks'}}
    yAxis = {"title": {"text": 'Number of Counts'}}

    return render_template("search-results.html",
                           results=results,
                           # final_data = final_data,
                           datapoints=datapoints,
                           # sorted_key_list_nounicode=sorted_key_list_nounicode,
                           sorted_key_list=sorted_key_list,
                           sorted_value_list=sorted_value_list,
                           keywords=keywords,
                           startdate=startdate,
                           enddate=enddate,
                           sentenceCount=results['count'],
                           chartID=chartID, 
                           chart=chart, 
                           series=series, 
                           title=title, 
                           xAxis=xAxis, 
                           yAxis=yAxis )


if __name__ == "__main__":
    #app.debug = True
    app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True)
    #app.run()
