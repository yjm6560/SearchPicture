import sqlite3

class Logger:

    def __init__(self):
        self.db_name = "photo_data"
        self.conn = sqlite3.connect(self.db_name + ".db")
        self.cur = self.conn.cursor()

    def createTable(self):
        create_query = "CREATE TABLE IF NOT EXISTS " + self.db_name + "(photo_id integer PRIMARY KEY, path TEXT, tag_list TEXT, text_img TEXT)"
        self.cur.execute(create_query)

    def getPhotoByTag(self, tag_keywords):
        select_query = "SELECT photo_id, path, tag_list FROM " + self.db_name + " WHERE"
        for keyword in tag_keywords:
            select_query += " tag_list LIKE \"%" + keyword + "%\"" + " AND "
        self.cur.execute(select_query[0:-5])
        return self.cur.fetchall()

    def getPhotoByText(self, text_keywords):
        select_query = "SELECT photo_id, path, tag_list, text_img FROM " + self.db_name + " WHERE tag_list LIKE \"text\" AND"
        for keyword in text_keywords:
            select_query += " text_img LIKE \"%" + keyword + "%\"" + " AND "
        self.cur.execute(select_query[0:-5])
        return self.cur.fetchall()

    def insertNonTextyPhoto(self, photo_id, photo_path, tag_list):
        insert_query = "INSERT INTO " + self.db_name + "(photo_id, path, tag_list) VALUES( ? , ? , ? )"
        self.cur.execute(insert_query, (photo_id, photo_path, ", ".join(tag_list)))

    def insertTextyPhoto(self, photo_id, photo_path, tag_list, text):
        insert_query = "INSERT INTO " + self.db_name + " VALUES( ? , ? , ? , ?)"
        self.cur.execute(insert_query, (photo_id, photo_path, ", ".join(tag_list), text))


if __name__ == "__main__":
    logger = Logger()
    logger.cur.execute("DROP TABLE IF EXISTS " + logger.db_name)
    logger.createTable()
    logger.insertNonTextyPhoto(1, "a", ["note", "book", "pencil"])
    logger.insertNonTextyPhoto(2, "b", ["news", "pen", "moniter"])
    logger.insertNonTextyPhoto(3, "c", ["news", "phone", "moniter"])
    logger.insertNonTextyPhoto(4, "d", ["mouse", "fly", "moniter"])

    logger.insertTextyPhoto(5, "e", ["text"], "Latte is horse")
    logger.insertTextyPhoto(6, "f", ["text"], "I was a car")

    print(logger.getPhotoByText("horse"))
    print(logger.getPhotoByText(["car", "was"]))
    print(logger.getPhotoByTag(["moniter", "pen"]))
