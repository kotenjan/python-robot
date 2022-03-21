# python 2

import qi
import argparse
import sys
import motion

def main(session):
    """
    This example uses the getPosition method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")
    names = motion_service.getBodyNames("Body")

    # Example showing how to get the position of the body
    name            = "CameraDepth"
    frame           = motion.FRAME_WORLD
    useSensorValues = True
    result          = motion_service.getPosition(name, frame, useSensorValues)
    print "Position of", name, " in World is:"
    print result
    name            = "CameraTop"
    frame           = motion.FRAME_WORLD
    useSensorValues = True
    result          = motion_service.getPosition(name, frame, useSensorValues)
    print "Position of", name, " in World is:"
    print result
    name            = "CameraBottom"
    frame           = motion.FRAME_WORLD
    useSensorValues = True
    result          = motion_service.getPosition(name, frame, useSensorValues)
    print "Position of", name, " in World is:"
    print result
    for name in names:
        frame           = motion.FRAME_WORLD
        useSensorValues = True
        result          = motion_service.getPosition(name, frame, useSensorValues)
        print "Position of", name, " in World is:"
        print result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default='10.10.48.230',
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)

# x, y, z, wx, wy, wz - positions and rotations
"""
Position of CameraDepth  in World is:
[0.05412835255265236, 0.028521958738565445, 1.0752665996551514, 0.036072809249162674, 0.461076945066452, 0.036183055490255356]
Position of CameraTop  in World is:
[0.10526478290557861, -0.0101948082447052, 1.097477912902832, 0.036072809249162674, 0.461076945066452, 0.036183055490255356]
Position of CameraBottom  in World is:
[0.06614011526107788, -0.007963600568473339, 1.0040802955627441, 0.08064889907836914, 1.1582735776901245, 0.09403740614652634]
Position of HeadYaw  in World is:
[-0.04428064450621605, -0.009731512516736984, 0.9900045394897461, 0.03230533003807068, 0.0072741033509373665, 0.020363284274935722]
Position of HeadPitch  in World is:
[-0.04428064450621605, -0.009731512516736984, 0.9900045394897461, 0.036072809249162674, 0.461076945066452, 0.036183055490255356]
Position of LShoulderPitch  in World is:
[-0.0651128739118576, 0.1424429714679718, 0.9119385480880737, 2.015179395675659, 1.5351170301437378, 2.0232768058776855]
Position of LShoulderRoll  in World is:
[-0.0651128739118576, 0.1424429714679718, 0.9119385480880737, 1.6492893695831299, 1.3938528299331665, 1.656363844871521]
Position of LElbowYaw  in World is:
[-0.06779491156339645, 0.18898946046829224, 0.7361981272697449, -0.3157042860984802, 1.3441526889801025, 0.8893037438392639]
Position of LElbowRoll  in World is:
[-0.06779491156339645, 0.18898946046829224, 0.7361981272697449, -1.2016878128051758, 0.9371947050094604, -0.05585825815796852]
Position of LWristYaw  in World is:
[0.02024896815419197, 0.18412460386753082, 0.6150544881820679, -1.3361297845840454, 0.9401552677154541, -0.055003855377435684]
Position of LHand  in World is:
[0.03496823459863663, 0.18331417441368103, 0.59486323595047, -1.3361297845840454, 0.9401552677154541, -0.055003855377435684]
Position of HipRoll  in World is:
[-0.008711482398211956, 0.0005059251561760902, 0.6809822916984558, -6.177287126263309e-09, 0.007669925224035978, 0.008097453974187374]
Position of HipPitch  in World is:
[-0.009317380376160145, 0.0005010189488530159, 0.6019846200942993, -2.47382536677776e-09, -0.010737896896898746, 0.008097454905509949]
Position of KneePitch  in World is:
[-0.006439773365855217, 0.0005243206396698952, 0.33400002121925354, -3.732708808712459e-09, -1.862645149230957e-09, 0.008097454905509949]
Position of RShoulderPitch  in World is:
[-0.06276310980319977, -0.1568724513053894, 0.9022931456565857, 1.8491207361221313, 1.5372939109802246, 1.8571193218231201]
Position of RShoulderRoll  in World is:
[-0.06276310980319977, -0.1568724513053894, 0.9022931456565857, -1.6458393335342407, 1.4477355480194092, -1.6371270418167114]
Position of RElbowYaw  in World is:
[-0.06397096067667007, -0.19401699304580688, 0.7240006923675537, 0.5239943861961365, 1.3799445629119873, -0.6726657748222351]
Position of RElbowRoll  in World is:
[-0.06397096067667007, -0.19401699304580688, 0.7240006923675537, 1.2915080785751343, 0.9325429797172546, 0.13978341221809387]
Position of RWristYaw  in World is:
[0.02452634833753109, -0.1815652847290039, 0.6035300493240356, 1.4387301206588745, 0.9325429201126099, 0.13978341221809387]
Position of RHand  in World is:
[0.039084188640117645, -0.1797412782907486, 0.5835750102996826, 1.4356002807617188, 0.9342162013053894, 0.13702690601348877]
Position of WheelFL  in World is:
[0.08230218291282654, 0.15624801814556122, 0.07000002264976501, -2.5678965620556937e-09, 2.3911994606606868e-09, 1.083270788192749]
Position of WheelFR  in World is:
[0.08481237292289734, -0.15374185144901276, 0.07000002264976501, -9.825040780953032e-10, -4.162872269120044e-09, -1.0670758485794067]
Position of WheelB  in World is:
[-0.1764342039823532, -0.0008522332645952702, 0.07000002264976501, 3.732709252801669e-09, 1.862645149230957e-09, -3.1334950923919678]
"""

"""
Position of LShoulderPitch  in World is:
[-6.51128739118576, 14.24429714679718, 91.19385480880737, 2.015179395675659, 1.5351170301437378, 2.0232768058776855]
Position of LElbowRoll  in World is:
[-6.779491156339645, 18.898946046829224, 73.61981272697449, -1.2016878128051758, 0.9371947050094604, -0.05585825815796852]
"""