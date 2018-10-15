# Getting Started



Here, I go through the exact process of connecting to the HSR.

First, ensure the robot is on. Then, hit the red e-stop, wait a few seconds, and release. The wrist should look firm when it's ready.

Then, make a virtualenv that can connect to the HSR and test moving its arm. It worked for me.

```
seita@hermes1:~$ virtualenv --system-site-packages --python=python2 seita-venvs/py2-hsr-extensions
Running virtualenv with interpreter /usr/bin/python2
New python executable in /home/seita/seita-venvs/py2-hsr-extensions/bin/python2
Also creating executable in /home/seita/seita-venvs/py2-hsr-extensions/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.

seita@hermes1:~$ source seita-venvs/py2-hsr-extensions/bin/activate

(py2-hsr-extensions) seita@hermes1:~$ ipython
WARNING: Attempting to work in a virtualenv. If you encounter problems, please install IPython inside the virtualenv.
Python 2.7.12 (default, Dec  4 2017, 14:50:18) 
Type "copyright", "credits" or "license" for more information.

IPython 2.4.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: import hsrb_interface

In [2]: exit


(py2-hsr-extensions) seita@hermes1:~$ ihsrb
---------------------------------------------------------------------------
RobotConnectionError                      Traceback (most recent call last)
/opt/ros/kinetic/bin/ihsrb in <module>()
     36 _robot.enable_interactive()
     37 
---> 38 with Robot() as robot:
     39     whole_body = robot.try_get('whole_body')
     40     omni_base = robot.try_get('omni_base')

/opt/ros/kinetic/lib/python2.7/dist-packages/hsrb_interface/robot.pyc in __init__(self, *args, **kwargs)
    273         use_tf_client = kwargs.get('use_tf_client', False)
    274         if Robot._connection is None or Robot._connection() is None:
--> 275             self._conn = _ConnectionManager(use_tf_client=use_tf_client)
    276             Robot._connection = weakref.ref(self._conn)
    277         else:

/opt/ros/kinetic/lib/python2.7/dist-packages/hsrb_interface/robot.pyc in __init__(self, use_tf_client)
    128             master.getUri()  # Examine a master connection
    129         except Exception as e:
--> 130             raise exceptions.RobotConnectionError(e)
    131         disable_signals = _is_interactive()
    132         if not rospy.core.is_initialized():

RobotConnectionError: [Errno 111] Connection refused

(py2-hsr-extensions) seita@hermes1:~$ hsrb_mode 

<hsrb>~$ ihsrb
HSR-B Interactive Shell 0.2.0


      ____________  ______  _________       __  _______ ____
     /_  __/ __ \ \/ / __ \/_  __/   |     / / / / ___// __ \
      / / / / / /\  / / / / / / / /| |    / /_/ /\__ \/ /_/ /
     / / / /_/ / / / /_/ / / / / ___ |   / __  /___/ / _, _/
    /_/  \____/ /_/\____/ /_/ /_/  |_|  /_/ /_//____/_/ |_|


In [1]: import hsrb_interface

In [2]: robot = hsrb_interface.Robot()

In [3]: omni_base = robot.get('omni_base')

In [4]: whole_body = robot.get('whole_body')

In [5]: import numpy as np

In [6]: whole_body.move_to_joint_positions({'arm_flex_joint': -np.pi/16.0})

In [7]: exit
Leaving HSR-B Interactive Shell
```

And it worked for me.

If you are experiencing trouble connecting to the robot and executing commands is not working, make sure you have set up your bashrc correctly. You can do this by calling:

```
$ gedit ~/.bashrc
```

Make sure that you have set up the network interface correctly. Your bashrc should contain the following:

```
# please set network-interface
network_if=enp0s31f6 # found by typing `ifconfig`

if [ -e /opt/ros/kinetic/setup.bash ] ; then
    source /opt/ros/kinetic/setup.bash
else
    echo "ROS packages are not installed."
fi

export TARGET_IP=$(LANG=C /sbin/ifconfig $network_if | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*')
if [ -z "$TARGET_IP" ] ; then
    echo "ROS_IP is not set."
else
    export ROS_IP=$TARGET_IP
fi

export ROS_HOME=~/.ros
alias sim_mode='export ROS_MASTER_URI=http://localhost:11311 export PS1="\[\033[44;1;37m\]<local>\[\033[0m\]\w$ "'
alias hsrb_mode='export ROS_MASTER_URI=http://hsrb.local:11311 export PS1="\[\033[41;1;37m\]<hsrb>\[\033[0m\]\w$ "'
```

In addition, for general debugging, make sure you have called
```
$ source /opt/ros/kinetic/setup.bash
```

Lastly, to verify that you are connected to the robot, you can call
```
$ rostopic list
```
which will list out a significantly long list of ros topics related to the HSR. If the list is short (~10 lines), it may be because the red stop button is still pressed.

```
$ rqt_image_view
```
Is also useful to see from the robot's camera perspective.
