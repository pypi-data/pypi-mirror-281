SELECTOR_NAME = 'Selector'
DECOMPOSER_NAME = 'Decomposer'
REFINER_NAME = 'Refiner'
SYSTEM_NAME = 'System'

MAX_ROUND = 3  # max try times of one agent talk

features_template = """
As an experienced and professional data scientist, your task is to analyze user question, provided schema and selected tables 
to provide relevant information. The database schema consists of table descriptions, each containing multiple column 
descriptions. Your goal is to identify the attributes needed for applying feature engineering and using the dataset
 for prediction as per user's objective and represent all in a dictionary format.

Here is a typical example:

==========
【DB_ID】 banking_system
【Schema】
# Table: account
[
  (account_id, the id of the account. Value examples: [11382, 11362, 2, 1, 2367].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].),
  (frequency, frequency of the account. Value examples: ['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
  (date, the creation date of the account. Value examples: ['1997-12-29', '1997-12-28'].)
]
# Table: client
[
  (client_id, the unique number. Value examples: [13998, 13971, 2, 1, 2839].),
  (gender, gender. Value examples: ['M', 'F']. And F：female . M：male ),
  (birth_date, birth date. Value examples: ['1987-09-27', '1986-08-13'].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].)
]
【Foreign keys】
client.`district_id` = district.`district_id`
【Relevant DB Schema】
```
{{
    "client": ["client_id", "gender", "date", "district_id"],
}}
```
【Question】
What is the gender of the youngest client who opened account in the lowest average salary branch?
【Evidence】
Later birthdate refers to younger age; A11 refers to average salary
【Answer】
```json
{{
  "problem_type": <classification, regression, clustering,  anomaly detection, or more>
  "training_shot": <recommended training shots number; number of different patterns in the data, minimum 10%>,
  "seed": <recommended seed for the prediction>",
  "task_class": <sklearn.ensemble.RandomForestClassifier (current support is only classification)>,
  "features": [ list of the relevant attributes ],
  "target": <target_attribute>
}}
```
Question Solved.

==========

Here is a new example, please start answering:

【DB_ID】 {db_id}
【Schema】
{desc_str}
【Foreign keys】
{fk_str}
【Relevant DB Schema】
{chosen_db_schem_dict}
【Question】
{query}
【Evidence】
{evidence}
【Answer】
"""


concise_template = """
As an experienced and professional data scientist, your task is to analyze user question, provided schema and selected tables 
to provide relevant information. The database schema consists of table descriptions, each containing multiple column 
descriptions. Your goal is to identify the metadata of each columns and represent all in a dictionary format.

Here is a typical example:

==========
【DB_ID】 banking_system
【Schema】
# Table: account
[
  (account_id, the id of the account. Value examples: [11382, 11362, 2, 1, 2367].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].),
  (frequency, frequency of the account. Value examples: ['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
  (date, the creation date of the account. Value examples: ['1997-12-29', '1997-12-28'].)
]
# Table: client
[
  (client_id, the unique number. Value examples: [13998, 13971, 2, 1, 2839].),
  (gender, gender. Value examples: ['M', 'F']. And F：female . M：male ),
  (birth_date, birth date. Value examples: ['1987-09-27', '1986-08-13'].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].)
]
【Foreign keys】
client.`district_id` = district.`district_id`
【Relevant DB Schema】
```
{{
    "client": ["client_id", "gender", "date", "district_id"],
}}
```
【Question】
What is the gender of the youngest client who opened account in the lowest average salary branch?
【Evidence】
Later birthdate refers to younger age; A11 refers to average salary
【Answer】
```json
{{
  "client_id": "the id of the client (identifier)",
  "gender": "gender of the client",
  "birth_date": "birth date of the client",
  "district_id": "the id of the district (identifier)",
}}
```
Question Solved.

==========

Here is a new example, please start answering:

【DB_ID】 {db_id}
【Schema】
{desc_str}
【Foreign keys】
{fk_str}
【Relevant DB Schema】
{chosen_db_schem_dict}
【Question】
{query}
【Evidence】
{evidence}
【Answer】
"""


