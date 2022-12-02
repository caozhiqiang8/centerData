import json
from flask import  render_template, request
from public.db_con import mysql_connect
from practise import practise_book_blue



# 练习册录入路由
@practise_book_blue.route('/book', methods=['get'])
def book():
    return render_template('book.html')


# 练习册分析
@practise_book_blue.route('/bookInfo', methods=['get'])
def bookInfo():
    code = request.values.get('code')
    print(code)
    sql = '''
            SELECT 
             g.grade_name, s.subject_name, v.version_name, m.material_name, eb.book_id ,eb.book_name,p.paper_count ,DATE_FORMAT(eb.c_time,'%%Y-%%m-%%d %%H:%%i:%%S') as c_time,eb.press_name,b.school_id,b.name
             from exercise_book_info eb
            LEFT JOIN
            (SELECT fr.school_id ,fr.name,bs.book_id
            from franchised_school_info fr ,book_school bs where fr.school_id = bs.school_id and fr.SCHOOL_TYPE in (3,4)  
            GROUP BY bs.book_id,fr.school_id) b
            on eb.book_id = b.book_id
            LEFT JOIN (SELECT p.practice_book_id,COUNT(*)as paper_count FROM  as_answer_sheet_info p  WHERE  p.paper_id > 0 and practice_book_id is not null
            group by p.practice_book_id) p
            on eb.book_id = p.practice_book_id
             LEFT JOIN subject_info s
            ON eb.subject_id = s.subject_id
             LEFT JOIN grade_info g
                  ON eb.grade_id = g.grade_id
            LEFT JOIN teach_version_info v
            ON eb.version_id = v.version_id
            LEFT JOIN teaching_material_info m
            ON eb.material_id = m.material_id
            ORDER BY g.grade_id,s.subject_id,v.version_id,m.material_id,b.school_id
            '''
    bookData = mysql_connect(sql)
    if code == '1':

        bookDistinct = bookData.iloc[:, :8].drop_duplicates()
        bookInfo = json.loads(bookDistinct.to_json(orient='records', force_ascii=False))

        bookPaperCount = bookData['paper_count'].sum()
        bookCount = bookDistinct['book_id'].count()
        schoolCount = bookData['school_id'].count()

        data = {
            'bookInfo': bookInfo,
            'bookCount': str(bookCount),
            'bookPaperCount': int(bookPaperCount),
            'schoolCount': str(schoolCount),
        }
        return data

    elif code == '2':
        bookGradeSubject = bookData.groupby(['grade_name', 'subject_name'], as_index=False)['book_id'].nunique().iloc[:,
                           0:4]
        bookGradeSubject = json.loads(bookGradeSubject.to_json(orient='records', force_ascii=False))

        data = {
            'bookGradeSubject': bookGradeSubject,
        }
        return data

    elif code == '3':
        bookSchool = bookData.groupby(
            ['book_id', 'book_name', 'version_name', 'material_name', 'grade_name', 'subject_name'],
            as_index=False).agg({'name': list})
        bookSchool = bookSchool.sort_values(by=['grade_name', 'subject_name', 'version_name', 'material_name'],
                                            ascending=False)
        bookSchool = json.loads(bookSchool.to_json(orient='records', force_ascii=False))

        data = {
            'bookSchool': bookSchool,
        }
        return data

    elif code == '4':
        schoolBook = bookData.groupby(['school_id', 'name'], as_index=False).agg({'book_name': '；'.join})
        schoolBook = json.loads(schoolBook.to_json(orient='records', force_ascii=False))

        data = {
            'schoolBook': schoolBook,
        }
        return data
