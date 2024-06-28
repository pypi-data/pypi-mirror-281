from flask import render_template
from xtquant import xtdata

def miniqmt_setting():
    return {
        # 'connect': xtdata.connect()
    }
def init_setting(app, scheduler):
    @app.route('/setting')
    def setting():
        data = {
            'miniqmt': miniqmt_setting(),
            'jobs': scheduler.get_jobs()
        }
        
        print(data, 'data')
        print(xtdata.data_dir, 'xtdata.data_dir')
        return render_template('setting.html', data=data)