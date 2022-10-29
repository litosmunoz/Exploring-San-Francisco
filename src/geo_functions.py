def Company_raised(c):
    filter_ = {"$and": [{'offices': {'$exists': 1}}, {'total_money_raised' : {'$regex' : '[$€].*[MB]'}}]}
    projection = {'name':1, '_id':0, 'total_money_raised':1, 'offices.country_code': 1, "offices.state_code":1,'offices.city':1,'offices.latitude':1,'offices.longitude':1}
    list_ = list(c.find(filter_, projection).sort('offices.country_code'))[20:]
    df = pd.DataFrame(list_).explode("offices").reset_index(drop=True)
    df = pd.concat([df, df["offices"].apply(pd.Series)], axis=1).reset_index(drop=True)
    df.dropna(subset=["latitude"],inplace=True)
    df.dropna(subset=["city"],inplace=True)
    df.drop(columns= 'offices', inplace=True)
    df.drop(columns= 0, inplace=True)
    return df