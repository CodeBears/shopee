import base64
import os
import uuid
from io import BytesIO

from PIL import Image, ImageFile

from utils.error_code import ErrorCode
from utils.errors import ValidationError

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageHandler:
    _PRODUCT_IMAGE_PATH = '/src/static/image/product/'

    @classmethod
    def upload_product_images(cls, product_id, images):
        images_name = list()
        try:
            for image in images:
                decode_data = base64.b64decode(image.split(';base64,')[1])
                buff = BytesIO(decode_data)
                image_ = Image.open(buff)
                uid = uuid.uuid4().time
                image_name = f'{product_id}_{uid}'
                filepath = f'{cls._PRODUCT_IMAGE_PATH}{image_name}.jpg'
                image_ = image_.convert('RGB')
                image_.save(filepath)
                images_name.append(image_name)
        except Exception as e:
            raise ValidationError(error_code=ErrorCode.UPLOAD_IMAGE_ERROR,
                                  message='upload image error')
        return images_name

    @classmethod
    def download_image(cls, response, product_id):
        os.makedirs(cls._PRODUCT_IMAGE_PATH, exist_ok=True)
        filepath = f'{cls._PRODUCT_IMAGE_PATH}{product_id}_1.jpg'
        with open(filepath, 'wb') as f:
            f.write(response.content)

    @classmethod
    def get_images(cls, image_names):
        results = list()
        for name in image_names:
            filepath = f'{cls._PRODUCT_IMAGE_PATH}{name}.jpg'
            with open(filepath, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                results.append(encoded_string)
        return results
