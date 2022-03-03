from TikTokApi import TikTokApi
import csv


# open the file in the write mode
f = open('C:/Users/Patri/Documents/test.csv', 'w', encoding='utf-8')

#attributes
fieldnames = ['index', 'id', 'nickname', 'desc','commentCount','playCount', 'shareCount']

# create the csv writer
writer = csv.DictWriter(f, fieldnames = fieldnames)
writer.writeheader()

i = 0

#s_v_web_id for access
veritfyFp = "verify_kvztrcrc_t2PQlzpn_sWrc_4JDY_9e4x_u45vZqqb2MhC"
def results(tiktoks, i):
    for tiktok in tiktoks:
        
        # write a row to the csv file
        writer.writerow({'index' : str(i), 'id': str(tiktok['id']), 'nickname': tiktok['author']['nickname'], 'desc': tiktok['desc'] ,'commentCount':str(tiktok['stats']['commentCount']),'playCount' : str(tiktok['stats']['playCount']), 'shareCount': str(tiktok['stats']['shareCount'])})
        i = i + 1

    
def hashtag():
    api = TikTokApi.get_instance(custom_verifyFp=veritfyFp, use_test_endpoints = True)
    
    #how many tiktoks get returned per hashtag
    count = 200

    #NEEDS FIXING, should loop through list instead of individual instances
    set = {
        "Antivaxxer",
        "governmentconspiracy",
        "antivax",
        "vaccine",
        "coronavirus" 
    }
    
    #select which hashtag gets returned
    tiktoks = api.by_hashtag("Antivaxxer", count=count) 
    #Write results
    results(tiktoks, i)

    tiktoks = api.by_hashtag("governmentconspiracy", count=count) 
    results(tiktoks, i + count)
            
    tiktoks = api.by_hashtag("antivaxx", count=count) 
    results(tiktoks, i + count * 2)
    
    tiktoks = api.by_hashtag("vaccine", count=count) 
    results(tiktoks, i + count * 3)
    
    tiktoks = api.by_hashtag("coronavirus", count=count) 
    results(tiktoks, i + count * 4)
                            
hashtag()
f.close()

