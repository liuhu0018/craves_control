import numpy as np
import cv2
import cv2.aruco as aruco
from craves_control.utils.trans import *
mtx = np.array([[646.443762,         0.,  330.047528],
                [0.,         643.573914,  235.385833],
                [0.,                 0.,          1.]])
dist = np.array([[0.031048, -0.108917, 0.000667, -0.001048, 0.000000]])


def track_aruco(frame):
    # operations on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):
        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

        for i in range(0, ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)

        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0]) + ', '

        cv2.putText(frame, "Id: " + strg, (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # display the resulting frame
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    return rvec, tvec


def get_relative(frame):
    # operations on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)
    font = cv2.FONT_HERSHEY_SIMPLEX
    xyz_new = None
    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(ids != None):

        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.06, mtx, dist)

        for i in range(0, ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
            R = euler_matrix(rvec[i][0][0], rvec[i][0][1], rvec[i][0][2])
            T = translation_matrix(tvec[i][0])
            if ids[i][0] == 1:
                cam2base = concatenate_matrices(T, R)
            elif ids[i][0] == 2:
                cam2target = concatenate_matrices(T, R)

        if ids.size == 2:
            base_pos = translation_from_matrix(cam2base)
            target_pos = translation_from_matrix(cam2target)
            xyz_cam = target_pos - base_pos
            xyz = np.dot(cam2base[:3, :3], xyz_cam)
            xyz_new = [xyz[1], xyz[0], xyz[2]]
            # xyz_new = [xyz[0], -xyz[2], xyz[1]]

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners)

        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):
            strg += str(ids[i][0]) + ', '

        cv2.putText(frame, "Id: " + strg, (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # display the resulting frame
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    return xyz_new