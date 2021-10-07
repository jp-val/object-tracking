import math

class EuclideanDistTracker:
	def __init__(self):
		self.center_points = {}
		self.id_count = 0 # tracks next available id

	def update(self, objects_rect):
		objects_bbs_ids = []

		# calculates center point of new object
		for rect in objects_rect:
			x, y, w, h = rect
			cx = (x + x + w) // 2
			cy = (y + y + h) // 2

			# checks if that object was detected already
			same_object_detected = False
			for ident, pt in self.center_points.items():
				dist = math.hypot(cx - pt[0], cy - pt[1])

				if dist < 25:
					self.center_points[ident] = (cx, cy)
					# print(self.center_points)
					objects_bbs_ids.append([x, y, w, h, ident])
					same_object_detected = True
					break

			# assigns id if new object is detected
			if same_object_detected is False:
				self.center_points[self.id_count] = (cx, cy)
				objects_bbs_ids.append([x, y, w, h, self.id_count])
				self.id_count += 1

		# removes old ids form object no longer in the video
		new_center_points = {}
		for obj_bb_id in objects_bbs_ids:
			_, _, _, _, object_id = obj_bb_id
			center = self.center_points[object_id]
			new_center_points[object_id] = center

		self.center_points = new_center_points.copy()
		return objects_bbs_ids