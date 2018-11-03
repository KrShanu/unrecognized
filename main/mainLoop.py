def isThresholdPassed(count,threshold):
    if count < threshold:
        return False
    else
        return True

THRESHOLD = 1
lastFrameInSecond = False
positive_detection = False #this represents main out value. Should it just be int?
frame_index = 0
detections = 0
FPS = 30

#for each second in file, check if enough frames contain face. If enough, output True (1) to CSV and skip to next second. Else output False(0) 
while (not endOfFile):

    
    #do image processing, face detection, threshold calculation (if we're doing that)
    #...
    #...

    thresholdPassed = isThresholdPassed(detections, THRESHOLD)
    
    #We have some threshold for positive detection, eg: six images in a second
    if thresholdPassed = True:
        positive_detection = True
        
        outputResultToCSV(indexToNearestSecond(frame_index, FPS), 1, path)   #csv row == [SECOND, INT_VALUE]
        
        #reset variables, jump index to start of next second
        positive_detection = False
        lastFrameInSecond = False
        frame_index += (FPS - frame_index)  #0-> FPS, FPS-1 -> FPS
        continue

    if frame_index % FPS == 0:  #FPS == 30, 29 -> 29, 30 -> 0
        
        outputResult(indexToNearestSecond(frame_index, FPS), 0, path)  #csv row == [SECOND, INT_VALUE]
        
        #reset variables, jump index to start of next second
        positive_detection = False
        lastFrameInSecond = False
        continue

    frame_index ++
    
