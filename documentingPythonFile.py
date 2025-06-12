import pandas as pd
import sys

class GT:
    """
    :Description: The GT function takes a studentID from a given Excel file and retrieves it as a web link.
    :parameters: filepath(str) -    filepath of the Excel file
                 df(dataflame) -    dataframe containing student ID
                 A(list) -    list of student IDs
                 B(list) -    list to store URL


    **Terminal command**

    .. code-block:: console

      Format:

      (.venv) $ python3 GT.py <inputFile>

      Example Usage:

      (.venv) $ python3 GT.py  RAGE_Uday_Kiran_1.xlsx


        """

    def __init__(self):
        pass
    def run(self,file_path)->None:       
        df = pd.read_excel(file_path, engine='openpyxl')
        A = df.loc[27:45, ['Unnamed: 1']]
        B = [None] * 10000
        url = "https://web-int.u-aizu.ac.jp/thesis/Thesis2024a-Poster/"

        for i in range(len(A)):
            B[i] = url + "s" + str(A.iloc[i]['Unnamed: 1']) + "/" + str(A.iloc[i]['Unnamed: 1']) + ".pdf"
            print(B[i])

# Example of how to use the class
if __name__ == "__main__":

        if len(sys.argv) !=2 :
            print("Error! The number of input parameters do not match the total number of parameters provided ")
        else:
            file_path = sys.argv[1]
            GT_instance = GT()
            GT_instance.run(file_path)
