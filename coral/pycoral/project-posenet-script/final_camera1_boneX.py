import argparse

import collections 

from functools import partial

import re

import time

 

import numpy as np

from PIL import Image

import svgwrite

import gstreamer

 

from pose_engine import PoseEngine

from pose_engine import KeypointType

#fcm

from pyfcm import FCMNotification

from firebase_admin import messaging

import firebase_admin

from firebase_admin import credentials

 

import threading

from threading import Thread

 

isfall = False

 

EDGES = (

    (KeypointType.NOSE, KeypointType.LEFT_EYE),

    (KeypointType.NOSE, KeypointType.RIGHT_EYE),

    (KeypointType.NOSE, KeypointType.LEFT_EAR),

    (KeypointType.NOSE, KeypointType.RIGHT_EAR),

    (KeypointType.LEFT_EAR, KeypointType.LEFT_EYE),

    (KeypointType.RIGHT_EAR, KeypointType.RIGHT_EYE),

    (KeypointType.LEFT_EYE, KeypointType.RIGHT_EYE),

    (KeypointType.LEFT_SHOULDER, KeypointType.RIGHT_SHOULDER),

    (KeypointType.LEFT_SHOULDER, KeypointType.LEFT_ELBOW),

    (KeypointType.LEFT_SHOULDER, KeypointType.LEFT_HIP),

    (KeypointType.RIGHT_SHOULDER, KeypointType.RIGHT_ELBOW),

    (KeypointType.RIGHT_SHOULDER, KeypointType.RIGHT_HIP),

    (KeypointType.LEFT_ELBOW, KeypointType.LEFT_WRIST),

    (KeypointType.RIGHT_ELBOW, KeypointType.RIGHT_WRIST),

    (KeypointType.LEFT_HIP, KeypointType.RIGHT_HIP),

    (KeypointType.LEFT_HIP, KeypointType.LEFT_KNEE),

    (KeypointType.RIGHT_HIP, KeypointType.RIGHT_KNEE),

    (KeypointType.LEFT_KNEE, KeypointType.LEFT_ANKLE),

    (KeypointType.RIGHT_KNEE, KeypointType.RIGHT_ANKLE),

)

 

 

msg = messaging.Message(

            data={

                "title" : '낙상사고가 발생했습니다',

                "content" : 'content'

                },

                topic = "fall"

            )

 

def shadow_text(dwg, x, y, text, font_size=16):

    dwg.add(dwg.text(text, insert=(x + 1, y + 1), fill='black',

                     font_size=font_size, style='font-family:sans-serif'))

    dwg.add(dwg.text(text, insert=(x, y), fill='white',

                     font_size=font_size, style='font-family:sans-serif'))

 

 

def draw_pose(dwg, pose, src_size, inference_box, color='yellow', threshold=0.2):

    box_x, box_y, box_w, box_h = inference_box

    scale_x, scale_y = src_size[0] / box_w, src_size[1] / box_h

    xys = {}

    global min_x 

    global min_y

    global max_x 

    global max_y 

    min_x = 640

    min_y = 480

    max_x = 0

    max_y = 0

    

    for label, keypoint in pose.keypoints.items():

        if keypoint.score < threshold: continue

        # Offset and scale to source coordinate space.

        kp_x = int((keypoint.point[0] - box_x) * scale_x)

        kp_y = int((keypoint.point[1] - box_y) * scale_y)

 

        #dwg.add(dwg.circle(center=(int(box_x), int(box_y)), r=5,

        #                   fill='cyan', fill_opacity=keypoint.score, stroke='blue'))

 

        xys[label] = (kp_x, kp_y)


         #if label>=0 or label<4:

          #   global nose_x

           #  global nose_y

            # nose_x = int(kp_x)

             #nose_y = int(kp_y)

    global nose_x

    global nose_y

    global rshoulder_x

    global rshoulder_y

    global lshoulder_x

    global lshoulder_y

    global cshoulder_x

    global cshoulder_y

    rshoulder_x = 0

    rshoulder_y = 0

    lshoulder_x = 0

    lshoulder_y = 0

                                                                                                                                                                                                                       

    for a, b in EDGES:

        if a not in xys or b not in xys: continue

        ax, ay = xys[a]

        bx, by = xys[b]

        

        

        if a>=0 or a<4:

            nose_x = ax

            nose_y = ay

        if a==7:           

            lshoulder_x = ax

            lshoulder_y = ay

            rshoulder_x = bx

            rshoulder_y = by

 

        if ax <= min_x:

            min_x = ax

        if ay <= min_y:

            min_y = ay

        if ax >= max_x:

            max_x = ax

        if ay >= max_y:

            max_y = ay

        if bx <= min_x:

            min_x = bx

        if by <= min_y:

            min_y = by

        if bx >= max_x:

            max_x = bx

        if by >= max_y:

            max_y = by

 



 

    # bounding box

    #dwg.add(dwg.line(start=(min_x, min_y), end=(max_x, min_y), stroke='red', stroke_width=2))

    #dwg.add(dwg.line(start=(min_x, min_y), end=(min_x, max_y), stroke='red', stroke_width=2))

    #dwg.add(dwg.line(start=(max_x, min_y), end=(max_x, max_y), stroke='red', stroke_width=2))

    #dwg.add(dwg.line(start=(min_x, max_y), end=(max_x, max_y), stroke='red', stroke_width=2))

    global aa

    global bb

 

    aa = (max_x + min_y)/2

    bb = (min_x + max_y)/2

 

    cshoulder_x = (lshoulder_x + rshoulder_x)/2

    cshoulder_y = (lshoulder_y + rshoulder_y)/2

 

    

 

