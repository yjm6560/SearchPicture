import ImageClassifier
import Logger
from FilePath import FilePathGetter
import threading
'''
Launcher
    실행 파일
1. db 파일 생성
2. image classify
3. test
'''
#TODO : 지금은 한 번 돌고 끝내는 상황임. 무한으로 돌게 고쳐야됨
#TODO : 계층트리 적용

DEBUG = False

if __name__ == "__main__":

    user_1 = "yjm6560"
    user_2 = "easy"
    user = user_2
    #db 파일 생성
    logger = Logger.Logger(user)
    logger.cur.execute("DROP TABLE IF EXISTS " + FilePathGetter.getDBName())
    logger.createTable()

    #image classify

    IC = ImageClassifier.ImageClassifier(user)
    threads = []
#    threads.append(threading.Thread(target=IC.classifyObjImagesByBatch, args=(logger, 8)))
    threads.append(threading.Thread(target=IC.classifyObjImages_sub, args=(logger, 8)))
    threads.append(threading.Thread(target=IC.classifyObjImagesByBatch, args=(logger, 8)))
    threads.append(threading.Thread(target=IC.analyzeTextImages, args=(logger, 8)))

    if DEBUG:
        print("THREAD START")

    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()

    if DEBUG:
        print("THREAD END")

    #classify images and insert into database
    print("="*30)
    print("INSERTING IMAGES")
    print("="*30)
    #test example
    tag_data = ["animal", "truck","person","cell phone","pizza"]
    text_tag = [["second","first"],["이거", "오류"],["아프리카돼지열병"]]

    #search by tag
    print("="*30)
    print("TAG SEARCH")
    print("="*30)
    for tag in tag_data:
        print("SEARCH TAG : ", tag)
        ret = logger.getPhotoByTag([tag])
        for dat in ret:
            print("\t",dat[1])
    #search by text
    print("=" * 30)
    print("TEXT SEARCH")
    print("=" * 30)
    for text in text_tag:
        print("SEARCH TEXT : ", text)
        ret = logger.getPhotoByText(text)
        for dat in ret:
            print("\t", dat[1])


