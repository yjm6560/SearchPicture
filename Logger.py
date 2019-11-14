import sqlite3
import threading

from FilePath import FilePathGetter
'''
Logger
    db 접근용 클래스
    기능
        1. 테이블 생성
        2. 텍스트 포함 이미지 삽입
        3. 텍스트 미포함 이미지 삽입
        4. 태그로 이미지 검색
        5. 텍스트로 이미지 검색
'''
#TODO : 텍스트 포함, 미포함으로 나눌지 말지 정해야 함.(현재는 나눠진 상태)
class Logger:

    def __init__(self, user_id):
        #연결
        self.db_name = FilePathGetter.getDBName() + "_" + user_id
        self.conn = sqlite3.connect(self.db_name + ".db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.lock = threading.Lock()

    def createTable(self):
        #db 파일 생성
        create_query = "CREATE TABLE IF NOT EXISTS " + self.db_name + "(photo_id integer, path TEXT PRIMARY KEY , tag_list TEXT, text_img TEXT)"
        self.cur.execute(create_query)
        self.conn.commit()

    def getPhotoByTag(self, tag_keywords):
        #태그로 이미지 검색
        select_query = "SELECT photo_id, path, tag_list FROM " + self.db_name + " WHERE"
        for keyword in tag_keywords:
            select_query += " tag_list LIKE \"%/" + keyword + "/%\"" + " AND "
        self.cur.execute(select_query[0:-5])
        return self.cur.fetchall()

    def getPhotoByText(self, text_keywords):
        #텍스트로 이미지 검색
        select_query = "SELECT photo_id, path, tag_list, text_img FROM " + self.db_name + " WHERE"
        for keyword in text_keywords:
            select_query += " text_img LIKE \"%" + keyword + "%\"" + " AND "
        self.cur.execute(select_query[0:-5])
        return self.cur.fetchall()

    def insertNonTextyPhoto(self, photo_id, photo_path, tag_list):
        #텍스트 미포함 이미지 삽입
        self.lock.acquire()
        insert_query = "INSERT INTO " + self.db_name + "(photo_id, path, tag_list) VALUES( ? , ? , ? )"
        try:
            self.cur.execute(insert_query, (photo_id, photo_path, "/" + "/".join(tag_list) + "/"))
        except sqlite3.IntegrityError as e:
            select_query = f"SELECT tag_list FROM {self.db_name} WHERE path=\"{photo_path}\""
            self.cur.execute(select_query)
            obj_list = self.cur.fetchall()
            if obj_list and obj_list[0][0] != "":
                print("OBJ LIST : ",obj_list)
                tag_list = tag_list + obj_list[0][0].split("/")
            update_query = f"UPDATE {self.db_name} SET tag_list = ? WHERE path = ?"
            self.cur.execute(update_query, ("/" + "/".join(tag_list) + "/", photo_path))
        self.lock.release()
        self.conn.commit()

    def insertTextyPhoto(self, photo_id, photo_path, text):
        #텍스트 포함 이미지 삽입
        #TODO: 이어진 글자 사이에 띄어쓰기가 있다고 인식해서 일단 띄어쓰기나 엔터 없앰 추후 어떻게 할지 논의
        text = text.replace(" ", "", len(text)).replace("\n", "", len(text))
        insert_query = "INSERT INTO " + self.db_name + " VALUES( ? , ? , ? , ?)"
        try:
            self.cur.execute(insert_query, (photo_id, photo_path, "" , text))

        except sqlite3.IntegrityError as e:
            update_query = f"UPDATE {self.db_name} SET text_img = ? WHERE path = ?"
            self.cur.execute(update_query, (text, photo_path))
        self.conn.commit()

    def getAllPath(self):
        getPath_query = f"SELECT path FROM {self.db_name}"
        self.cur.execute(getPath_query)
        return self.cur.fetchall()

if __name__ == "__main__":
    logger = Logger("yjm6560")
    logger.cur.execute("DROP TABLE IF EXISTS " + logger.db_name)
    logger.createTable()
    logger.insertNonTextyPhoto(1, "a", ["note", "book", "pencil"])
    logger.insertNonTextyPhoto(2, "b", ["news", "pen", "monitor"])
    logger.insertNonTextyPhoto(3, "c", ["news", "phone", "monitor"])
    logger.insertNonTextyPhoto(4, "d", ["mouse", "fly", "monitor"])

    logger.insertTextyPhoto(5, "e", [], "Latte is horse")
    logger.insertTextyPhoto(6, "f", [], "I was a car")

    print(logger.getPhotoByText(["horse"]))
    print(logger.getPhotoByText(["car", "was"]))
    print(logger.getPhotoByTag(["monitor", "pen"]))
