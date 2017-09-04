from superset import app
import os
#print 'zxc:',os.path.expanduser('~')
app.run(debug=True, host='192.168.75.132', port=8088)
