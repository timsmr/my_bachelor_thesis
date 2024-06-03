import threading

from services.video_processer import VideoProcesser
from services.video_loader import VideoLoader

video_loader = VideoLoader()
video_processer = VideoProcesser()

if __name__ == "__main__":
    thread1 = threading.Thread(target=video_loader.start_load_video)
    thread2 = threading.Thread(target=video_processer.start_model)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
