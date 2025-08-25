from django.shortcuts import render
import pyodbc
from django.views.decorators.csrf import csrf_exempt
import os
import logging
import json
from django.http import JsonResponse, HttpResponse

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')


"""ODBC kurulumu esnasında talimatlarda yazan veri kaynağı adı, kullanıcı adı ve parolasından farklı değerler tanımladıysanız
 tanımladığınız değerleri aşşağıda yer alan alanlara girmelisiniz """
FM_DSN_NAME = os.environ.get('FM_DSN_NAME', 'todolistwebuser')#DSN ADI
FM_USERNAME = os.environ.get('FM_USERNAME', 'todolistuser')#KULLANICI ADI
FM_PASSWORD = os.environ.get('FM_PASSWORD', 'todolistuser')#PAROLA


def get_filemaker_connection():
    try:
        conn_str = f"DSN={FM_DSN_NAME};UID={FM_USERNAME};PWD={FM_PASSWORD}"
        conn = pyodbc.connect(conn_str, autocommit=False)
        return conn
    except pyodbc.Error as ex:
        logger.error(f"FileMaker veritabanı bağlantı hatası: {ex.args[1]}")
        return None



def fetch_records(table_name, select_cols="*", where_clause="", params=(), conn=None):
    is_internal_conn = False
    if not conn:
        conn = get_filemaker_connection()
        is_internal_conn = True
    
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = f"SELECT {select_cols} FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cursor.execute(query, params)

        columns = [column[0] for column in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return records
    except Exception as ex:
        logger.error(f"VERİ ÇEKME HATASI from {table_name}: {ex}")
        return []
    finally:
        if is_internal_conn and conn:
            conn.close()

def execute_query(query, params=(), conn=None):
    is_internal_conn = False
    if not conn:
        conn = get_filemaker_connection()
        is_internal_conn = True
    
    if not conn:
        logger.error("Hata: Sorgu çalıştırmak için bağlantı kurulamadı.")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if is_internal_conn:
            conn.commit()
        return True
    except Exception as ex:
        logger.error(f"SQL Sorgu çalıştırma hatası: {ex} -- Sorgu: '{query}', Parametreler: {params}")
        if is_internal_conn:
            conn.rollback()
        return False
    finally:
        if is_internal_conn and conn:
            conn.close()

@csrf_exempt
def todo_api(request, req_task_id=None):
    table_name = "todolist"




            





    match request.method:
        


        case 'GET':
    
            filemaker_tasks = fetch_records(
                    table_name='todolist',
                    select_cols='TaskID, TaskName, TaskCompleted, CreationTimestamp',

            )
    
            if not filemaker_tasks:
                return JsonResponse([], safe=False)

            
            tasks_list = []
    
            for fm_task in filemaker_tasks:
                task_ID = fm_task.get('TaskID')
                task_name = fm_task.get('TaskName')
                task_completed = fm_task.get('TaskCompleted')
                task_creationtime = fm_task.get('CreationTimestamp')
    
                tasks_list.append({
                    "TaskID": task_ID,
                    "TaskName": task_name,
                    "TaskCompleted": task_completed,
                    "CreationTimestamp": task_creationtime,
                })
            return JsonResponse(tasks_list, safe=False)
            



        case 'POST':
            try:
                data = json.loads(request.body)
                cols = []
                placeholders = []
                params = []

                for key, value in data.items():
                    if key not in ['TaskID']:
                        cols.append(key)
                        placeholders.append('?')
                        params.append(value)

                if not cols:
                    return JsonResponse({'error':'Alanlar eksik dolduruldu!'}, status=400)

                query = f"INSERT INTO {table_name}({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
                success = execute_query(query, tuple(params))

                if success:
                    return JsonResponse({'message': 'Görev başarıyla oluşturuldu.'}, status=201)


                else:
                    return JsonResponse({'error': 'Görev oluşturulamadı.'}, status=500)


            except json.JSONDecodeError:
                return JsonResponse({'error': 'Geçersiz JSON formatı.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Sunucu hatası: {str(e)}'}, status=500)


        case 'DELETE':
            if request.path.endswith('/clear_completed/'):
                try:
                    query = f"DELETE FROM {table_name} WHERE TaskCompleted = ?"
                    success = execute_query(query, (1,))
                    if success:
                        return JsonResponse({'message': 'Tamamlanan tüm görevler başarıyla silindi.'}, status=200)
                    else:
                        return JsonResponse({'error': 'Hiçbir görev silinemedi.'}, status=500)
                except Exception as e:
                    return JsonResponse({'error': f'Sunucu hatası: {str(e)}'}, status=500)
            else:

                try:
                    if not req_task_id:
                        return JsonResponse({'error': 'Görev kimliği eksik.'}, status=400)
            
                    query = f"DELETE FROM {table_name} WHERE TaskID = ?"
                    success = execute_query(query, (req_task_id,))
                    if success:
                        return JsonResponse({'message': 'Görev başarıyla silindi.'}, status=200)
                    else:
                        return JsonResponse({'error': 'Görev bulunamadı.'}, status=404)
                except Exception as e:
                    return JsonResponse({'error': f'Sunucu hatası: {str(e)}'}, status=500) 




        case 'PATCH':
            try:


                #KEY DATA PARAMS?
                data = json.loads(request.body)
                updates = []
                params = []
                for key, value in data.items():
                    updates.append(f"{key} = ?")
                    params.append(value)

                if not req_task_id:
                    return JsonResponse({'error': 'Güncelleme için görev kimliği gerekli.'}, status=400)
                    
                query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE TaskID = ?"
                params.append(req_task_id)

                success = execute_query(query, tuple(params))

                if success:
                    return JsonResponse({'message': 'Görev başarıyla güncellendi.'}, status=200)
                else:
                    return JsonResponse({'error': 'Görev güncellenemedi.'}, status=500)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Geçersiz JSON formatı.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Sunucu hatası: {str(e)}'}, status=500)






          



  