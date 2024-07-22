import glob
import io
import os

from PIL import Image


def photo_resize_and_copy(image_file, output_file):
    image = Image.open(image_file)

    # Сохраняем фотографию
    output_stream = io.BytesIO()
    image.save(output_stream, format="WEBP")
    output_stream.seek(0)

    with open(output_file, "wb") as f:
        f.write(output_stream.read())


# Обход папок с фотографиями
root_dir = "static/"
for fileName in glob.iglob(root_dir + "**/*.png", recursive=True):
    images_saves_dir = os.path.dirname(fileName)
    fileName = os.path.basename(fileName)

    newFileName = fileName
    photo_resize_and_copy(images_saves_dir + "/" + fileName, images_saves_dir + "/" + newFileName)
    print(images_saves_dir)
    print(fileName)
