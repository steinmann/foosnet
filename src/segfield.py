import numpy as np
import cv2
import sys
import csv
import argparse


def create_image(height, width):
    img = np.zeros((height, width, 3), np.uint8)
    img[:] = (255, 255, 255)
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    # draw detections
    img = create_image(1080, 1920)
    blue = [123, 95, 12]
    with open(args.infile) as f:
        reader = csv.reader(f, delimiter='\t')

        detection_set = set()
        for line in reader:
            line = [int(i) for i in line]
            prob = line[1]
            x = line[2]
            y = line[3]
            if prob > 90:
                img[y, x] = blue
    cv2.imwrite("detections.png", img)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("Program canceled by user!\n")
        sys.exit(0)
