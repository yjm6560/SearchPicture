
'''
filePathGetter
    파일 경로 리턴해주는 static 클래스
    파일
        1. 네이버상품트리 파일
        2. 이미지넷 계층트리 파일
        3. 이미지가 있는 디렉토리
        4. 트레이닝 이미지가 있는 디렉토리
        5. 데이터베이스 파일
'''
class FilePathGetter:

    @staticmethod
    def getNaverGoodsTreeFilePath():
        return "NaverGoodsTree.txt"

    @staticmethod
    def getImageNetTreeFilePath():
        return "ImageNetTree.txt"

    @staticmethod
    def getImageDirPath():
        return "image"

    @staticmethod
    def getTrainingImageDirPath():
        return "training_img"

    @staticmethod
    def getDBName():
        return "photo_data"