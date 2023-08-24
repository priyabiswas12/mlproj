import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl") #output is stored here ie artifacts\proprocessor.pkl



class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()




    def get_data_transformer_object(self): #outputs preprocessed object
        '''
        This function is responsible for data transformation based on diff types of data
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

        
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")), #handling missing values
                ("scaler",StandardScaler()) #scaling

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)




        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")




            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object() #calling the previous function defined here

            target_column_name="math_score"
            

            x_train_df=train_df.drop(columns=[target_column_name],axis=1)
            y_train_df=train_df[target_column_name]

            x_test_df=test_df.drop(columns=[target_column_name],axis=1)
            y_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            x_train_arr=preprocessing_obj.fit_transform(x_train_df) #applying preprocessing here
            x_test_arr=preprocessing_obj.transform(x_test_df)

            train_arr = np.c_[x_train_arr, np.array(y_train_df)]
            test_arr = np.c_[x_test_arr, np.array(y_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)





