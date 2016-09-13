import json
from threading import Timer, RLock

import numpy as np
from flask import Flask, redirect, request, url_for

from tabs import thredds_frame_source

app = Flask(__name__)

RANDOM_STATE = np.random.get_state()


# We should probably maintain a connection for at least a short while
class THREDDS_CONNECTION(object):

    def __init__(self, timeout=300.0, **fs_args):
        """ Create an expiring connection to the THREDDS server.

        The connection will drop after 5 minutes of non-use. Any subsequent
        attempt to use the connection will initiate a new one. Access to the
        connection is RLock'd to ensure only one connection is alive at a time.

        Parameters:
        timeout : int, seconds
            The lenght of time in seconds to hold open a connection.

        Remaining keyword args are passed to the connection's constructor.
        """
        self._fs = None
        self._fs_lock = RLock()
        self._fs_args = fs_args
        self._timer = None
        self.timeout = float(timeout)

    def _forget(self):
        app.logger.info("Closing THREDDS connection")
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self._fs = None

    def _reset_timer(self):
        app.logger.info("Resetting THREDDS connection timer")
        if self._timer:
            self._timer.cancel()
        self._timer = Timer(self.timeout, self._forget)
        self._timer.start()

    def fs():
        doc = "The fs property."

        def fget(self):
            with self._fs_lock:
                if not self._fs:
                    app.logger.info("Opening new THREDDS connection")
                    # Ensure that we get the same ordering of grid points
                    np.random.set_state(RANDOM_STATE)
                    cls = thredds_frame_source.THREDDSFrameSource
                    self._fs = cls(**self._fs_args)
                self._reset_timer()
                return self._fs

        def fset(self, value):
            with self._fs_lock:
                self._fs = value
                self._reset_timer()
                return self._fs

        def fdel(self):
            with self._fs_lock:
                self._forget()
        return locals()
    fs = property(**fs())


tc = THREDDS_CONNECTION(data_uri=thredds_frame_source.DEFAULT_DATA_URI,
                        decimate_factor=60)


def jsonify_dict_of_array(obj):
    """ Return a copy of obj with list and array values turned into lists that
    have been rounded to four decimals. """
    obj = obj.copy()
    for k in obj:
        if isinstance(obj[k], (np.ndarray, list)):
            obj[k] = np.asarray(obj[k]).round(4).tolist()
    return obj


@app.route('/')
def index():
    return redirect(url_for('static', filename='tabs.html'))


# An outline of the region interest

@app.route('/data/prefetched/domain')
def domain():
    """ Return the domain outline """
    filename = 'data/json/domain.json'
    return redirect(url_for('static', filename=filename))


# Retrieve the grid

@app.route('/data/thredds/velocity/grid')
def thredds_grid():
    """ Return the grid points for the velocity frames. """
    return json.dumps(jsonify_dict_of_array(tc.fs.velocity_grid))


@app.route('/data/prefetched/velocity/grid')
def static_grid():
    """ Return the grid points for the velocity frames. """
    filename = 'data/json/grd_locations.json'
    return redirect(url_for('static', filename=filename))


# Retrieve velocity frames

@app.route('/data/thredds/velocity/step/<int:time_step>')
def thredds_velocity_frame(time_step):
    """ Return the velocity frame corresponding to `time_step`. """
    vs = tc.fs.velocity_frame(time_step)
    vs = jsonify_dict_of_array(vs)
    return json.dumps(vs)


@app.route('/data/prefetched/velocity/step/<int:time_step>')
def static_velocity_frame(time_step):
    """ Return the velocity frame corresponding to `time_step`. """
    filename = 'data/json/step{}.json'.format(time_step)
    return redirect(url_for('static', filename=filename))


# Retrieve salinity contours

@app.route('/data/thredds/salt/step/<int:time_step>')
def thredds_salt_frame(time_step):
    num_levels = request.args.get('numSaltLevels', 10)
    logspace = 'logspace' in request.args
    salt = tc.fs.salt_frame(
        time_step, num_levels=num_levels, logspace=logspace)
    return json.dumps(salt)

if __name__ == '__main__':
    app.run(debug=True)
