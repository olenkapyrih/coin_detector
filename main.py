import cv2


def resize_frames(images, scale=0.2):
    resized_images = []
    for image in images:
        if image.shape[0] >= 1500 and image.shape[1] >= 1000 or image.shape[1] >= 1500 and image.shape[0] >= 1000:
            w, h = int(image.shape[1] * scale), int(image.shape[0] * scale)
            resized_images.append(cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA))
        else:
            resized_images.append(image)
    return resized_images


def get_frames(file_path, number_of_frames=5):
    frames = []
    video = cv2.VideoCapture(file_path)
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)

    resized_frames = resize_frames(frames[::number_of_frames])
    video.release()
    return resized_frames


def detect_coins(image):
    all_circles = []
    blured = cv2.medianBlur(image, 5)
    gray_scaled = cv2.cvtColor(blured, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('result2.jpg', gray_scaled)
    print("Searching for coins...")
    circles = cv2.HoughCircles(
        gray_scaled, cv2.HOUGH_GRADIENT, dp=1, minDist=5,
        param1=70, param2=35, minRadius=0, maxRadius=0
    )

    if circles is not None:
        all_circles.extend(circles[0])
    count = len(all_circles)
    print(f'Coins detected: {count}')


path_to_video_file = input("Enter the path to the video: ")
frames = get_frames(path_to_video_file)
stitcher = cv2.Stitcher.create(cv2.STITCHER_SCANS)
status_1, stitched_image = stitcher.stitch(frames)
if status_1 == 0:
    cv2.imwrite('result.jpg', stitched_image)
    detect_coins(stitched_image)
else:
    print('Sorry. Something went wrong. Please try again.')
