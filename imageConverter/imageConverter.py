import sys, os, time
from PIL import Image
from novella.config.config import  my_config
from novella.filemanager.filemanager import my_filemanager
from novella.logger.logger import logger

# Image object
class ImageConverter:
    def __init__(self):
        self.new_width = my_config.get("image", "new_width")
        self.new_height = my_config.get("image", "new_height")
        self.fixed_length = 60

    def convert_image(self, imagename):
        ImageConverter.debug("Converting image {}".format(imagename))
        imgname = os.path.join( my_filemanager.image_dir, imagename)
        self.isImage = False

        try:
            self.im = Image.open(imgname)
            self.owidth, self.oheight = self.im.size
            self.info = self.im.info
            temp = imagename.split('.')[0] + '.bin'
            outputFile = os.path.join(my_filemanager.bin_dir, temp)
        except Exception as e:
            ImageConverter.debug(e)
            return False

        newWidth = int(self.owidth * self.fixedLength / self.oheight)
        newSize = newWidth, self.fixed_length

        self.im = self.im.convert('RGB')    # convert to rgb
        self.im = self.im.resize(newSize, Image.ANTIALIAS)     # resize to thumbnail
        self.im = self.im.rotate(90, expand=True)

        data = list(self.im.getdata())

        if os.path.isfile(outputFile):      # delete file if already exists
            os.remove(outputFile)

        with open(outputFile, 'wb') as myf:
            for pixel in data:          # iterate through all the pixels
                for col in pixel:       # iterate through all the colors 
                    tem = int(col/8)
                    myf.write( tem.to_bytes(1, byteorder='big') )

        ImageConverter.debug("IMAGE: Bin file generated ..")
        return True


    @staticmethod
    def debug(*args):
        logger.debug("ImageConverter", *args)


    @staticmethod
    def error(*args):
        logger.error("ImageConverter", *args)


# class object
my_imageConverter = ImageConverter()