selector_template = """
As an experienced and professional database scientist, your task is to analyze a user question and a database schema to provide relevant information. The database schema consists of table descriptions, each containing multiple column descriptions. Your goal is to identify the relevant tables and columns based on the user question and evidence provided.

[Instruction]:
1. Discard any table schema that is not related to the user question and evidence.
2. Sort the columns in each relevant table in descending order of relevance and keep the top 6 columns.
3. Ensure that at least 3 tables are included in the final output JSON.
4. The output should be in JSON format.

Requirements:
1. If a table has less than or equal to 10 columns, mark it as "keep_all".
2. If a table is completely irrelevant to the user question and evidence, mark it as "drop_all".
3. Prioritize the columns in each relevant table based on their relevance.

Here is a typical example:

==========
【DB_ID】 banking_system
【Schema】
# Table: account
[
  (account_id, the id of the account. Value examples: [11382, 11362, 2, 1, 2367].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].),
  (frequency, frequency of the account. Value examples: ['POPLATEK MESICNE', 'POPLATEK TYDNE', 'POPLATEK PO OBRATU'].),
  (date, the creation date of the account. Value examples: ['1997-12-29', '1997-12-28'].)
]
# Table: client
[
  (client_id, the unique number. Value examples: [13998, 13971, 2, 1, 2839].),
  (gender, gender. Value examples: ['M', 'F']. And F：female . M：male ),
  (birth_date, birth date. Value examples: ['1987-09-27', '1986-08-13'].),
  (district_id, location of branch. Value examples: [77, 76, 2, 1, 39].)
]
# Table: loan
[
  (loan_id, the id number identifying the loan data. Value examples: [4959, 4960, 4961].),
  (account_id, the id number identifying the account. Value examples: [10, 80, 55, 43].),
  (date, the date when the loan is approved. Value examples: ['1998-07-12', '1998-04-19'].),
  (amount, the id number identifying the loan data. Value examples: [1567, 7877, 9988].),
  (duration, the id number identifying the loan data. Value examples: [60, 48, 24, 12, 36].),
  (payments, the id number identifying the loan data. Value examples: [3456, 8972, 9845].),
  (status, the id number identifying the loan data. Value examples: ['C', 'A', 'D', 'B'].)
]
# Table: district
[
  (district_id, location of branch. Value examples: [77, 76].),
  (A2, area in square kilometers. Value examples: [50.5, 48.9].),
  (A4, number of inhabitants. Value examples: [95907, 95616].),
  (A5, number of households. Value examples: [35678, 34892].),
  (A6, literacy rate. Value examples: [95.6, 92.3, 89.7].),
  (A7, number of entrepreneurs. Value examples: [1234, 1456].),
  (A8, number of cities. Value examples: [5, 4].),
  (A9, number of schools. Value examples: [15, 12, 10].),
  (A10, number of hospitals. Value examples: [8, 6, 4].),
  (A11, average salary. Value examples: [12541, 11277].),
  (A12, poverty rate. Value examples: [12.4, 9.8].),
  (A13, unemployment rate. Value examples: [8.2, 7.9].),
  (A15, number of crimes. Value examples: [256, 189].)
]
【Foreign keys】
client.`district_id` = district.`district_id`
【Question】
What is the gender of the youngest client who opened account in the lowest average salary branch?
【Evidence】
Later birthdate refers to younger age; A11 refers to average salary
【Answer】
```json
{{
  "account": "keep_all",
  "client": "keep_all",
  "loan": "drop_all",
  "district": ["district_id", "A11", "A2", "A4", "A6", "A7"]
}}
```
Question Solved.

==========

Here is a new example, please start answering:

【DB_ID】 {db_id}
【Schema】
{desc_str}
【Foreign keys】
{fk_str}
【Question】
{query}
【Evidence】
{evidence}
【Answer】
"""

