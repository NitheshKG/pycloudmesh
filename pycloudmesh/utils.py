import pandas as pd

def convert_json_to_csv(response_json):

    df = pd.DataFrame(response_json)
    df.to_csv("output_response.csv", index=False)

