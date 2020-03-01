import os, sys
import numpy as np
import torch

from fer_pytorch.utils.get_landmark_from_dataset import affine_img_with_five_landmark


if __name == "__main__":
    weights = ''
    images='reid_data/samples',  # input folder
   output='output',  # output folder


    # Initialize
    device = 'cpu' # cpu or gpu
    torch.backends.cudnn.benchmark = False  # set False for reproducible results
    if os.path.exists(output):
        shutil.rmtree(output)  # remove previous result
    os.makedirs(output)       

    affiner = affine_img_with_five_landmark()
    
    
    

    # Load weights
    if weights.endswith('.pth'):  # pytorch format
        model.load_state_dict(torch.load(weights, map_location=device)['model'])
    else:  # other format
       raise NotImplementedError

    # Eval mode
    model.to(device).eval()

    # Half precision
    opt.half = opt.half and device.type != 'cpu'  # half precision only supported on CUDA
    if opt.half:
        model.half()


    # Set Dataloader
    vid_path, vid_writer = None, None
    if opt.webcam:
        save_images = False
        dataloader = LoadWebcam(img_size=img_size, half=opt.half)
    else:
        dataloader = LoadImages(images, img_size=img_size, half=opt.half)

    classes = ['happy', 'anger', 'sad', 'neutral', 'disgust', 'surprised'] # class list
    
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))] # random color for each class

    # Run inference
    t0 = time.time()
    for i, (path, img, im0, vid_cap) in enumerate(dataloader):
        t = time.time()
        save_path = str(Path(output) / Path(path).name) 
        # Get detections and align
        img=affiner.face_affiner(img)   # 不好,最好分离
        
        img = torch.from_numpy(img).unsqueeze(0).to(device) # torch.Size([1, 3, 416, 320])
        pred_loggits = model(img)  
        pred_loggits = pred_loggits.softmax(dim=-1)

        cls = np.argmax(pred_loggits)
        print(classes[int(cls)])

        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)])
