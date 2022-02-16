import cv2
import time


def img_trans(img, IMAGE, MASK, SIZE):
    global num
    num += 1

    time_start = time.time()

    out = cv2.resize(img, SIZE)

    out = out/255

    IMAGE = cv2.resize(IMAGE, SIZE)
    MASK = cv2.resize(MASK, SIZE)

    result = out * IMAGE + (1 - out) * MASK

    time_end = time.time()

    interval = time_end - time_start

    result = result.astype('uint8')

    cv2.imshow('Styled image', result)

    return result, interval


def save_video_style_trans(Video_In, Video_Out, Size, Image, Mask):

    cap = cv2.VideoCapture(Video_In)

    frames_num = cap.get(7)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数

    out = cv2.VideoWriter(Video_Out, fourcc, fps, Size, isColor=True)

    current_num = 0

    while True:

        ret, frame = cap.read()

        if ret is True:

            frame, interval = img_trans(frame, Image, Mask, Size)

            out.write(frame)

            current_num += 1

            process = current_num * 100 / frames_num

            spend_time = (frames_num-current_num) * interval

            print("process:{:.2f}%  预计还需时间:{:.2f}s" .format(process, spend_time))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image = cv2.imread('S2_card.jpg')  # 读取源图片
    mask = cv2.imread('US2_card.jpg')  # 读取蒙版图片
    video_in = 'badapple.mp4'          # 读入处理视频
    video_out = 'out.mp4'              # 输出视频命名
    size = (480, 360)                  # 确定输出视频像素
    num = 0                            # 全局计时用，不需改动
    save_video_style_trans(video_in, video_out, size, image, mask)