import sqlite3 as db
import pandas as pd

def get_people_data():
    return [
        {"Gender": "Male", "HeightCm": 171, "WeightKg": 96},
        {"Gender": "Male", "HeightCm": 161, "WeightKg": 85},
        {"Gender": "Male", "HeightCm": 180, "WeightKg": 77},
        {"Gender": "Female", "HeightCm": 166, "WeightKg": 62},
        {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
        {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]


def persist_dataframe(dataframe, tablename):
    with db.connect('my_database.db') as connection:
        dataframe.to_sql(tablename, connection, if_exists="replace")


def get_bmi_reference():
    return [
        {"BMICategory": "Underweight", "LowerLimit": 0, "UpperLimit": 18.4, "HealthRisk": "Malnutrition risk"},
        {"BMICategory": "Normal weight", "LowerLimit": 18.5, "UpperLimit": 24.9, "HealthRisk": "Low risk"},
        {"BMICategory": "Overweight", "LowerLimit": 25, "UpperLimit": 29.9, "HealthRisk": "Enhanced risk"},
        {"BMICategory": "Moderately obese", "LowerLimit": 30, "UpperLimit": 34.9, "HealthRisk": "Medium risk"},
        {"BMICategory": "Severely obese", "LowerLimit": 35, "UpperLimit": 39.9, "HealthRisk": "High risk"},
        {"BMICategory": "Very severely obese", "LowerLimit": 40, "UpperLimit": 9999, "HealthRisk": "Very high risk"}
    ]

if __name__ == '__main__':
    bmi_reference = pd.DataFrame(get_bmi_reference())
    persist_dataframe(bmi_reference, "bmi_reference")

    people_data = get_people_data()
    people_df = pd.DataFrame(people_data)
    people_df["Bmi"] = people_df.apply(lambda person: (person["WeightKg"]/(person["HeightCm"]/100.0)**2), axis=1)
    persist_dataframe(people_df, "people")
    query = '''
        select  
            p.Gender,
            p.HeightCm,
            p.WeightKg,
            p.Bmi,
            r.BMICategory,
            r.HealthRisk
        from
            people as p join bmi_reference r on
            p.Bmi between r.LowerLimit and r.UpperLimit
        '''
    data = pd.DataFrame()
    with db.connect('my_database.db') as connection:
        data = pd.read_sql_query(query, connection)
    print(data)