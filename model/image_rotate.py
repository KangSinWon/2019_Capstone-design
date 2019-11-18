import os
from PIL import Image, ImageOps

def folder_list(file_path):

    folder = os.listdir(file_path)
    folder.sort()
    label_list=[]

    for data_folder in folder:
        print("Working on {} folder..".format(data_folder))
        data_folder_path = os.path.join(file_path,'{}'.format(data_folder))
        data_folder_list = os.listdir(data_folder_path)
        data_folder_list.sort()
        label_list.append(data_folder)
        print(folder)
        #build fix folder
        target_path = '/Users/gangsin-won/2019_Capstone-design/fix_image_set'
        print("{} to {} dataset...".format(target_path, data_folder))
        os.mkdir(target_path + "/train/" + data_folder )
        os.mkdir(target_path + "/valid/" + data_folder)
        os.mkdir(target_path + "/test/" + data_folder)

        #case is 3 train, vaild, test
        #image total 6000
        #train 5000 vaild 500 test 500

        count = 0
        for imagefile in data_folder_list:
            image = Image.open(data_folder_path+"/"+imagefile)
            image = image.convert('RGB')
            save_image = image.resize((255,255))
            save_image = save_image.rotate(180)

            '''
            if(count<6000):
                save_image.save(target_path + "/train/" + data_folder + "/" + imagefile, quality=100)
            elif (count >= 6000 & count < 6500):
                save_image.save(target_path + "/test/" + data_folder + "/" + imagefile, quality=100)
            elif (count >= 6500 & count < 7000):
                save_image.save(target_path + "/valid/" + data_folder + "/" + imagefile, quality=100)
            '''
            if (count < 6000):
                save_image.save(target_path + "/train/" + data_folder + "/" + imagefile, quality=100)
            elif (count >= 6000 and count < 6500):
                save_image.save(target_path + "/test/" + data_folder + "/" + imagefile, quality=100)
            elif (count >= 6500 and count < 6600):
                save_image.save(target_path + "/valid/" + data_folder + "/" + imagefile, quality=100)

            image.close()
            save_image.close()
            count = count+1
        print("{} done!".format(data_folder))



def main():

    print("Image rorate start...")
    folder_list("/Users/gangsin-won/2019_Capstone-design/image_set")


if __name__ == "__main__":
    main()