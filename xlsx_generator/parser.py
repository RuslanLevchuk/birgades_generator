import pandas as pd



def week_task_dict():
    file = pd.read_excel("Ежедневный план выпуска продукции _ Варіант_ План _ Директивна дата з 25.10.2021 по 31.10_Z55AI5A04.xlsx",  usecols="A:Z", skiprows=2)

    excel_full_table = file.to_dict()


    cropped_task_table = {}


    cropped_task_table['Дата директивна'] = excel_full_table['Дата \nдирективна']
    cropped_task_table['Зміна'] = excel_full_table['Зміна']
    cropped_task_table['Робочий центр'] = excel_full_table['Робочий \nцентр']
    cropped_task_table['Найменування'] = excel_full_table['Найменування']
    cropped_task_table['План (кг)'] = excel_full_table['План (кг)']
    cropped_task_table['Коментар'] = excel_full_table['Коментар']
    """
    for name in cropped_task_table:
        print(name, end='')
        print('                    ', end='')
    print()
    print(cropped_task_table)
    
    for number, value in enumerate(cropped_task_table['Дата директивна'].keys()):
        for name in cropped_task_table.keys():
            if number == 0:
                pass
            else:
                print(cropped_task_table[name][number], end='         ')
    
        print()
        
    """

    modified_task_table = {}

    for num, value in enumerate(cropped_task_table['Дата директивна'].values()):
        if num == 0:
            pass
        else:
            temporary_date = cropped_task_table['Дата директивна'][num]
            temporary_shift = str(int(cropped_task_table['Зміна'][num]))
            temporary_work_center = cropped_task_table['Робочий центр'][num]
            temporary_product_name = cropped_task_table['Найменування'][num]
            temporary_plan_tonnage = cropped_task_table['План (кг)'][num]
            temporary_comment = cropped_task_table['Коментар'][num]

            if not temporary_date in modified_task_table.keys():
                modified_task_table[temporary_date] = {}
            if not temporary_shift in modified_task_table[temporary_date].keys():
                modified_task_table[temporary_date][temporary_shift] = {}
            if not temporary_work_center in modified_task_table[temporary_date][temporary_shift].keys():
                modified_task_table[temporary_date][temporary_shift][temporary_work_center] = {}
            if not temporary_product_name in modified_task_table[temporary_date][temporary_shift][temporary_work_center].keys():
                modified_task_table[temporary_date][temporary_shift][temporary_work_center][temporary_product_name] = [temporary_plan_tonnage, temporary_comment]




    return modified_task_table

if __name__ == '__main__':
    dict = week_task_dict()

    for date, shift in dict.items():
        print(date)
        print('     ')