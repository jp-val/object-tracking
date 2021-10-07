import cv2 as cv

GREEN = (0, 255, 0)

capture = cv.VideoCapture("highway.mp4")

object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
	isTrue, frame = capture.read();
	
	height, width, _ = frame.shape
	# print(height, width)

	rio = frame[340:720, 500: 800] # focuses on a video region

	mask = object_detector.apply(rio)
	_, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY) # removes shadows
	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	
	for cnt in contours:
		area = cv.contourArea(cnt)
		if area > 100:
			# cv.drawContours(rio, [cnt], -1, GREEN, 2)
			x, y, w, h, = cv.boundingRect(cnt)
			cv.rectangle(rio, (x, y), (x+w, y+h), GREEN, 3)
	
	# cv.imshow("video", frame)
	# cv.imshow("masked video", mask)
	cv.imshow("rio", rio)

	if cv.waitKey(20) & 0xFF==ord('d'):
		break
	
capture.release()
cv.destroyAllWindows()