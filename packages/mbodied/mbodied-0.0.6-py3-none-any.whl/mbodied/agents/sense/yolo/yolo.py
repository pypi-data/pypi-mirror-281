import supervision as sv
from ultralytics import YOLOv10

#!pip install supervision git+https://github.com/THU-MIG/yolov10.git


class Yolo:
    def __init__(self, model_path):
        self.model = YOLOv10(model_path)

    def get_objects(self, image, categories):
        results = self.model(
            source=image, verbose=True, conf=0.1, show_labels=True, show_conf=True, imgsz=image.size()
        )[0]
        detections = sv.Detections.from_ultralytics(results)
        box_annotator = sv.BoundingBoxAnnotator()

        category_dict = dict(enumerate(categories))

        labels = [
            f"{category_dict[class_id]} {confidence:.2f}"
            for class_id, confidence in zip(detections.class_id, detections.confidence, strict=False)
        ]
        return box_annotator.annotate(
            image.copy(),
            detections=detections,
            labels=labels,
        )
