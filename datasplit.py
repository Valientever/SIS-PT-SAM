import os
import shutil
import glob
from ipdb import set_trace

# Define dataset paths
original_dataset_path = "/home/santhi/Documents/SIS-PT-SAM/dataset"  # Change this to your dataset root
main_dataset_path = "/home/santhi/Documents/SIS-PT-SAM/main_dataset"  # Destination dataset root

if not os.path.exists(main_dataset_path):
    os.makedirs(main_dataset_path)
# Create new directories
subsets = ["train", "val", "test"]
for subset in subsets:
    os.makedirs(os.path.join(main_dataset_path, subset, "imgs"), exist_ok=True)
    os.makedirs(os.path.join(main_dataset_path, subset, "gts"), exist_ok=True)

# Get sorted video folder paths
video_folders = sorted(glob.glob(os.path.join(original_dataset_path, "video*")))  # List all video folders
# set_trace()

img_files = []
gt_files = []

# Iterate through video folders and collect image and mask paths
for video_folder in video_folders: # video_foldes == 17  # 17 videos
    # set_trace()
    frame_folders = sorted(glob.glob(os.path.join(video_folder, "video*_*")))  # List all frame subfolders # 16 frames in one video01

    for frame_folder in frame_folders:
        img_path = None
        gt_path = None

        # Get sorted list of files inside each frame folder
        frame_files = sorted(os.listdir(frame_folder))  # Ensuring files are in sequence
        #frame_folder = '/home/santhi/Documents/SIS-PT-SAM/dataset/video01/video01_00080'
        #frame_files = ['video01_00080_endo.png', 'video01_00080_endo_mask.png'] # 320 in total for video01_00080
        for frame in frame_files:
            # set_trace()
            frame_path = os.path.join(frame_folder, frame)

            if frame.endswith("_endo.png"):
                img_path = frame_path
            elif frame.endswith("_endo_mask.png"):
                gt_path = frame_path

        # Debugging: Check found paths
            if img_path and gt_path:
                # print(f"Found Image: {img_path}, Mask: {gt_path}")
                img_files.append(img_path)
                gt_files.append(gt_path)

# Ensure images and masks are matched correctly
assert len(img_files) == len(gt_files), f"Mismatch between images ({len(img_files)}) and ground truth masks ({len(gt_files)})."

print(f"Total frames: {len(img_files)}, {len(gt_files)}")
# Define split sizes
total_frames = len(img_files)
test_size = 3597  # 8 consecutive clips (already known)
train_val_size = total_frames - test_size
train_size = int(train_val_size * 0.8)
val_size = train_val_size - train_size

# Assign files
test_imgs, test_gts = img_files[:test_size], gt_files[:test_size]
print(f"test size: {len(test_imgs)}, {len(test_gts)}")
train_imgs, train_gts = img_files[test_size:test_size+train_size], gt_files[test_size:test_size+train_size]
print(f"train size: {len(train_imgs)}, {len(train_gts)}")
val_imgs, val_gts = img_files[test_size+train_size:], gt_files[test_size+train_size:]
print(f"val size: {len(val_imgs)}, {len(val_gts)}")

# Function to move files
def move_files(file_list, dest_folder):
    for file in file_list:
        shutil.copy(file, os.path.join(dest_folder, os.path.basename(file)))  # Use copy instead of move

# Move files to respective folders
move_files(test_imgs, os.path.join(main_dataset_path, "test", "imgs"))
move_files(test_gts, os.path.join(main_dataset_path, "test", "gts"))

move_files(train_imgs, os.path.join(main_dataset_path, "train", "imgs"))
move_files(train_gts, os.path.join(main_dataset_path, "train", "gts"))

move_files(val_imgs, os.path.join(main_dataset_path, "val", "imgs"))
move_files(val_gts, os.path.join(main_dataset_path, "val", "gts"))

print("Dataset restructuring completed successfully!")
