import cv2
import numpy as np
import sys
from pathlib import Path

CLASSES = ['beaver', 'boar', 'deer', 'hare', 'lynx', 'wolf']
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def get_classes():
    classes = []
    with open("classes.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            classes.append(line.rstrip())
    return classes


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]}'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 5)
    cv2.putText(img, label, (x + 30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 3)


def return_image(onnx_model, input_image):
    # Load the ONNX model
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)

    # Load names of classes (there should be txt file with every class in each line)
    CLASSES = get_classes()

    # Read the input image
    original_image: np.ndarray = cv2.imread(input_image)
    [height, width, _] = original_image.shape

    # Prepare a square image for inference
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image

    # Calculate scale factor
    scale = length / 640

    # Preprocess the image and prepare blob for model
    blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
    model.setInput(blob)

    # Perform inference
    outputs = model.forward()

    # Prepare output array
    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    # Iterate through output to collect bounding boxes, confidence scores, and class IDs
    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)

    # Apply NMS (Non-maximum suppression)
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    detections = []

    # Iterate through NMS results to draw bounding boxes and labels
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        detection = {
            'class_id': class_ids[index],
            'class_name': CLASSES[class_ids[index]],
            'confidence': scores[index],
            'box': box,
            'scale': scale}
        detections.append(detection)
        draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                          round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

    
    original_image = cv2.resize(original_image, (480, 480))

    # Display the image with bounding boxes
    # cv2.imshow('image', original_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    file_extension = Path(input_image).suffix

    # Save the image with bounding boxes to a temporary file
    output_image_path = "detected_img" + file_extension
    cv2.imwrite(output_image_path, original_image)

    return output_image_path

if __name__ == '__main__':
    return_image('best.onnx', sys.argv[1])