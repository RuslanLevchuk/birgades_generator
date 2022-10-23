import datetime
from sqlite_request import sqlite_brigde_request

brigades = {'brigade1': {}, 'brigade2': {}, 'brigade3': {}}



def brigade_repr(shift, shift_task):

    shift_brigade_respond = [shift]

    for work_center, assortment in shift_task.items():
        #якщо у завданні на одну лінію лише один асортимент
        if len(assortment) == 1:
            shift_brigade_respond += sqlite_brigde_request(list(assortment.keys())[0])

        #якщо у завданні два асортимента, то формується одна бригада, якщо вони однакові
        #або дві бригади якщо у них відмінність у довжині
        if len(assortment) == 2:
            br_1 = sqlite_brigde_request(list(assortment.keys())[0])
            br_2 = sqlite_brigde_request(list(assortment.keys())[1])
            if len(br_1) == len(br_2):
                shift_brigade_respond += br_1
            else:
                shift_brigade_respond += br_1 + br_2

        # якщо у завданні три асортимента, то формується одна бригада, якщо вони однакові
        # або три бригади, якщо у них відмінність у довжині
        if len(assortment) == 3:
            br_1 = sqlite_brigde_request(list(assortment.keys())[0])
            br_2 = sqlite_brigde_request(list(assortment.keys())[1])
            br_3 = sqlite_brigde_request(list(assortment.keys())[2])
            if len(br_1) == len(br_2) and len(br_2) == len(br_3):
                shift_brigade_respond += br_1
            else:
                shift_brigade_respond += br_1 + br_2 + br_3

        if len(assortment) > 3:
            shift_brigade_respond += [work_center] + ['У завданні більше трьох найменувань продукції, додайте бригаду вручну']

    return shift_brigade_respond







def parse(brig_dict):
    global brigades

    for date, day_task in brig_dict.items():
        weekday = datetime.datetime.fromisoformat(str(date)).weekday()

        #task for brigade 1. monday is sanitary shift
        if '1' in day_task:
            brigades['brigade1'][date] = brigade_repr('1', day_task['1'])


        #task for brigade 2. monday - saturday is 2nd shif, sunday is 3rd shift
        if '2' in day_task and weekday != 6:
            brigades['brigade2'][date] = brigade_repr('2', day_task['2'])
        if '3' in day_task and weekday == 6:
            brigades['brigade2'][date] = brigade_repr('3', day_task['3'])

        #task for brigade 3. monday - saturday is 3rd shif, sunday is 2nd shift
        if '3' in day_task and weekday != 6:
            brigades['brigade3'][date] = brigade_repr('3', day_task['3'])
        if '2' in day_task and weekday == 6:
            brigades['brigade3'][date] = brigade_repr('2', day_task['2'])

    return brigades





if __name__ == '__main__':
    #temporary
    import parser
    dic = parser.week_task_dict()
    #temporary



    bb = parse(dic)

    for key, value in bb.items():
        print(key)
        print(value)
        for date, br in value.items():
            print('-----  ', date)
            for item in br:
                print('            ', item)


