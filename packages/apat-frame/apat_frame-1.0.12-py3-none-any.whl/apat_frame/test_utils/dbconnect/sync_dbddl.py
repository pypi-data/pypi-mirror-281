from sqlalchemy import create_engine, exc,text
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import os
from sync_dbsetting.app1.testcaseModel import CaseManageModel
from sync_dbsetting.app1.testcaseModel import model_to_dict
import keyword

DB_URL = os.getenv('DB_URL', 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhangyuze')  # 添加默认值处理

def init_sqlalchemy_mysql():
    engine = create_engine(DB_URL)
    return scoped_session(sessionmaker(bind=engine))

def execute_with_session(function):
    """装饰器，用于自动管理Session的生命周期"""
    def wrapper(*args, **kwargs):
        session_factory = init_sqlalchemy_mysql()
        session = session_factory()
        try:
            result = function(session, *args, **kwargs)
        finally:
            session.close()
            session_factory.remove()
        return result
    return wrapper


@execute_with_session
def selectall_operations(session):
    instances = session.query(CaseManageModel).all()
    return [model_to_dict(instance) for instance in instances]

@execute_with_session
def select_operations(session, filter_column, value):
    instances = session.query(CaseManageModel).filter(getattr(CaseManageModel, filter_column) == value).all()
    return [model_to_dict(instance) for instance in instances]

@execute_with_session
def update_operations(session, code, updates):
    instance = session.query(CaseManageModel).get(code)
    if instance:
        for key, value in updates.items():
            setattr(instance, key, value)
        session.commit()
    else:
        raise ValueError(f"No instance found with code {code}")

@execute_with_session
def delete_operations(session, code):
    instance = session.query(CaseManageModel).get(code)
    if instance:
        session.delete(instance)
        session.commit()
    else:
        raise ValueError(f"No instance found with code {code}")

@execute_with_session
def insert_operations(session, **kwargs):
    new_instance = CaseManageModel(**kwargs)
    session.add(new_instance)
    session.commit()
    return "success"

@execute_with_session
def select_operations_bysql(session, **kwargs):
    # 初始化变量，默认值设定
    select_vals = '*'
    select_table = 'casemanage'
    select_condition = ''
    group_column = '' 
    order_clause = ''
    limit_number = None
    
    # 处理关键字参数
    for key, value in kwargs.items():
        if key == 'select_vals':
            select_vals = ', '.join(value) if isinstance(value, list) else value
        elif key == 'select_table':
            select_table = value
        elif key == 'select_condition':
            select_condition = str(value)  # 确保条件被转换为字符串
        elif key == 'group_column':
            group_column = value
        elif key == 'order':
            order_clause = value  # 简单处理排序指令
        elif key == 'limit_number':
            limit_number = value
        else:
            print(f"{key} is not a recognized keyword argument.")

    # 检查表名和列名是否安全
    def is_safe_identifier(identifier):
        if identifier == '*':
            return True
        return identifier.isidentifier() and not keyword.iskeyword(identifier)

    table_and_columns_safety_check = f"Checking table '{select_table}' with columns '{select_vals}', safety: "
    if not is_safe_identifier(select_table):
        table_and_columns_safety_check += "Table name is unsafe."
    else:
        column_safety = all(is_safe_identifier(col.strip()) for col in select_vals.split(','))
        table_and_columns_safety_check += "safe" if column_safety else "Column name(s) are unsafe."

    print(table_and_columns_safety_check)  # 添加这行用于调试

    if not is_safe_identifier(select_table) or not all(is_safe_identifier(col.strip()) for col in select_vals.split(',')):
        raise ValueError("Table name or column name contains unsafe characters.")
 
 
    # 构建SQL查询语句
    executesql = f'SELECT {select_vals} FROM {select_table}'
    if select_condition:
        executesql += f' WHERE {select_condition}'
    if group_column:
        executesql += f' GROUP BY {group_column}'
    if order_clause:
        executesql += f' {order_clause}'
    if limit_number is not None:
        executesql += f' LIMIT {limit_number}'
    print('这是测试语句')
    print (executesql)
    # 执行SQL并获取所有数据
    try:
        select_result = session.execute(text(executesql))
        result_list = []
        chunk = select_result.fetchmany(10)
        while chunk:
            result_list.extend(chunk)
            chunk = select_result.fetchmany(10)
        return result_list
    except Exception as e:
        print(f"An error occurred while executing the SQL: {e}")
        return None


    
# 示例使用
if __name__ == "__main__":
    # insert_operations(code='ceshi004', name='mingcheng002', description='jjjjj', 
    #                   category1='cate3', category2='cate4', status=2, script='new_script', 
    #                   expected='new_expected', actual='new_actual', result='new_result', creator='creator2', updater='updater2')
    # all_instances = selectall_operations()
    
    result = select_operations_bysql(select_condition = 'name = "mingcheng001"', limit_number = 10 )
    print(result)