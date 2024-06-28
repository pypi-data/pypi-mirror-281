from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import col
import numpy as np
from scipy.stats import chi2_contingency, f_oneway
import seaborn as sns
import matplotlib.pyplot as plt
from .utils import round_off

def get_bivariate_analysis(df, table_name, print_graphs=0, id_columns=None, correlation_analysis=1, cramer_analysis=1, anova_analysis=1):
    """
    Perform bivariate analysis on the given DataFrame and save the results in a single table.

    Parameters:
    df (DataFrame): The input DataFrame for analysis.
    table_name (str): The base table name to save the results.
    print_graphs (bool): Whether to print scatter plot graphs.
    id_columns (list): List of ID columns to drop.
    correlation_analysis (bool): Whether to perform correlation analysis.
    cramer_analysis (bool): Whether to perform Cramer's V analysis.
    anova_analysis (bool): Whether to perform ANOVA analysis.
    """
    spark = SparkSession.builder.getOrCreate()
    
    # Drop the ID column if provided
    if id_columns:
        df = df.drop(*id_columns)

    # Drop columns with all null values
    not_null_columns = [col for col in df.columns if df.filter(df[col].isNotNull()).count() == 0]
    df = df.drop(*not_null_columns)

    # Get numerical columns and categorical columns
    numerical_columns = [col for col, dtype in df.dtypes if dtype in ['int', 'double']]
    categorical_columns = [col for col, dtype in df.dtypes if dtype == 'string']

    # Schema definition for result DataFrame
    result_schema = StructType([
        StructField('Column_1', StringType(), nullable=False),
        StructField('Column_2', StringType(), nullable=False),
        StructField('Correlation_Coefficient', DoubleType(), nullable=True),
        StructField('Cramers_V', DoubleType(), nullable=True),
        StructField('Anova_F_Value', DoubleType(), nullable=True),
        StructField('Anova_P_Value', DoubleType(), nullable=True)
    ])
    # Drop the table if it exists
    spark.sql(f"DROP TABLE IF EXISTS {table_name}")

    # Numerical vs numerical analysis - correlation coefficient
    '''The correlation coefficient is a statistical measure of the strength of a linear relationship between two variables.
    Its values can range from -1 to 1.
    A correlation coefficient of -1 describes a perfect negative, or inverse, correlation.
    A coefficient of 1 shows a perfect positive correlation, or a direct relationship.
    A correlation coefficient of 0 means there is no linear relationship.'''
    if correlation_analysis and numerical_columns:
        for i in range(len(numerical_columns)):
            for j in range(i + 1, len(numerical_columns)):
                col1 = numerical_columns[i]
                col2 = numerical_columns[j]
                corr = df.stat.corr(col1, col2)
                new_row = spark.createDataFrame([(col1, col2, round_off(corr, dec=4),None,None,None)], schema=result_schema)
                new_row.write.option("mergeSchema", "true").saveAsTable(table_name, mode='append')

    # Categorical vs categorical analysis - Cramer's V
    '''Cramers V is a measure of the strength of association between two nominal variables. It ranges from 0 to 1 where:
    0 indicates no association between the two variables. 1 indicates a perfect association between the two variables.'''
    if cramer_analysis and categorical_columns and len(categorical_columns) >= 2:
        def cramers_v(contingency_table):
            chi2 = chi2_contingency(contingency_table)[0]
            n = contingency_table.sum()
            return np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))

        for i in range(len(categorical_columns)):
            for j in range(i + 1, len(categorical_columns)):
                col1 = categorical_columns[i]
                col2 = categorical_columns[j]

                filtered_df = df.filter(col(col1).isNotNull() & col(col2).isNotNull())
                contingency_table = filtered_df.groupBy(col1, col2).count().groupBy(col1).pivot(col2).sum("count").fillna(0)
                data = contingency_table.collect()
                counts = np.array([row[1:] for row in data], dtype=int)
                counts = counts[~(counts == 0).all(1)]
                counts = counts[:, ~(counts == 0).all(0)]

                if counts.size > 0:
                    v = cramers_v(counts)
                    new_row = spark.createDataFrame([(col1, col2,None, round_off(v),None,None)], schema=result_schema)
                    new_row.write.option("mergeSchema", "true").saveAsTable(table_name, mode='append')

    # Numerical vs categorical analysis - ANOVA
    '''ANOVA (Analysis of Variance) tests whether there are significant differences between the means of different groups.
    F-Value: A higher F-value indicates greater variance between groups compared to within groups.
    P-Value: A P-value < 0.05 typically indicates significant differences between group means,
    suggesting the categorical variable impacts the numerical variable.'''
    if anova_analysis and numerical_columns and categorical_columns:
        for num_col in numerical_columns:
            for cat_col in categorical_columns:
                df = df.withColumn(num_col, col(num_col).cast('double'))
                summary_stats = df.groupBy(cat_col).agg(F.mean(num_col).alias('mean'), F.count(num_col).alias('count'))
                summary_list = summary_stats.collect()
                overall_mean = df.select(F.mean(col(num_col)).alias('mean')).collect()[0]['mean']
                ssb = sum(row['count'] * (row['mean'] - overall_mean) ** 2 for row in summary_list)
                ssw = df.withColumn('squared_diff', (col(num_col) - overall_mean) ** 2).agg(F.sum('squared_diff').alias('ssw')).collect()[0]['ssw']
                df_b = len(summary_list) - 1
                df_w = df.count() - len(summary_list)
                f_val = (ssb / df_b) / (ssw / df_w)
                category_groups = [df.filter(col(cat_col) == row[cat_col]).select(num_col).rdd.flatMap(lambda x: x).collect() for row in summary_list]
                p_val = f_oneway(*category_groups)[1]
                new_row= spark.createDataFrame([(num_col, cat_col, None,None, round_off(f_val), round_off(p_val))], schema=result_schema)
                new_row.write.option("mergeSchema", "true").saveAsTable(table_name, mode='append')

    # Shows scatter plot if the user wants
    if print_graphs:
        scatter_pairs = [(col1, col2) for i, col1 in enumerate(numerical_columns) for col2 in numerical_columns[i+1:]]

        def plot_scatter(pair):
            col1, col2 = pair
            data = df.select(col1, col2).dropna().toPandas()
            plt.figure(figsize=(5, 3))
            sns.scatterplot(data=data, x=col1, y=col2)
            plt.title(f'Scatter Plot between {col1} and {col2}')
            plt.xlabel(col1)
            plt.ylabel(col2)
            plt.show()

        for pair in scatter_pairs:
            plot_scatter(pair)

    print(f"The results have been successfully saved to the table: {table_name}")