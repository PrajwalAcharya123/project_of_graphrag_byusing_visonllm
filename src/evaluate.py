# import pandas as pd
# import re

# from query_pipeline import ask_question
# from evaluator import evaluate_answers

# # =========================
# # NORMALIZE TEXT
# # =========================
# def normalize(text):
#     if pd.isna(text):
#         return ""

#     text = str(text).lower().strip()

#     # remove spaces/newlines
#     text = re.sub(r"\s+", " ", text)

#     # remove punctuation
#     text = re.sub(r"[^\w\s$%/]", "", text)

#     return text


# # =========================
# # MAIN EVALUATION
# # =========================
# def evaluate():

#     # Read Excel file
#     file_path = "../data/sbc_test.xlsx"

#     df = pd.read_excel(file_path)
#     # ======================================
#     # REQUIRED OUTPUT COLUMNS
#     # ======================================

#     required_columns = [
#         "Predicted_Answer(Y_P)",
#         "Total_Input_Token",
#         "Total_Output_Token",
#         "Total_Token",
#         "Total_Time",
#         "Evaluation"
#     ]

#     for col in required_columns:
#         if col not in df.columns:
#             df[col] = ""

#     # Force object/string type
#     for col in required_columns:
#         df[col] = df[col].astype(object)



#     # Create columns as STRING type
#     if "Predicted_Answer(Y_P)" not in df.columns:
#         df["Predicted_Answer(Y_P)"] = ""

#     if "Evaluation" not in df.columns:
#         df["Evaluation"] = ""

#     # Force string/object dtype
#     df["Predicted_Answer(Y_P)"] = df["Predicted_Answer(Y_P)"].astype(object)

#     df["Evaluation"] = df["Evaluation"].astype(object)
#     # ======================================
#     # LOOP THROUGH QUESTIONS
#     # ======================================
#     for index, row in df.iterrows():

#         question = str(row["Question"])

#         actual_answer = str(row["Actual_Answer(Y_A)"])

#         print("\n===================================")
#         print(f"Question {index + 1}: {question}")

#         try:

#             # ======================================
#             # GET PREDICTED ANSWER
#             # ======================================
#             #predicted_answer = ask_question(question)
#             result = ask_question(question)

#             predicted_answer = result["answer"]

#             prompt_tokens = result["prompt_tokens"]

#             completion_tokens = result["completion_tokens"]

#             total_tokens = result["total_tokens"]

#             total_time = result["total_time"]
#             # Save predicted answer
#             #df.at[index, "Predicted_Answer(Y_P)"] = predicted_answer
#             # ======================================

                        
#             # STORE RESULTS
#             # ======================================

#             df.at[index, "Predicted_Answer(Y_P)"] = predicted_answer

#             df.at[index, "Total_Input_Token"] = prompt_tokens

#             df.at[index, "Total_Output_Token"] = completion_tokens

#             df.at[index, "Total_Token"] = total_tokens

#             df.at[index, "Total_Time"] = total_time




#             # # ======================================
#             # # NORMALIZE BOTH ANSWERS
#             # # ======================================
#             # actual_norm = normalize(actual_answer)

#             # predicted_norm = normalize(predicted_answer)

#             # # ======================================
#             # # EVALUATION
#             # # ======================================
#             # if actual_norm == predicted_norm:
#             #     evaluation = 1
#             # else:
#             #     evaluation = 0
            


#             df.at[index, "Evaluation"] = evaluation

#             print(f"\nActual Answer    : {actual_answer}")
#             print(f"Predicted Answer : {predicted_answer}")
#             print(f"Evaluation       : {evaluation}")

#         except Exception as e:

#             print("Error:", e)

#             df.at[index, "Predicted_Answer(Y_P)"] = "ERROR"

#             df.at[index, "Evaluation"] = 0

#     # ======================================
#     # SAVE OUTPUT
#     # ======================================
#     output_path = "../data/sbc_test_result.xlsx"
#     #output_path = "../data/evaluated_output.xlsx"

#     df.to_excel(output_path, index=False)

#     print("\n===================================")
#     print("Evaluation Completed!")
#     print(f"Saved File: {output_path}")


# if __name__ == "__main__":
#     evaluate()





import pandas as pd
from query_pipeline import ask_question
from evaluator import evaluate_answers


# =========================
# MAIN EVALUATION
# =========================
def evaluate():

    # ======================================
    # READ EXCEL FILE
    # ======================================
    file_path = "../data/sbc_test.xlsx"

    df = pd.read_excel(file_path)

    # ======================================
    # REQUIRED OUTPUT COLUMNS
    # ======================================
    required_columns = [
        "Predicted_Answer(Y_P)",
        "Total_Input_Token",
        "Total_Output_Token",
        "Total_Token",
        "Total_Time",
        "Evaluation"
    ]

    # Create missing columns
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    # Force object/string dtype
    for col in required_columns:
        df[col] = df[col].astype(object)

    # ======================================
    # LOOP THROUGH QUESTIONS
    # ======================================
    for index, row in df.iterrows():

        question = str(row["Question"])

        actual_answer = str(row["Actual_Answer(Y_A)"])

        print("\n===================================")
        print(f"Question {index + 1}: {question}")

        try:

            # ======================================
            # GET PREDICTED ANSWER
            # ======================================
            result = ask_question(question)

            predicted_answer = result["answer"]

            prompt_tokens = result["prompt_tokens"]

            completion_tokens = result["completion_tokens"]

            total_tokens = result["total_tokens"]

            total_time = result["total_time"]

            # ======================================
            # STORE RESULTS
            # ======================================
            df.at[index, "Predicted_Answer(Y_P)"] = predicted_answer

            df.at[index, "Total_Input_Token"] = prompt_tokens

            df.at[index, "Total_Output_Token"] = completion_tokens

            df.at[index, "Total_Token"] = total_tokens

            df.at[index, "Total_Time"] = total_time

            # ======================================
            # LLM EVALUATION
            # ======================================
            evaluation = evaluate_answers(
                question,
                actual_answer,
                predicted_answer
            )

            df.at[index, "Evaluation"] = evaluation

            # ======================================
            # PRINT RESULTS
            # ======================================
            print(f"\nActual Answer    : {actual_answer}")

            print(f"Predicted Answer : {predicted_answer}")

            print(f"Evaluation       : {evaluation}")

        except Exception as e:

            print("\nError:", e)

            df.at[index, "Predicted_Answer(Y_P)"] = "ERROR"

            df.at[index, "Evaluation"] = 0

    # ======================================
    # SAVE OUTPUT FILE
    # ======================================
    output_path = "../data/sbc_test_result.xlsx"

    df.to_excel(output_path, index=False)

    print("\n===================================")

    print("Evaluation Completed!")

    print(f"Saved File: {output_path}")


# ======================================
# RUN
# ======================================
if __name__ == "__main__":
    evaluate()