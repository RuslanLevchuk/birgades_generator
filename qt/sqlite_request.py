import sqlite3



def sqlite_brigde_request(assortment_name):
        brigade_request = f"""SELECT 
                            (
                            SELECT short_name FROM work_centres 
                            INNER JOIN assortment on assortment.work_center = work_centres.work_center_id
                            WHERE assortment.assortment_name like '%{assortment_name}%' LIMIT 1
                            ) 
                            as work_center,
                            composition
                                    
                            FROM brigades 
                            INNER JOIN assortment on assortment.brigade_id = brigades.id
                            WHERE assortment.assortment_name like '%{assortment_name}%' LIMIT 1;
                        """

        staff_db = sqlite3.connect("staff.db")
        cursor = staff_db.cursor()
        result = cursor.execute(brigade_request).fetchone()
        staff_db.close()


        if not result:
            result = f"У базі даних не існує найменування асортименту \"{assortment_name}\". Додайте асортимент у базу даних."
            return [result]
        else:
            return [result[0]]+result[1].split(', ')




def work_centres_list():
    work_centres_request = 'SELECT short_name, work_center_id FROM work_centres;'
    wc = sqlite3.connect("staff.db")
    cursor = wc.cursor()
    wc_list = cursor.execute(work_centres_request).fetchall()
    wc.close()
    return wc_list


def brigades_request_qt():
    all_brigades_request = "SELECT * from brigades;"
    all_bridades_db = sqlite3.connect("staff.db")
    all_brigades_cursor = all_bridades_db.cursor()
    all_brigades_respond = all_brigades_cursor.execute(all_brigades_request).fetchall()
    all_bridades_db.close()
    return all_brigades_respond


def sqlite_is_assortment_exist(name):
    assortments_request = "SELECT assortment_name from assortment;"
    assortments_db = sqlite3.connect("staff.db")
    assortments_cursor = assortments_db.cursor()
    assortments_respond = assortments_cursor.execute(assortments_request).fetchall()
    assortments_db.close()

    if name in [i[0] for i in assortments_respond]:
        return 'Такий асортимент у базі даних уже існує!'
    elif name == '':
        return 'Введіть назву асортименту'
    else:
        return ''


def sqlite_insert_assortment(assortment_name, work_center_id, brigade_id):
    assortments_request = f"""INSERT INTO assortment ( assortment_name, work_center, brigade_id)
                            VALUES ('{assortment_name}', {int(work_center_id)}, {int(brigade_id)});"""
    assortments_db = sqlite3.connect("staff.db")
    assortments_cursor = assortments_db.cursor()
    assortments_cursor.execute(assortments_request)
    assortments_db.commit()
    assortments_db.close()







if __name__ == '__main__':

    #print(sqlite_brigde_request('ЦУКЕРКИ Ko-Ko Choco White ВКФ 1кг /5пак'))
    #assortment_name = 'ЦУКЕРКИ Ko-Ko Choco White ВКФ 1кг /5пак'
    #print(work_centres_list())

    print([i for i in work_centres_list()])
    print(brigades_request_qt())
    print(sqlite_is_assortment_exist('ШОКОЛАД Lacmi молочний з цілими лісовими горіхами і шоколао-карамельною начинкою ВКФ 295г /12шт'))




