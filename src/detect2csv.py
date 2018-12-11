import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    args = parser.parse_args()

    with open(args.infile) as f:
        lines = f.readlines()

    frame_count = 0
    ball_detected = False
    for line in lines:
        detection = line.split(':')[0]
        if detection == 'Objects':
            frame_count += 1
            if not ball_detected:
                print('{}\t0\t0\t0'.format(frame_count))
            ball_detected = False
        if detection == 'ball':
            ball_detected = True
            cleaned_line = line.replace(')\n', '')
            split_line = [i for i in cleaned_line.split(' ') if not i == '']
            prob = split_line[1].split('%')[0].strip()
            left_x = int(split_line[3])
            top_y = int(split_line[5])
            width = int(split_line[7])
            height = int(split_line[9])
            x = int(round(left_x + width / 2))
            y = int(round(top_y - height / 2))
            print('{}\t{}\t{}\t{}'.format(frame_count, prob, x, y))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("Program canceled by user!\n")
        sys.exit(0)
