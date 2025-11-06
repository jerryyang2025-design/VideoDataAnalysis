from collections import defaultdict

import cv2
import numpy as np
import csv

from ultralytics import YOLO

from graphs import Frame_Info
import graphs

import pandas as pd

from tkinter import Canvas
import tkinter as tk


from PIL import Image, ImageTk, ImageDraw, ImageChops
import matplotlib.pyplot as plt

# Load the YOLO11 model
model = YOLO("yolo11n.pt")

# Open the video file
video_path = "datasets/retail.mp4"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])




## Saving as Video
# 3. Query input properties for writer
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0


# 4. Create a VideoWriter (here we write MP4, change codec/extension as you like)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out    = cv2.VideoWriter("output_with_tracks.mp4", fourcc, fps, (width, height))

seen_ids = set()
frame_number = 0
cumulative = 0
coords = []
flow = []

current_video_data = []



with open("Logging_Data.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["frame_number", "new_people_count", "total_people_in_frame", "cumulative", "flow", "position_of_objects"])
    
    
    #Dict of the heat trails
    heat_trails = dict()
    
    #overlay = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
    #draw = ImageDraw.Draw(overlay)


    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()    
  

        if success:
            # Run YOLO11 tracking on the frame, persisting tracks between frames
            result = model.track(frame, persist=True)[0]

           # Get the boxes and track IDs
            if result.boxes and result.boxes.is_track:
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()
                class_ids = result.boxes.cls.int().cpu().tolist()
                
              
                
                people_ids = [tid for tid, cls in zip(track_ids, class_ids) if cls ==0]
                
                people_track_ids = []
                new_people_ids = [tid for tid in people_ids if tid not in seen_ids]
                
                for new_id in new_people_ids:
                    heat_trails[new_id] = Image.new('RGBA', (1270, 720), (0, 0, 0, 0))
                    
                
                    

                seen_ids.update(people_ids)
                cumulative += len(new_people_ids)
                
                # Visualize the result on the frame
                frame = result.plot()
                
              
                    
                # Plot the tracks
                for box, track_id in zip(boxes, track_ids):

                    x, y, w, h = box
                    coords.append((track_id, float(x), float(y-h/2)))
                    track = track_history[track_id]
                    track.append((float(x), float(y)))  # x, y center point
                    if len(track) > 30:  # retain 30 tracks for 30 frames
                        track.pop(0)

                    # Draw the tracking lines
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    
             
                    
                
                    
                    #cv2.polylines(frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
                    

                    
                    if track_id in people_ids:
                        
                        
                    # cv2.imshow("OpenCV Image", opencv_image\)
                        
                        
                   
                        
                        #draw the circle
                        radius = 10 
                        x_center = int(x)
                        y_center = int(y) 
                        
                        draw = ImageDraw.Draw(heat_trails[track_id])
                        draw.ellipse((x_center - radius, y_center - radius, x_center + radius, y_center + radius), fill=(255, 0, 0, 40))
                        
                        
                     
                        
                    
                    
                  
                        
                          
                    

                    

                    
                    initial_direction = [0,0]
                    for i in range(1, min(5, len(points))):
                        change_in_x = points[i][0][0] - points[i - 1][0][0]
                        change_in_y = points[i][0][1] - points[i - 1][0][1]
                        initial_direction[0] += int(change_in_x)
                        initial_direction[1] += int(change_in_y)

                    final_direction = [0,0]
                    for i in range(max(len(points) - 5, 1), len(points)):
                        change_in_x = points[i][0][0] - points[i - 1][0][0]
                        change_in_y = points[i][0][1] - points[i - 1][0][1]
                        final_direction[0] += int(change_in_x)
                        final_direction[1] += int(change_in_y)
                        
                    flow.append((initial_direction, final_direction, track_id))
                    
                    if len(points) > 0:
                        start_initial = tuple(points[0][0])
                        end_initial = (int(start_initial[0] + initial_direction[0]), int(start_initial[1] + initial_direction[1]))
                        cv2.arrowedLine(frame, start_initial, end_initial, color=(0,255,0), thickness=2, tipLength=0.3)

                        start_final = tuple(points[-1][0])
                        end_final = (int(start_final[0] + final_direction[0]), int(start_final[1] + final_direction[1]))
                        cv2.arrowedLine(frame, start_final, end_final, color=(0,0,255), thickness=2, tipLength=0.3)
                                
                writer.writerow([frame_number, len(new_people_ids), len(people_ids), cumulative, "-".join(str(p) for p in flow), "-".join(str(p) for p in coords)])
                
                # Store frame item in list
                current_video_data.append(Frame_Info(frame_number, len(new_people_ids), len(people_ids), cumulative, flow, coords))
                
                
                
                coords = []
                flow = []


  
  
            
            combined_trails = Image.new('RGBA', (1270, 720), (0, 0, 0, 0))
            
            for trail in heat_trails:
                combined_trails = ImageChops.add(combined_trails, heat_trails[trail])
            
            
      
            
            color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            pil_image = Image.fromarray(color_converted)
            
            #### DO PIL image conversion
                    
            #pil_image = Image.blend(pil_image, overlay, alpha=0.1)
            pil_image.paste(combined_trails, (0, 0), combined_trails)
            
            ##convert back to opencv
            
            
            open_cv_image = np.array(pil_image)
            
            #### DEBUG
            combined_cv = np.array(combined_trails)
            ######
            
            # Convert RGB(A?) to BG
            
            frame = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2BGR)
            #frame = cv2.cvtColor(combined_cv, cv2.COLOR_RGBA2BGR)  
    

            # Display the annotated frame
            # try:
            cv2.imshow("YOLO11 Tracking", frame)
            # except:
            #      pass  
            
        
            
            # Write frame to video stream
            out.write(frame)
            frame_number += 1
            
        

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break



# generate pandas dataframe csv file
df = pd.DataFrame(current_video_data)

df.to_csv("pandas_csv.csv")




#test

#graphs.generate_customerspertime_graph(df, 0.1)

graphs.generate_scatterplot(df, width/100, height/100)

graphs.generate_averagepeople_graph(df, 0.1)




# Release the video capture objects and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()




