Create a script called synthetic seed data ingestion in scripts this should do the following,
* In data folder create seed_data folder.
* In write python script which will generated connected tables with common ids.
* Here are some example data which should be stored in these tables,
	* B2B sales data
		* Ecommerce
		* Modern trade
		* Traditional trade
	* B2C data
	* Promotion related data
* Identify which all tables makes sense.
* These datasets should be realistic
* It is okay if the data is not star schema, 3NF but relationships between tables should make sense.
* At least 10k rows wherever possible to make things realistic.

Ultrathink and come up with a script which will generate these datasets, save them as csv files. 

---

Write a script which will do the following,

* Analyse all the tables from MS SQL for a given schema
* Carefully look into the values and suggests following,
	* appropriate data type | consider max length and buffer for future values
	* column name
	* table name
	* tables should be refactored or not
	* appropriate db model | star schema, 1NF, 2NF, 3NF
	* PK, FK data type consistent or not
	* Schema description
	* Table description
	* Column description
	* top 10 sample values by each column from each table ordered by frequency
	* Any categorical column is high cardinality column or not > 200 unique values.
All of above has to be returned as JSON. While generating keep in mind that this info will be used for NL2SQL engine. Use LLM via LiteLLM proxy from docker compose. Env variables are present in .env. Check LLM usage pattern from engine folder if required. Use gpt-4.1 from Azure as LLM.
---


Update the script with following functionality,

* calling out with current data quality where NL2SQL engine is failing to generate correct SQL. Break it down into following buckets,
	* wrong table selected
	* wrong column selected
	* wrong filter condition
	* wrong join condition
	* wrong aggregation function
* In each table description add columns present, how it can be used for analysis, what all analysis can be done. how it is connected to other tables.
* In schema description add overall schema level analysis, what all analysis can be done using this schema, what all business questions can be answered using this schema.
* In column description add how this column can be used for analysis, what all business questions can be answered using this column. Sample values already present.
* Extract and store DDL for each table in a separate key in JSON.
* Extract PK and FK constraints and store them in separate keys in JSON. Update NL2SQL friendly description along with DDL and constraints so that it can be used while generating SQL.

Rerun and validate the script is working as expected and generating expected output.
