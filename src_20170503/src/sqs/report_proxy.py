# -*- coding:utf-8 -*-

import flask
from config import report_conf
import cognosreporthelper as report
import simplejson as json
from flask.ext.cors import CORS
from flask.ext.cors import cross_origin
from sqs import Report as SqsReport
from flask import send_from_directory
from sqs.proc_template import TemplateProc
from sqs.excelutil import excel_writer
import StringIO
import datetime
import sys
from flask import current_app
app = flask.Flask(__name__)
#CORS(app)


@app.route('/report_proxy/<engine_name>/<report_name>')
@cross_origin()
def gen_report(engine_name, report_name):
    engine_name = engine_name.lower()
    result = '{}'
    if "cognos" == engine_name:
        result = report.get_report(
            report_name=report_name,
            args=flask.request.args.to_dict(),
            report_conf=report_conf)
    elif "sqs" == engine_name:
        args = flask.request.args.to_dict()
        if flask.request.args.to_dict().get("export"):      #导出则全部导出
            args["export"] = 1
            args["choose"] = 1
        sqs = SqsReport(code=report_name,
                        args=args,
                        report_conf=report_conf)
        result = sqs.get_data()


    if flask.request.args.to_dict().get("export"):
        print report_name
        output = StringIO.StringIO()
        file_name = "%s.xlsx" % report_name
        data = json.loads(result)
        if excel_writer(file_name, data,output) == False:
            tp = TemplateProc(file_name)
            print "before data:", str(datetime.datetime.now()) 
            print "after data:", str(datetime.datetime.now()) 
            tp.get_excel(data)
            print "after excel:", str(datetime.datetime.now()) 
            tp.wb.save(output)
            print "after save:", str(datetime.datetime.now()) 
        response = flask.Response(mimetype='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response.headers['Content-Disposition'] = 'attachment; filename='+ file_name
        response.data = output.getvalue() 
        return response

    return json_response(result)


@app.route('/report_proxy/<engine_name>/<conversation_id>/<action>')
@cross_origin()
def gen_report_convo(engine_name, conversation_id, action):
    engine_name = engine_name.lower()
    result = '{}'
    if "cognos" == engine_name:
        result = report.get_report_convo(
            conversation_id, action, report_conf=report_conf)
    elif "sqs" == engine_name:
        pass
    return json_response(result)


def json_response(json_str):
    resp = flask.Response(json_str)
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/js/<path:path>")
def static_js(path):
    return send_from_directory('js', path)

@app.route("/<master>/proxy.html")
def proxy(master):
    return """
<!DOCTYPE HTML>
<script src="/js/xdomain.min.js" master="http://%s"></script>            
""" % (master)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)
