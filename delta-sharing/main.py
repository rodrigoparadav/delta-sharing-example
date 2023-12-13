from share import DeltaShareClient
from log import Log

log = Log().get_instance()

# config.share or profile file, provided by Databricks
profile_file = "resources/config.share"

# Create DeltaShareClient
delta = DeltaShareClient(profile_file=profile_file)

# Print list of shares and tables
log.info(f"f{delta.get_list_of_tables()}")

# Get specific table from the list
ingresos_tbl = delta.get_table("ingresos", limit=100)


log.info(f"Print Pandas dataframe context")
df = ingresos_tbl.to_pandas()
print(df)

log.info(f"Print filtered data")
print(df[df['anlage'] == 4100002134])

log.info(f"Store data into csv file")
df.to_csv('outputs/ingresos_tbl.csv')
