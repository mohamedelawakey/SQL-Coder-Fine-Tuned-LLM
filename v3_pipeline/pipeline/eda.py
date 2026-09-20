import pandas as pd

data = pd.read_csv("../fine tuning data set/train.csv")
data.head(3)

# check if it clean
print(data.shape)
print("*" * 50)
print(data.isnull().sum())
print("*" * 50)
print(data.duplicated().sum())
print("*" * 50)

# understand about core data as a text
# length with count of chars
max_question_length_with_chars = data["question"].str.len().max()
max_sql_query_length_with_chars = data["sql"].str.len().max()

# length with count of tokens (simulation)
max_question_length_with_tokens = data['question'].apply(lambda x: len(str(x).split())).max()
max_sql_query_length_with_tokens = data["sql"].apply(lambda x: len(str(x).split())).max()

print("length with count of chars")
print("max length of question:", max_question_length_with_chars)
print("max length of sql query:", max_sql_query_length_with_chars)

print("*" * 50)

print("length with count of tokens")
print("max length of question:", max_question_length_with_tokens)
print("max length of sql query:", max_sql_query_length_with_tokens)
