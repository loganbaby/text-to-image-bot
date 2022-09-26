import requests

class ImageDefiner:
    def __init__(self):
        self.__api_url = 'https://api.ocr.space/parse/image'
        self.__api_key = 'K87669101088957'
        self.__language = 'eng'       # russian - rus
        self.__url_to_image = ''      # url to image (.png in the end)
        self.__path_to_image = ''     # path in filesystem
        self.__ocr_engine = '1'       # OCR engine version

    def get_word_by_url(self):
        request = requests.post(self.__api_url,
                                data={'url': self.__url_to_image,
                                'isOverlayRequired': False,
                                'apikey': self.__api_key,
                                "OCREngine": self.__ocr_engine,
                                'language': self.__language})

        return False if request.json()["IsErroredOnProcessing"] == True else request.json()["ParsedResults"][0]["ParsedText"]

    def get_word_by_path(self):
        payload = {'isOverlayRequired': False,
                   'apikey': self.__api_key,
                   'language': self.__language,
                   }
        with open(self.__path_to_image, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={self.__path_to_image: f},
                              data=payload,
                              )
        return r.json()["ParsedResults"][0]["ParsedText"]

    @property
    def url_to_image(self):
        return self.__url_to_image

    @url_to_image.setter
    def url_to_image(self, url):
        self.__url_to_image = url

    @property
    def path_to_image(self):
        return self.__path_to_image

    @path_to_image.setter
    def path_to_image(self, new_path):
        self.__path_to_image = new_path

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, new_lang):
        self.__language = new_lang
