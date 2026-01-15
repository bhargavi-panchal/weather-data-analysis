import sys
import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# --------------------------
# Glue job arguments
# --------------------------
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --------------------------
# Current date for S3 path
# --------------------------
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# --------------------------
# Read CSV from S3
# --------------------------
weather_dyf = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": [f"s3://weather-data-project-gds/date={current_date}/weather_api_data.csv"],
        "recurse": True,
    },
    transformation_ctx="weather_dyf",
)

# --------------------------
# Rename columns to safe Redshift names
# --------------------------
changeschema_weather_dyf = ApplyMapping.apply(
    frame=weather_dyf,
    mappings=[
        ("dt", "string", "dt", "string"),
        ("weather", "string", "weather", "string"),
        ("visibility", "string", "visibility", "string"),
        ("pop", "string", "pop", "string"),
        ("dt_txt", "string", "dt_txt", "string"),
        ("main.temp", "string", "main_temp", "string"),
        ("main.feels_like", "string", "main_feels_like", "string"),
        ("main.temp_min", "string", "temp_min", "string"),
        ("main.temp_max", "string", "temp_max", "string"),
        ("main.pressure", "string", "pressure", "string"),
        ("main.sea_level", "string", "sea_level", "string"),
        ("main.grnd_level", "string", "grnd_level", "string"),
        ("main.humidity", "string", "humidity", "string"),
        ("main.temp_kf", "string", "temp_kf", "string"),
        ("clouds.all", "string", "clouds_all", "string"),
        ("wind.speed", "string", "wind_speed", "string"),
        ("wind.deg", "string", "wind_deg", "string"),
        ("wind.gust", "string", "wind_gust", "string"),
        ("snow.3h", "string", "snow_3h", "string"),
        ("sys.pod", "string", "sys_pod", "string"),
    ],
    transformation_ctx="changeschema_weather_dyf"
)

# --------------------------
# Write to Redshift
# --------------------------
redshift_output = glueContext.write_dynamic_frame.from_options(
    frame=changeschema_weather_dyf,
    connection_type="redshift",
    connection_options={
        "redshiftTmpDir": "s3://aws-glue-assets-767397682530-us-east-1/temporary/",
        "useConnectionProperties": "true",
        "aws_iam_role": "arn:aws:iam::767397682530:role/Glue-S3-Redshift-Role",
        "dbtable": "public.weather_data",
        "connectionName": "Redshift connection 2",
        "preactions": """
            DROP TABLE IF EXISTS public.weather_data;
            CREATE TABLE public.weather_data (
                dt VARCHAR,
                weather VARCHAR,
                visibility VARCHAR,
                pop VARCHAR,
                dt_txt VARCHAR,
                main_temp VARCHAR,
                main_feels_like VARCHAR,
                temp_min VARCHAR,
                temp_max VARCHAR,
                pressure VARCHAR,
                sea_level VARCHAR,
                grnd_level VARCHAR,
                humidity VARCHAR,
                temp_kf VARCHAR,
                clouds_all VARCHAR,
                wind_speed VARCHAR,
                wind_deg VARCHAR,
                wind_gust VARCHAR,
                snow_3h VARCHAR,
                sys_pod VARCHAR
            );
        """,
    },
    transformation_ctx="redshift_output",
)

# --------------------------
# Commit the Glue job
# --------------------------
job.commit()
