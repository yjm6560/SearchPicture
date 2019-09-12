import ImageClassifier
import Logger

if __name__ == "__main__":
    IC = ImageClassifier.ImageClassfier('image')
    logger = Logger.Logger()

    logger.cur.execute("DROP TABLE IF EXISTS "+logger.db_name)
    logger.createTable()

    data_list = IC.imagesClassify()

    for data in data_list:
        print(data)
        logger.insertNonTextyPhoto(data[0], data[1], data[2])
    print("wow")
    tag_data = ["cat", "dog", "truck"]

    for tag in tag_data:
        print(logger.getPhotoByTag(tag))