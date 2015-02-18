import numpy as np
import cv2
import cv2.cv as cv
import facetracker
import traceback
from SimpleCV import *
from video import create_capture
from common import clock, draw_str
import pdb

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''
try_me = 10
if __name__ == '__main__':
    import sys, getopt
    print help_message
    
    args, video_src = getopt.getopt(sys.argv[1:], '', ['face=', 'con=', 'tri='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    face_fn = args.get('--con', r"../external/FaceTracker/model/face2.tracker")
    con_fn = args.get('--con', r"../external/FaceTracker/model/face.con")
    tri_fn  = args.get('--tri', r"../external/FaceTracker/model/face.tri")

    tracker = facetracker.FaceTracker(face_fn)
    # Tracker init variables
    

    conns = facetracker.LoadCon(con_fn)
    trigs = facetracker.LoadTri(tri_fn)

    cam = create_capture(video_src, width=800,height=600)
    tracker.setWindowSizes((11,9,7))

    try:
        while True:
            t = clock()
            
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            cv2.imshow('facedetect', gray)
            if tracker.update(gray):
                draw_str(img, (20, 40), 'pos: %.1f, %.1f' % tracker.getPosition())
                draw_str(img, (20, 60), 'scale: %.1f ' % tracker.getScale())
                draw_str(img, (20, 80), 'orientation: %.1f, %.1f, %.1f' % tracker.getOrientation())
                tracker.getScale()
                tracker.getOrientation()
                img = tracker.draw(img, conns, trigs)


            else:
                tracker.setWindowSizes((11, 9,7))
            dt = clock() - t
    
            # Draw eyes ONLY MY CODE
            faceShape= tracker.get2DShape()[0]
            
            MAX_SIZE = 132 / 2
            left_eye_x, left_eye_y = faceShape[36:42],faceShape[36+MAX_SIZE:42+MAX_SIZE]

            MIN_X = MIN_Y = float("+inf")
            MAX_X = MAX_Y = float("-inf")

            for i in range(len(left_eye_x)):
                x = int(round(left_eye_x[i]))
                y = int(round(left_eye_y[i]))

                # Debug to check if eye is found
                # draw_str(img, (x, y), '*')

                if(x > MAX_X):
                    MAX_X = x
                if(x < MIN_X):
                    MIN_X = x

                if(y > MAX_Y):
                    MAX_Y = y
                if(y < MIN_Y):
                    MIN_Y = y
            MAX_Y += 10
            MAX_X += 10
            MIN_Y -= 10
            MIN_X -= 10
            # Get LEFT_EYE INTO Image
            subset_img = gray[MIN_Y:MAX_Y, MIN_X:MAX_X]
            # Transpose suc that (y,x) -> (x,y)
            _img = Image(np.transpose(subset_img))
            bm = BlobMaker() # create the blob extractor
            # invert the image so the pupil is white, threshold the image, and invert again
            # and then extract the information from the image
            blobs = _img.findBlobs()
            if(len(blobs)>0): # if we got a blob
                blobs[0].draw() # the zeroth blob is the largest blob - draw it
                locationStr = "("+str(blobs[0].x)+","+str(blobs[0].y)+")"
                # write the blob's centroid to the image
                # _img.dl().text(locationStr,(0,0),color=Color.RED)
                # save the image
    
                _img.save("eye_only_1.png")
                # and show us the result.
                pdb.set_trace()

                _img.show()
            # END MY CODE
            # draw_str(img, (20, 20), 'time: %.1f ms' % (dt*1000))
            # cv2.rectangle(img, (MIN_X, MIN_Y), (MAX_X, MAX_Y), (255,0,0), 2)
            cv2.imshow('facedetect', img)

            if 0xFF & cv2.waitKey(5) == 27:
                break
    except Exception, err:
        print traceback.format_exc()

        
    cv2.destroyAllWindows() 			

