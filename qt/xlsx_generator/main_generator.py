import parser
import datetime
from brigade_generator import parse
from sqlite_request import work_centres_list
import xlsxwriter

def generate(file_path):

    print(file_path)


    def date_col_position(sheet_dic, check_date):

        for col_num, dt in enumerate(sheet_dic):
            if datetime.datetime.fromisoformat(str(dt)) == datetime.datetime.fromisoformat(str(check_date)):
                return col_num



    def cell_check(cell_data):
        try:
            if datetime.datetime.fromisoformat(cell_data):
                return 'date'
        except ValueError:
            work_centre = [i[0] for i in work_centres_list()]
            yellow_list = ['СТв', '4рв']
            gray_list = ['СТз', '4рз']
            blue_list = ['3рв', '3рз']
            if cell_data in work_centre:
                return 'work centre'
            elif cell_data in yellow_list:
                return 'yellow'
            elif cell_data in gray_list:
                return 'gray'
            elif cell_data in blue_list:
                return 'blue'
            elif len(cell_data) > 15:
                return 'red'
            else:
                return 'white'




    #отримання словника із завданням після парсингу таблиці із завданням
    dic = parser.week_task_dict()


    #======================================================================================================================
    # побригадний словник (переформатування у формат:
    # {Бригада1: {Дата1: [зміна, лінія, бригада, лінія, бригада...], {Дата2:... ...}
    # {Бригада2: ...}
    # ...
    temporary_data = parse(dic)
    print(temporary_data)



    workbook = xlsxwriter.Workbook('СКЕЛЕТ.xlsx')

    format_date = workbook.add_format({'align': 'center', 'border': 1, 'bold': 1, 'bg_color': '#53ff1d', 'num_format': 'd mmm, nn'})
    format_green_bold = workbook.add_format({'align': 'center', 'border': 1, 'bold': 1, 'bg_color': '#53ff1d'})
    format_yellow = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#ffff00'})
    format_gray = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#cccccc'})
    format_blue = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#b4c7fc'})
    format_white = workbook.add_format({'align': 'center', 'border': 1})
    format_red = workbook.add_format({'align': 'center', 'border': 1, 'bg_color': '#ff0000'})

    cell_formats = {
        'date': format_date,
        'work centre': format_green_bold,
        'yellow': format_yellow,
        'gray': format_gray,
        'blue': format_blue,
        'white': format_white,
        'red': format_red
    }



    for brigade_num, dates in enumerate(temporary_data.values()):
        brigade_num += 1
        brigade_sheet = workbook.add_worksheet(f'Бригада {brigade_num}')

        for position, date in enumerate(dates.keys()):
            brigade_sheet.write(0, position, date, format_date)

        for col_num, date_brigade in enumerate(dates.values()):

            if date_brigade[0] == '1':
                date_brigade[0] = '1зм 7:00'
            if date_brigade[0] == '2':
                date_brigade[0] = '2зм 15:00'
            if date_brigade[0] == '3':
                date_brigade[0] = '3зм 22:00'

            for row_num, cell_value in enumerate(date_brigade):
                brigade_sheet.write(row_num+1, col_num, cell_value, cell_formats[cell_check(str(cell_value))])



    workbook.close()

if __name__ == '__main__':
    generate('1')





