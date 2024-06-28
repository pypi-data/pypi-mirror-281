from flask import redirect, url_for, request, render_template, g
from .qmt import init_qmt

def init_error(app):

    app.config['qmt_succ'] = False

    @app.before_request
    def check_error():
        if (request.endpoint in ['auth', 'authorize', 'error'] or request.path.startswith('/static')) or app.config['qmt_succ']:
            return
        try:
            init_qmt()
            app.config['qmt_succ'] = True
        except:
            return redirect(url_for('error', message='您未启动QMT独立交易模式(MiniQMT)，请开启后刷新页面重试。'))
        
    @app.route('/error')
    def error():
        message = request.args.get('message', '出错了')
        return render_template('error.html', message=message)