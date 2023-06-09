def check_if_bool_search(search_string):
    bool_operators = ['AND', 'OR']
    search_elements =[]
    oper = ''
    bool_flag = False
    for operator in bool_operators:
        if search_string.find(operator) != -1:
            search_elements = search_string.split(operator)
            oper = operator
            bool_flag = True
            search_elements = [x.strip() for x in search_elements]
    return oper,search_elements,bool_flag
  
  def vault_service():
    data = request.get_json()
    query = data.get('query', '')
    flag1 = data.get('contextual','')
    print("FLAG1:",flag1)
    #import pdb;pdb.set_trace()
    df = dd.read_parquet('/Users/raunakpandey/Downloads/DD23/pinaka/app1/utils/vault_d1', engine='fastparquet')
    
    if query == '':
        filtered_df = df.drop(['content'], axis=1)
        
    else:
        if flag1:
            print("#### CONTEXTUAL SEARCH ####")
            filtered_df = get_contextual_search(df,query)
        else:
            print("#### NORMAL SEARCH ####")
            bool_operators = ['AND','OR']
            search_elements =[]
            oper = ''
            bool_flag = False
            oper,search_elements,bool_flag = check_if_bool_search(query)
            if bool_flag == True:
                if oper == 'AND':
                    df['bool'] = df['content'].apply(lambda x: True if all(y.lower() in x.lower() for y in search_elements) else False)
                else:
                    df['bool'] = df['content'].apply(lambda x: True if any(y.lower() in x.lower() for y in search_elements) else False)
                filtered_df = df[df['bool'] == True]
                filtered_df = filtered_df.drop(['content','bool'], axis=1)
            else:
                filtered_df = df[df['content'].str.contains(query, case=False)]
                filtered_df = filtered_df.drop(['content'], axis=1)
    #import pdb;pdb.set_trace()
    if flag1:
        records = filtered_df.to_dict(orient='records')
    else:
        records = filtered_df.compute().to_dict(orient='records')
    return jsonify(records)
