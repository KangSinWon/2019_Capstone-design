import struct
from struct import unpack
import matplotlib.pyplot as plt
import os
import errno
import multiprocessing
from subprocess import call


class QuickDrawData:
    bin_folder_path = ""
    bin_list = []
    save_folder = "/home/mll601-2/2019_Capstone/2019_Capstone-design/image_set"
    remove_name = "full%2Fbinary%2F"

    def init(self, bin_folder_path, bin_list):
        self.bin_folder_path = bin_folder_path
        self.bin_list = bin_list

    def unpack_drawing(self, file_handle):
        key_id, = unpack('Q', file_handle.read(8))
        countrycode, = unpack('2s', file_handle.read(2))
        recognized, = unpack('b', file_handle.read(1))
        timestamp, = unpack('I', file_handle.read(4))
        n_strokes, = unpack('H', file_handle.read(2))
        image = []
        for i in range(n_strokes):
            n_points, = unpack('H', file_handle.read(2))
            fmt = str(n_points) + 'B'
            x = unpack(fmt, file_handle.read(n_points))
            y = unpack(fmt, file_handle.read(n_points))
            image.append((x, y))

        return {
            'key_id': key_id,
            'countrycode': countrycode,
            'recognized': recognized,
            'timestamp': timestamp,
            'image': image
        }

    def unpack_drawings(self, filename):
        filename = bin_folder_path + "/" + filename
        with open(filename, 'rb') as f:
            while True:
                try:
                    yield self.unpack_drawing(f)
                except struct.error:
                    break

    def data_preprocessing(self, filename, path):
        _dpi = 100
        count = 0
        for drawing in self.unpack_drawings(filename):
            image_array = drawing['image']
            plt.clf()
            plt.figure(figsize=(331 / _dpi, 333 / _dpi), dpi=_dpi)
            for x in range(len(image_array)):
                x1, y1 = image_array[x][0], image_array[x][1]
                plt.plot(x1, y1, color='k')

            save_path = path + str(count) + ".png"
            plt.axis('off')
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=_dpi)
            plt.close()
            print("save png:", save_path)
            count += 1
            if count == 1:
                break

    def load_binfile(self, files):
        for file_name in files:
            if file_name[len(file_name)-4:] == ".bin":
                '''
                os.rename(self.bin_folder_path + "/" + file_name,
                          self.bin_folder_path + "/" + file_name[len(self.remove_name):])
                file_name = file_name[len(self.remove_name):]
                print(file_name)
                '''
                data_folder_name = file_name[0:len(file_name) - 4]
                data_folder_path = self.save_folder + "/" + data_folder_name + "/"
                try:
                    os.makedirs(data_folder_path)
                    print('mkdir -p', data_folder_path)
                    self.data_preprocessing(file_name, data_folder_path)
                except OSError as exc:
                    if exc.errno == errno.EEXIST and os.path.isdir(data_folder_path + "/" + data_folder_name + "/"):
                        print('already exist folder')
                        self.data_preprocessing(file_name, data_folder_path)
                        pass
                    else:
                        raise

    def get_process_schedule(self):
        process_count = 4
        process_list = []
        for i in range(process_count):
            process_list.append([])

        index = 0
        for i in range(len(self.bin_list)):
            process_list[index].append(self.bin_list[i])
            index += 1
            if index == 4:
                index = 0
        return process_list

    def run(self):
        for files in self.get_process_schedule():
            print(files)
            p = multiprocessing.Process(target=self.load_binfile, args=(files,))
            process.append(p)
            p.start()

        for p in process:
            p.join()


if __name__ == "__main__":
    process = []

    bin_folder_path = input("폴더명을 입력해주세요: ")
    bin_list = os.listdir(bin_folder_path)

    quickdata = QuickDrawData()
    quickdata.init(bin_folder_path, bin_list)
    quickdata.run()


    call(["python3", "/home/mll/Capstone/2019_Capstone-design/model/image_rotate.py"])



