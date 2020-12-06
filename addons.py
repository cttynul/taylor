import datetime, re, random, os, urllib.request, time, taybook, json
from urllib.request import urlopen

def get_random_meme():
    base_dir = "./meme/"
    random_meme = random.choice([x for x in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, x))])
    return base_dir + random_meme

def get_random_gif():
    base_dir = "./gif/"
    random_gif = random.choice([x for x in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, x))])
    return base_dir + random_gif

def get_random_song():
    #convert mp3 with ffmpeg
    #ffmpeg -i input.mp3 -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 output.ogg
    base_dir = "./song/"
    random_song = random.choice([x for x in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, x))])
    return base_dir + random_song

def get_random_movie():
    with open("config.json") as f:
        data = json.loads(f.read())
        base_dirs = data["content_dirs"]
    result = []
    for base_dir in base_dirs:
        for x in os.listdir(base_dir): 
            if os.path.isfile(os.path.join(base_dir, x)):
                result.append(os.path.splitext(re.sub(r'[\(\[].*?[\)\]]', "", x))[0])
    print(result)
    return random.choice(result)

#######################################
#           /bus command              #
#######################################

def query_hellobus(fermata, linea=0):
    SATELLITE_EMOJI = "\U0001F4E1"
    CLOCK_EMOJI = "\U0001F550"
    
    time_now = datetime.datetime.now().strftime('%H%M')
    
    if linea != 0:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + linea + "&oraHHMM=" #+ str(time_now)
    else:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + "&oraHHMM=" #+ str(time_now)

    root = urlopen(url).read()
    result = re.findall('.asmx">([^<]*)', str(root))
    print(result)
    return_value = ""
    for res in result:
        result = res.replace(", ", "_").strip()
        result1, result2 = result.split("_")
        if "Previsto" in result1:
            return_value += CLOCK_EMOJI + "" + result1.replace("TperHellobus:" , "").replace("Previsto", "da orario") + "\n"
        else:
            return_value += SATELLITE_EMOJI + "" + result1.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"

        if "Previsto" in result2:
            return_value += CLOCK_EMOJI + " " + result2.replace("TperHellobus:" , "").replace("Previsto", "da orario") + "\n"
        else:
            return_value += SATELLITE_EMOJI + " " + result2.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"
    return str(return_value)

#######################################
#          /book command              #
#######################################

def get_all_authors():
    return taybook.get_all_authors()

def search_author(user_input):
    return taybook.search_author(user_input)

def retrive_books(authors, bformat="pdf"):
    return taybook.retrive_books(authors, bformat)

def wrapper_retrive_books(authors):
    return retrive_books(authors)

def clean_book_cache(file_list):
    for f in file_list:
        os.remove(f)

    