def avg_fps_counter(window_size):

    window = collections.deque(maxlen=window_size)

    prev = time.monotonic()

    yield 0.0  # First fps value.

 

    while True:

        curr = time.monotonic()

        window.append(curr - prev)

        prev = curr

        yield len(window) / sum(window)

 

 

def run(inf_callback, render_callback):

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--mirror', help='flip video horizontally', action='store_true')

    parser.add_argument('--model', help='.tflite model path.', required=False)

    parser.add_argument('--res', help='Resolution', default='640x480',

                        choices=['480x360', '640x480', '1280x720'])

    parser.add_argument('--videosrc', help='Which video source to use', default='/dev/video3')

    parser.add_argument('--h264', help='Use video/x-h264 input', action='store_true')

    parser.add_argument('--jpeg', help='Use image/jpeg input', action='store_true')

    args = parser.parse_args()

           
    #default_model = 'models/mobilenet/posenet_mo=bilenet_v1_075_%d_%d_quant_decoder_edgetpu.tflite'

    default_model = 'models/resnet/posenet_resnet_50_416_288_16_quant_edgetpu_decoder.tflite'

    if args.res == '480x360':

        src_size = (640, 480)

        appsink_size = (480, 360)

        model = args.model or default_model

    elif args.res == '640x480':

        src_size = (640, 480)

        appsink_size = (640, 480)

        model = default_model

    elif args.res == '1280x720':

        src_size = (1280, 720)

        appsink_size = (1280, 720)

        model = args.model or default_model

    print('Loading model: ', model)

    engine = PoseEngine(model)

    input_shape = engine.get_input_tensor_shape()

    inference_size = (input_shape[2], input_shape[1])

 

    gstreamer.run_pipeline(partial(inf_callback, engine), partial(render_callback, engine),

                           src_size, inference_size,

                           mirror=args.mirror,

                           videosrc=args.videosrc,

                           h264=args.h264,

                           jpeg=args.jpeg

                           )

 


   

 

def thread_run1():

    

    global hs_x1

    global hs_y1     

    global hs_x2

    global hs_y2

        

    hs_x1=0

    hs_y1=0

    

    hs_x1 = (nose_x + cshoulder_x)/2

    hs_y1 = (nose_y + cshoulder_y)/2

    

    #print(hs_x1)

    #print(hs_y1)

    time.sleep(0.125)

    

 

 

def check_stand():

    start = time.time()

    global isfall

    

    while True:

        

        #box_h = max_x - min_x

        #box_w = max_y - min_y

        end = time.time()

        result = end-start

     

        # 5초 안지났는데 일어나면 낙상X

        if result<5.00 and aa<=bb:

            isfall = False

            print("No Fall    time: %.2f"%result)

            #print("time: %.2f"%result)

            return

    

        # 5초 지났는데 안일어나면 낙상    

        if result>=5.00 and aa>bb and isfall==True:

            print("Fall!!    time: %.2f"%result)

            

            #print("Fall!!")

            sendToTopic()

