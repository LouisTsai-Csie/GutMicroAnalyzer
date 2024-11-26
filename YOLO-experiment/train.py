from ultralytics import YOLO

# Load a model
# model = YOLO("yolo11n.yaml")  # build a new model from YAML
model = YOLO("yolo11l-cls.pt")  # load a pretrained model (recommended for training)
# model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model
# results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
results = model.train(data="datasets",model="yolo11l-cls.pt", epochs=300, batch=16, imgsz=640, device="0", project="output_dir", name="yolo11l_AdamW_300epoch", workers=128, optimizer="AdamW", amp=True, half=True, dnn=True)
# save final model
model.save("yolo11l-cls-300epoch.pt")
# valiadtion
# results = model.val(data="dataset.yaml", batch_size=1)
# test
# results = model.predict(data="dataset.yaml", batch_size=1)

# parser.add_argument('--data', type=str, default=ROOT + '/ultralytics/cfg/datasets/coco.yaml', help='dataset.yaml path')
# parser.add_argument('--config', type=str, default=ROOT + '/ultralytics/cfg/models/mamba-yolo/Mamba-YOLO-T.yaml', help='model path(s)')
# parser.add_argument('--batch_size', type=int, default=512, help='batch size')
# parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=640, help='inference size (pixels)')
# parser.add_argument('--task', default='train', help='train, val, test, speed or study')
# parser.add_argument('--device', default='0,1,2,3,4,5,6,7', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
# parser.add_argument('--workers', type=int, default=128, help='max dataloader workers (per RANK in DDP mode)')
# parser.add_argument('--epochs', type=int, default=300)
# parser.add_argument('--optimizer', default='SGD', help='SGD, Adam, AdamW')
# parser.add_argument('--amp', action='store_true', help='open amp')
# parser.add_argument('--project', default=ROOT + '/output_dir/mscoco', help='save to project/name')
# parser.add_argument('--name', default='mambayolo', help='save to project/name')
# parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
# parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
