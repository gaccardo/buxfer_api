import os

from flask import Flask, make_response, request

from buxfer_commands import daemon
import settings

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.from_object(__name__)

@app.route('/buxfer/report')
def get_report():
    d = daemon.BuxferDaemon()

    import ipdb;ipdb.set_trace()

    if request.args.get('email') == '1':
        d.send_report(http=False)
    else:
        d.send_report(http=True)

    report_path = os.path.join(settings.REPORT_TMP, 
        settings.REPORT_NAME)

    with open(report_path, 'rb') as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s' % \
            os.path.basename(report_path)

        f.close()

    return response