di_selector_template = """
As an experienced and professional data scientist, your task is to analyze a user question and a database schema to provide relevant information. The database schema consists of table descriptions, each containing multiple column descriptions. Your goal is to identify the relevant tables and columns based on the user question and evidence provided.

[Instruction]:
1. Discard any table schema that is not related to the user question and evidence.
2. Sort the columns in each relevant table in descending order of relevance and keep the top 6 columns.
3. Ensure that at least 3 tables are included in the final output JSON.
4. The output should be in JSON format.

Requirements:
1. If a table has less than or equal to 10 columns, mark it as "keep_all".
2. If a table is completely irrelevant to the user question and evidence, mark it as "drop_all".
3. Prioritize the columns in each relevant table based on their relevance.

Here is a typical example:

==========
【DB_ID】 health_data
【Schema】
# Table: heart
[
  (Age, age. Value examples: [40, 49, 37, 48, 54, 39].),
  (Sex, sex. Value examples: ['M', 'F'].),
  (ChestPainType, chestpaintype. Value examples: ['ATA', 'NAP', 'ASY', 'TA'].),
  (RestingBP, restingbp. Value examples: [140, 160, 130, 138, 150, 120].),
  (Cholesterol, cholesterol. Value examples: [289, 180, 283, 214, 195, 339].),
  (FastingBS, fastingbs. Value examples: [0, 1].),
  (RestingECG, restingecg. Value examples: ['Normal', 'ST', 'LVH'].),
  (MaxHR, maxhr. Value examples: [172, 156, 98, 108, 122, 170].),
  (ExerciseAngina, exerciseangina. Value examples: ['N', 'Y'].),
  (Oldpeak, oldpeak. Value examples: [0.0, 1.0, 1.5, 2.0, 3.0, 4.0].),
  (ST_Slope, st slope. Value examples: ['Up', 'Flat', 'Down'].),
  (HeartDisease, heartdisease. Value examples: ['no', 'yes'].)
]
# Table: myocardial
[
  (AGE, age. Value examples: [55.0, 64.0, 70.0, 77.0, 71.0, 50.0].),
  (SEX, sex. Value examples: ['male', 'female'].),
  (INF_ANAM, inf anam. Value examples: ['one', 'zero', 'two', 'three and more'].),
  (STENOK_AN, stenok an. Value examples: ['never', 'during the last year', 'more than 5 years ago', '4-5 years ago', 'one year ago', 'two years ago'].),
  (FK_STENOK, fk stenok. Value examples: ['there is no angina pectoris', 'II FC', 'IV FC', 'I FC', 'III FC.'].),
  (IBS_POST, ibs post. Value examples: ['there was no СHD', 'exertional angina pectoris', 'unstable angina pectoris'].),
  (GB, gb. Value examples: ['there is no essential hypertension', 'Stage 2', 'Stage 3', 'Stage 1'].),
  (SIM_GIPERT, sim gipert. Value examples: ['no', 'yes'].),
  (DLIT_AG, dlit ag. Value examples: ['there was no arterial hypertension', 'more than 10 years', '6-10 years', 'three years', 'two years', 'one year'].),
  (ZSN_A, zsn a. Value examples: ['there is no chronic heart failure', 'I stage', 'IIА stage', 'IIB stage'].),
  (fibr_ter_07, fibr ter 07. Value examples: ['no', 'yes'].),
  (fibr_ter_08, fibr ter 08. Value examples: ['no', 'yes'].),
  (ALT_BLOOD, alt blood. Value examples: [0.38, 0.45, 0.3, 0.15, 1.13, 0.23].),
  (AST_BLOOD, ast blood. Value examples: [0.18, 0.22, 0.11, 0.45, 0.6, 0.15].),
  (L_BLOOD, l blood. Value examples: [7.8, 7.2, 11.1, 6.9, 9.1, 9.6].),
  (ROE, roe. Value examples: [3.0, 2.0, 5.0, 30.0, 18.0, 15.0].),
  (TIME_B_S, time b s. Value examples: ['2-4 hours', 'less than 2 hours', '4-6 hours', '6-8 hours', '8-12 hours', 'more than 3 days'].),
  (NITR_S, nitr s. Value examples: ['no', 'yes'].),
  (LID_S_n, lid s n. Value examples: ['yes', 'no'].),
  (B_BLOK_S_n, b blok s n. Value examples: ['no', 'yes'].),
  (ANT_CA_S_n, ant ca s n. Value examples: ['yes', 'no'].),
  (GEPAR_S_n, gepar s n. Value examples: ['yes', 'no'].),
  (ASP_S_n, asp s n. Value examples: ['yes', 'no'].),
  (TIKL_S_n, tikl s n. Value examples: ['no', 'yes'].),
  (TRENT_S_n, trent s n. Value examples: ['yes', 'no'].),
  (ZSN, zsn. Value examples: ['no', 'yes'].)
]
# Table: diabetes
[
  (Pregnancies, pregnancies. Value examples: [6, 1, 8, 0, 5, 3].),
  (Glucose, glucose. Value examples: [148, 85, 183, 89, 137, 116].),
  (BloodPressure, bloodpressure. Value examples: [72, 66, 64, 40, 74, 50].),
  (SkinThickness, skinthickness. Value examples: [35, 29, 0, 23, 32, 45].),
  (Insulin, insulin. Value examples: [0, 94, 168, 88, 543, 846].),
  (BMI, bmi. Value examples: [33.6, 26.6, 23.3, 28.1, 43.1, 25.6].),
  (DiabetesPedigreeFunction, diabetespedigreefunction. Value examples: [0.627, 0.351, 0.672, 0.167, 2.288, 0.201].),
  (Age, age. Value examples: [50, 31, 32, 21, 33, 30].),
  (Outcome, outcome. Value examples: ['yes', 'no'].)
]
【Foreign keys】

【Question】
Does this patient have diabetes? Yes or no?
【Evidence】

【Answer】
```json
{{
  "heart": "drop_all",
  "myocardial": "drop_all",
  "diabetes": "keep_all",
  "xyz": ["district_id", "A11", "A2", "A4", "A6", "A7"]
}}
```
Question Solved.

==========

Here is a new example, please start answering:

【DB_ID】 {db_id}
【Schema】
{desc_str}
【Foreign keys】
{fk_str}
【Question】
{query}
【Evidence】
{evidence}
【Answer】
"""


