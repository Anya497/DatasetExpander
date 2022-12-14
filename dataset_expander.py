from PIL import Image
import os
import random


def get_intervals_info(directory):
    interval_pict_num = [0]*4
    interval_len_num = [0]*4
    len_variation = []
    for picture_name in os.listdir(directory):
        in_image = Image.open(directory + picture_name)
        seq_size = in_image.size[0]
        if seq_size <= 14:
            if seq_size not in len_variation:
                len_variation.append(seq_size)
                interval_len_num[0] += 1
            interval_pict_num[0] += 1
        elif seq_size <= 30:
            if seq_size not in len_variation:
                len_variation.append(seq_size)
                interval_len_num[1] += 1
            interval_pict_num[1] += 1
        elif seq_size <= 62:
            if seq_size not in len_variation:
                len_variation.append(seq_size)
                interval_len_num[2] += 1
            interval_pict_num[2] += 1
        else:
            if seq_size not in len_variation:
                len_variation.append(seq_size)
                interval_len_num[3] += 1
            interval_pict_num[3] += 1
    return interval_pict_num, interval_len_num


def generate_pictures(pictures_names, required_num, interval, in_directory):
    generated_pic_num = 0
    fields_size = (16 * (2 ** interval), 16 * (2 ** interval))
    for picture in pictures_names:

        in_image = Image.open(in_directory + picture)
        out_image = Image.open(in_directory.replace('in', 'out') + picture)
        for k in range(required_num // len(pictures_names)):

            generated_pic_num += 1
            in_fields = Image.new(mode="RGB", size=fields_size)
            out_fields = Image.new(mode="RGB", size=fields_size)

            range_size = 16 * (2 ** interval) - in_image.size[0] - 1
            random_i = random.randint(0, range_size)
            random_j = random.randint(0, range_size)
            all_variants = []
            for i in range(range_size + 1):
                for j in range(range_size + 1):
                    all_variants.append((i, j))
            while os.path.isfile("expanded_dataset" + "in/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png"):
                all_variants.remove((random_i, random_j))
                random_i, random_j = random.choice(all_variants)
            in_fields.paste(in_image, (random_i, random_j))
            out_fields.paste(out_image, (random_i, random_j))
            in_fields.save("expanded_dataset" + "in/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png")
            out_fields.save("expanded_dataset" + "out/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png")

    for picture in pictures_names:
        in_image = Image.open(in_directory + picture)
        out_image = Image.open(in_directory.replace('in', 'out') + picture)
        if generated_pic_num != required_num:
            generated_pic_num += 1

            in_fields = Image.new(mode="RGB", size=fields_size)
            out_fields = Image.new(mode="RGB", size=fields_size)

            range_size = 16 * (2 ** interval) - in_image.size[0] - 1
            random_i = random.randint(0, range_size)
            random_j = random.randint(0, range_size)
            all_variants = []
            for i in range(range_size + 1):
                for j in range(range_size + 1):
                    all_variants.append((i, j))
            while os.path.isfile(
                    "expanded_dataset" + "in/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png"):
                all_variants.remove((random_i, random_j))
                random_i, random_j = random.choice(all_variants)
            in_fields.paste(in_image, (random_i, random_j))
            out_fields.paste(out_image, (random_i, random_j))
            in_fields.save("expanded_dataset" + "in/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png")
            out_fields.save("expanded_dataset" + "out/" + picture[0:4] + "_" + str(random_i) + '_' + str(random_j) + ".png")


def get_required_num(pictures_info, len_num, required_pictures_num):
    required_num = {}
    for seq_len in pictures_info:
        required_num[seq_len] = required_pictures_num // len_num
    for seq_len in required_num:
        if sum(required_num.values()) != required_pictures_num:
            required_num[seq_len] += 1
    return required_num


def get_pictures_info(in_directory):
    all_pictures_info = {}
    pictures_names = os.listdir(in_directory)
    pictures_info = [{}, {}, {}, {}]
    for picture_name in pictures_names:
        in_image = Image.open(in_directory + picture_name)
        im_size = in_image.size[0]
        all_pictures_info[im_size] = {}
        all_pictures_info[im_size]['pictures_names'] = []
        all_pictures_info[im_size]['interval'] = 0

    all_pictures_info_sorted = {k: all_pictures_info[k] for k in sorted(all_pictures_info)}
    for picture_name in pictures_names:
        in_image = Image.open(in_directory + picture_name)
        all_pictures_info_sorted[in_image.size[0]]['pictures_names'].append(picture_name)
    for seq_len in all_pictures_info_sorted:
        if seq_len <= 14:
            pictures_info[0][seq_len] = all_pictures_info_sorted[seq_len]
        elif seq_len <= 30:
            pictures_info[1][seq_len] = all_pictures_info_sorted[seq_len]
        elif seq_len <= 62:
            pictures_info[2][seq_len] = all_pictures_info_sorted[seq_len]
        else:
            pictures_info[3][seq_len] = all_pictures_info_sorted[seq_len]
    return pictures_info


def expand_dataset(required_pictures_num, directory):
    pictures_info = get_pictures_info(directory)
    intervals_info = get_intervals_info(directory)
    for interval in range(4):
        required_num = get_required_num(pictures_info[interval], intervals_info[1][interval],
                                        required_pictures_num[interval])
        for seq_len in pictures_info[interval]:

            generate_pictures(pictures_info[interval][seq_len]['pictures_names'], required_num[seq_len], interval, directory)












