import execnet
import json
from constants import *


head_rotation = -7
hip_rotation = 25
table_height = 743
object_height = 40


def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec(
        """
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
        """ 
        % 
        (Module, Function)
    )
    channel.send(ArgumentList)
    return channel.receive()


call_python_version("2.7", "positions", "prepare_for_movement", [ROBOT_IP])
relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_body", [[hip_rotation, head_rotation], ROBOT_IP]))
relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [[115, 0, 0, 0, 0], ROBOT_IP]))