decompose_template_spider = """
Given a 【Database schema】 description, and the 【Question】, you need to use valid SQLite and understand the database, and then generate the corresponding SQL.

==========

【Database schema】
# Table: stadium
[
  (Stadium_ID, stadium id. Value examples: [1, 2, 3, 4, 5, 6].),
  (Location, location. Value examples: ['Stirling Albion', 'Raith Rovers', "Queen's Park", 'Peterhead', 'East Fife', 'Brechin City'].),
  (Name, name. Value examples: ["Stark's Park", 'Somerset Park', 'Recreation Park', 'Hampden Park', 'Glebe Park', 'Gayfield Park'].),
  (Capacity, capacity. Value examples: [52500, 11998, 10104, 4125, 4000, 3960].),
  (Highest, highest. Value examples: [4812, 2363, 1980, 1763, 1125, 1057].),
  (Lowest, lowest. Value examples: [1294, 1057, 533, 466, 411, 404].),
  (Average, average. Value examples: [2106, 1477, 864, 730, 642, 638].)
]
# Table: concert
[
  (concert_ID, concert id. Value examples: [1, 2, 3, 4, 5, 6].),
  (concert_Name, concert name. Value examples: ['Week 1', 'Week 2', 'Super bootcamp', 'Home Visits', 'Auditions'].),
  (Theme, theme. Value examples: ['Wide Awake', 'Party All Night', 'Happy Tonight', 'Free choice 2', 'Free choice', 'Bleeding Love'].),
  (Stadium_ID, stadium id. Value examples: ['2', '9', '7', '10', '1'].),
  (Year, year. Value examples: ['2015', '2014'].)
]
【Foreign keys】
concert.`Stadium_ID` = stadium.`Stadium_ID`
【Question】
Show the stadium name and the number of concerts in each stadium.

SQL
```sql
SELECT T1.`Name`, COUNT(*) FROM stadium AS T1 JOIN concert AS T2 ON T1.`Stadium_ID` = T2.`Stadium_ID` GROUP BY T1.`Stadium_ID`
```

Question Solved.

==========

【Database schema】
# Table: singer
[
  (Singer_ID, singer id. Value examples: [1, 2].),
  (Name, name. Value examples: ['Tribal King', 'Timbaland'].),
  (Country, country. Value examples: ['France', 'United States', 'Netherlands'].),
  (Song_Name, song name. Value examples: ['You', 'Sun', 'Love', 'Hey Oh'].),
  (Song_release_year, song release year. Value examples: ['2016', '2014'].),
  (Age, age. Value examples: [52, 43].)
]
# Table: concert
[
  (concert_ID, concert id. Value examples: [1, 2].),
  (concert_Name, concert name. Value examples: ['Super bootcamp', 'Home Visits', 'Auditions'].),
  (Theme, theme. Value examples: ['Wide Awake', 'Party All Night'].),
  (Stadium_ID, stadium id. Value examples: ['2', '9'].),
  (Year, year. Value examples: ['2015', '2014'].)
]
# Table: singer_in_concert
[
  (concert_ID, concert id. Value examples: [1, 2].),
  (Singer_ID, singer id. Value examples: ['3', '6'].)
]
【Foreign keys】
singer_in_concert.`Singer_ID` = singer.`Singer_ID`
singer_in_concert.`concert_ID` = concert.`concert_ID`
【Question】
Show the name and the release year of the song by the youngest singer.


SQL
```sql
SELECT `Song_Name`, `Song_release_year` FROM singer WHERE Age = (SELECT MIN(Age) FROM singer)
```

Question Solved.

==========

【Database schema】
{desc_str}
【Foreign keys】
{fk_str}
【Question】
{query}

SQL

"""

refiner_template = """
【Instruction】
When executing SQL below, some errors occurred, please fix up SQL based on query and database info.
Solve the task step by step if you need to. Using SQL format in the code block, and indicate script type in the code block.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
【Constraints】
- In `SELECT <column>`, just select needed columns in the 【Question】 without any unnecessary column or value
- In `FROM <table>` or `JOIN <table>`, do not include unnecessary table
- If use max or min func, `JOIN <table>` FIRST, THEN use `SELECT MAX(<column>)` or `SELECT MIN(<column>)`
- If [Value examples] of <column> has 'None' or None, use `JOIN <table>` or `WHERE <column> is NOT NULL` is better
- If use `ORDER BY <column> ASC|DESC`, add `GROUP BY <column>` before to select distinct values
【Query】
-- {query}
【Evidence】
{evidence}
【Database info】
{desc_str}
【Foreign keys】
{fk_str}
【old SQL】
```sql
{sql}
```
【SQLite error】 
{sqlite_error}
【Exception class】
{exception_class}

Now please fixup old SQL and generate new SQL again.
【correct SQL】
"""


subq_pattern = r"Sub question\s*\d+\s*:"
