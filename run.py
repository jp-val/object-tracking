import cv2 as cv
from tracker import *

capture = cv.VideoCapture("highway.mp4")
object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
tracker = EuclideanDistTracker()

while True:
	isTrue, frame = capture.read();
	
	# height, width, _ = frame.shape
	# print(height, width)

	rio = frame[340:720, 500: 800] # select video region

	# object detection
	mask = object_detector.apply(rio)
	_, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY) # removes shadows
	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	detections = []

	for cnt in contours:
		area = cv.contourArea(cnt)
		if area > 100:
			# cv.drawContours(rio, [cnt], -1, (0, 255, 0), 2)
			x, y, w, h, = cv.boundingRect(cnt)
			cv.rectangle(rio, (x, y), (x+w, y+h), (0, 255, 0), 3)
			detections.append([x, y, w, h])
	
	# object tracking
	boxes_ids = tracker.update(detections)
	# print(boxes_ids)
	for box_id in boxes_ids:
		x, y, w, h, ident = box_id
		cv.putText(rio, str(ident), (x, y-15), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
		cv.rectangle(rio, (x, y), (x+w, y+h), (0, 255, 0), 3)

	# cv.imshow("video", frame)
	# cv.imshow("masked video", mask)
	cv.imshow("rio", rio)

	if cv.waitKey(20) & 0xFF==ord('d'):
		break
	
capture.release()
cv.destroyAllWindows()