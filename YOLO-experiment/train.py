from ultralytics import YOLO

# Load model
model = YOLO("yolo11s-cls.pt")
# Train model
results = model.train(
    data="datasets",
    model="yolo11s-cls.pt", 
    epochs=300, 
    batch=16, 
    imgsz=640, 
    device="0", 
    project="output_dir", 
    name="yolo11s_SGD_300epoch_crop_2diseasesPredia", 
    workers=128, 
    optimizer="SGD", 
    amp=True, 
    half=True,
    dnn=True
    )