# coding: utf-8
import json
import pyspark.sql.functions as sf
import requests
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

conf = SparkConf()
sc = SparkContext(conf=conf)
ss = SparkSession.builder.getOrCreate()



import json 
def read_creds(caminho:str):
    f = open('creds/'+caminho)
    variables = json.load(f)
    return variables
variables = read_creds('zendesk_main_creds.json')

TOKEN = variables['token']
URL = variables['url_brands']


headers = {
    'content-type': "application/json",
    'authorization': TOKEN,
}

# Executa o Request na API
response = requests.request("GET", URL, headers=headers)

body_list = json.loads(response.content.decode('utf-8'))
body = body_list['brands']


# Documentation fields
name_fields = [
    'url',
    'id',
    'name',
    'brand_url',
    'subdomain',
    'has_help_center',
    'help_center_state',
    'active',
    'default',
    'is_deleted',
    'logo',
    'signature_template',
    'created_at',
    'updated_at',
]

# Dataframe create
df = sc.parallelize(body).map(lambda x: json.dumps(x))
df = ss.read.json(df)
df = (
    df.select(name_fields)
    .fillna('')
    .withColumn("logo", sf.col("logo").cast("string"))
)


namespace,dataset='zendesk','brands'

df.write.parquet(
    "/opt/airflow/scripts/bucket/"+namespace+"/"+"brands"
)
