import sqlalchemy
from sqlalchemy.orm import Session
from PeaTMOSS import *

### This demo is an example of how one could use SQLAlchemy to interact with the PeaTMOSS database in order to answer
### one of the research questions, in this case question I1: "It can be difficult to interpret model popularity numbers by 
### download rates. To what extent does a PTM’s download rates correlate with the number of GitHub projects that rely on it, or 
### the popularity of the GitHub projects?". This demo also includes equivalent SQL queries of SQLAlchemy statements. 

if __name__ == "__main__":

    ### When creating an absolute path string, make sure there is a leading forward slash (/)
    absolute_path = "/scratch/bell/rsashti/sql_db/PeaTMOSS.db" #change this to an appropriate filepath for your directory
    engine = sqlalchemy.create_engine(f"sqlite:///{absolute_path}")
    # relative_path = "PeaTMOSS.db"
    # engine = sqlalchemy.create_engine(f"sqlite:///{relative_path}")

    highly_downloaded = {}
    reused_rates = {}
    with Session(engine) as session:
        # Query the 100 most downloaded models from the Model table
        query_name_downloads = sqlalchemy.select(Model.id, Model.context_id, Model.downloads) \
            .limit(100).order_by(sqlalchemy.desc(Model.downloads)) # The Model class is declared in PeaTMOSS
        '''
        Equivalent SQL query to the above SQLAlchemy statement:

        SELECT id, context_id, downloads FROM Model
        ORDER BY downloads DESC
        LIMIT 100

        '''
        ### When executing a query that selects an entire table like ".select(PeaTMOSS.Model)" (equivalent to SELECT * FROM Model), 
        ### it is important to note that the return value will be a list of tuples of objects, where each tuple only contains 
        ### one object, like [(<PeaTMOSS Model Object at 0x{mem_address}>,) (<PeaTMOSS Model Object at 0x{mem_address}>,) etc.].
        ### In this case, in the for loop you have to access the first element in order to access the fields, or you will get a key
        ### error. In the loop below, this would look like "model[0].downloads" if you were to access the downloads field.
        
        models = session.execute(query_name_downloads).all()
        for model in models:
            highly_downloaded[model.context_id] = model.downloads
            # Query the instances where this model's ID appears in the model_to_reuse_repository table 
            query_num_reuses = sqlalchemy.select(model_to_reuse_repository.columns.model_id) \
                .where(model_to_reuse_repository.columns.model_id == model.id)
            '''
            Equivalent SQL query to the above SQLAlchemy statement:

            SELECT model_id FROM model_to_reuse_repository
            WHERE model_id = {insert model id here}

            '''
            num_reuses = len(session.execute(query_num_reuses).all())
            reused_rates[model.context_id] = num_reuses

    print(highly_downloaded)
    print(reused_rates)

    ### From here you may observe correlations between the two dictionaries
