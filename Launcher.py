import ImageClassifier
import Logger
from FilePath import FilePathGetter
'''
Launcher
    실행 파일
1. db 파일 생성
2. image classify
3. test
'''
#TODO : 지금은 한 번 돌고 끝내는 상황임. 무한으로 돌게 고쳐야됨
if __name__ == "__main__":
    user_1 = "yjm6560"
    user_2 = "easy"
    user = user_2
    #db 파일 생성
    logger = Logger.Logger(user)
    logger.cur.execute("DROP TABLE IF EXISTS "+ FilePathGetter.getDBName())
    logger.createTable()

    #image classify

    IC = ImageClassifier.ImageClassifier(user)
    data_list = IC.imagesClassify()

    for data in data_list:
        print(data)
        logger.insertTextyPhoto(data[0], data[1], data[2], data[3])
    #test example
    tag_data = ["cat", "dog", "truck"]
    text_tag = ["second","first"]

    print("TAG SEARCH")
    for tag in tag_data:
        print(tag, " ", logger.getPhotoByTag(tag))

    print("TEXT SEARCH")
    for text in text_tag:
        print(text, " ", logger.getPhotoByText(text))

