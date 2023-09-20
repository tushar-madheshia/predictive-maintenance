# import pandas as pd
# from snowflake.snowpark.session import Session

# def score_udf(session, udf_name,payload):
    
#     response = session.sql("SELECT " + udf_name +"("+payload+").colloct()")
#     return response
# def score_local(model_path, payload):
#     try:
#         print(model_path)
#         model = load(model_path)
#         data = pd.DataFrame(payload,index=[0])
#         prediction = str(model.predict(data)["PREDICTION"][0])
#         print(prediction)
#         if str(prediction)=="1":
#             return "Employee will leave"
#         elif str(prediction)=="0":
#             return "Employee will stay" 
#     except Exception as ex:
#         print(ex)
#         return None
    
def score(data):
    from snowflake.snowpark import Session
    connection_params = {"user":"REFRACT.FOSFOR@LNTINFOTECH.COM", 
                         "password":"Password321",
                         "account":"fya62509.us-east-1", 
                         "warehouse":"FOSFOR_REFRACT", 
                         "database":"REFRACT_SNOWFLAKE_INTEGRATION",
                         "schema":"SNOWFRACT", 
                         "role":"ACCOUNTADMIN"}

    session = Session.builder.configs(connection_params).create()
    
# def score_api():

    # return prediction

# data = {'SALARY': 62668.834,
#   'SENIORITY': 2,
#   'TENURE_MONTHS': 8,
#   'MONTHS_AFTER_COLLEGE': 106,
#   'BIRTH_YEAR': 1981,
#   'MAPPED_ROLE_CLEAN': 'nurse',
#   'SEX': 'F',
#   'ETHNICITY': 'White',
#   'HOSPITAL_TYPE': 'Acute Care Hospitals',
#   'HOSPITAL_OWNERSHIP': 'Voluntary non-profit - Church',
#   'COMPANY_NAME': 'Mayo Clinic',
#   'CITY_STATE': 'Rochester, MN',
#   'DISTANCE': '5-10mi',
#   'DEGREE_CLEAN': 'Masters_Degree',
#   'OVERTIME_HOURS': 6}
# model_path="/home/pcadmin/model.joblib.gz"
# score(model_path,data)