#            

#             result_msg = messaging.send(msg)

#             print(result_msg)

            #time.sleep(10)

#             print("end")

            isfall = False

            

            return

      

 

    return

    

def thread_run2():

    

    

    global hs_x1

    global hs_y1     

    global hs_x2

    global hs_y2

        

    hs_x2 = (nose_x + cshoulder_x)/2

    hs_y2 = (nose_y + cshoulder_y)/2

    

    #print(hs_x2)

    #print(hs_y2)

 

def thread_run3():

    s = ((hs_x1 - hs_x2)**2 + (hs_y1 - hs_y2)**2)**(1/2)

    

    global v

    global isfall

    v = s / 0.25 

#     print(v)

    if v > 100 and v < 900:

        if aa>=bb:

            #sendToTopic()

#             print(v)

            if isfall == False:

                

                print("===========================")

                print("WARNING")

                print("===========================")

                x4 = threading.Thread(target=thread_run4)

                x4.start()

                isfall = True

            #check_stand()    

    

def thread_run4():

    check_stand()

# API키

 

#push_service = FCMNotification(api_key = "AAAAkfLQ-3c:APA91bFVvNgMDdetbydjM7ax0sI9oKGmpIQ_CLjkIzhgDihROTJw62ragzix_nlCbKH8pWg34gipeOalSDUC4XVrChKw41i3oSdLjjnMoXeBg-cjO8rXAGdQXcBuCnqkfwKW3F35eLyB")

 

# token

#registrationToken = "com.google.android.gms.tasks.zzw@f64c4a9"

 

cred = credentials.Certificate("/home/pi/test-8bbfd-firebase-adminsdk-13vf7-aa0228e5c4.json")

 

firebase_admin.initialize_app(cred)

 

def sendToTopic():

    msg = messaging.Message(

        data={

            "title" : '낙상사고가 발생했습니다',

            "content" : 'content'

            },

            topic = "fall"

    )

    result = messaging.send(msg)

    print(result)

 

def main():

   

    n = 0

    sum_process_time = 0

    sum_inference_time = 0

    ctr = 0

    fps_counter = avg_fps_counter(30)

 

    def run_inference(engine, input_tensor):

        return engine.run_inference(input_tensor)

 

    def render_overlay(engine, output, src_size, inference_box):

        nonlocal n, sum_process_time, sum_inference_time, fps_counter

 

        svg_canvas = svgwrite.Drawing('', size=src_size)

        start_time = time.monotonic()

        outputs, inference_time = engine.ParseOutput()

        end_time = time.monotonic()

        n += 1

        sum_process_time += 1000 * (end_time - start_time)

        sum_inference_time += inference_time * 1000

 

        avg_inference_time = sum_inference_time / n

        text_line = 'PoseNet: %.1fms (%.2f fps) TrueFPS: %.2f Nposes %d' % (

            avg_inference_time, 1000 / avg_inference_time, next(fps_counter), len(outputs)

        )

        

 

        shadow_text(svg_canvas, 10, 20, text_line)

        

        for pose in outputs:          

            draw_pose(svg_canvas, pose, src_size, inference_box)

        #x1 = threading.Thread(target=thread_run1)

        #print("111-thread start-111")

        #x1.start()

        thread_run1()

        #x1.join()

        #print("111-thread join-111")

        

        time.sleep(0.125)

        

        outputs, inference_time = engine.ParseOutput()

        for pose in outputs:          

            draw_pose(svg_canvas, pose, src_size, inference_box)

        #x2 = threading.Thread(target=thread_run2)

        

        #print("222-thread start-222")

        #x2.start()

        #x2.join()

        thread_run2()

        #print("222-thread join-222")

        #x3 = threading.Thread(target=thread_run3)

        #x3.start()

        #x3.join()

        thread_run3()

        

       

        return (svg_canvas.tostring(), False)

 

    

 

    

    run(run_inference, render_overlay)

    

# ******************************************************

    

    

    

            

 

       

    

    

 

    

    

    

    

    

 

 

if __name__ == '__main__':

    main()

    
