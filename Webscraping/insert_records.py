import argparse, cv2, re, time, bs4
from urllib.parse import urlparse
from . import USER, WEBDRIVER, CONNECT, INSERT, EXT, json_generator
from .utils import IncrementalBar, get_hash, get_name, get_tags, generate_tags, save_image

MATCH = cv2.imread(r'Webscraping\image.jpg'), cv2.imread(r'Webscraping\video.jpg')

def extract_files(driver, path, dest=None):
    
    if dest is None: dest = path.parent

    errors = []
    errors_txt = path / 'Errors.txt'
    if errors_txt.exists():
        
        for image in errors_txt.read_text().split('\n'):
           
            image = image.strip()
            name = path.parent / image.split('/')[-1].split('?')[0]
            save_image(name, image)
        
    for file in path.glob('*json'):

        for url in json_generator(file):
            
            path = urlparse(url['url']).path[1:]
            if re.match('https://i.imgur.com/.+gif', url['url']):
                path.replace('gif', 'mp4')
            elif re.search('.+/watch.+', url['url']):
                try: path = get_url(driver, url['url'])
                except: continue

            name = dest / path.split('/')[-1]
            if name.exists(): continue
            image = (
                f'https://{url["title"]}'
                if url['url'] == 'about:blank' else 
                url['url']
                )
            
            if name.suffix == '.gifv':
                name = name.with_suffix('.mp4')
                image = image.replace('gifv', 'mp4')
            elif name.suffix == '.webp':
                name = name.with_suffix('.jpg')
            
            if not save_image(name, image): errors.append(image)
            elif name.suffix == '.gif' and b'MPEG' in name.read_bytes():
                try: name.rename(name.with_suffix('.mp4'))
                except: name.unlink(missing_ok=1)
        
        file.unlink()
    
    if errors: errors_txt.write_text('\n'.join(errors))

    for file in dest.glob('*webp'):

        name = file.with_suffix('.jpg')
        name.write_bytes(file.read_bytes())
        file.unlink()
        
    for file in dest.glob('*gifv'):

        name = file.with_suffix('.mp4')
        image = f'https://i.imgur.com/{name.name}'
        save_image(name, image)
        file.unlink()

def get_url(driver, src):

    driver.get(src)
    time.sleep(5)
    html = bs4.BeautifulSoup(driver.page_source(), 'lxml')
    url = html.find(src=re.compile('.+mp4\Z'))

    return url.get('src')

def similarity(path):

    if re.search(EXT, path.suffix, re.IGNORECASE): 
        match = MATCH[0]
        image = cv2.imread(str(path))
    else: 
        match = MATCH[1]
        image = cv2.VideoCapture(str(path)).read()[-1]

    try:
        if divmod(*image.shape[:2])[0] == divmod(*match.shape[:2])[0]:

            image = cv2.resize(image, match.shape[1::-1])
            k = cv2.subtract(image, match)
            return (k.min() + k.max()) < 20
            
    except: return True
    
def start(extract=True, add='', path=USER / r'Downloads\Images'):
    
    MYSQL = CONNECT()
    DRIVER = WEBDRIVER(profile=None)
    
    if extract: extract_files(DRIVER, path / 'Generic')
    files = [
        file for file in path.iterdir() if re.search(EXT, file.suffix, re.IGNORECASE)
        ]
    progress = IncrementalBar('Files', max=len(files))

    for file in files:
        
        progress.next()
        try:
            if (dest := get_name(file, 1)).exists() or similarity(file):
                file.unlink()
                continue
            
            if not (hash_ := get_hash(file)): continue

            if dest.suffix.lower() in ('.jpg', '.png'):

                tags, rating, exif = generate_tags(
                    general=get_tags(DRIVER, file, True), 
                    custom=True, rating=True, exif=True
                    )
                save_image(file, exif=exif)

            elif dest.suffix.lower() in ('.gif', '.webm', '.mp4'):
                
                tags, rating = generate_tags(
                    general=get_tags(DRIVER, file, True), 
                    custom=True, rating=True, exif=False
                    )

            if MYSQL.execute(INSERT[3], (
                dest.name, '', ' '.join((tags, add)), 
                rating, 1, hash_, None, None, None
                )):
                if file.replace(dest): MYSQL.commit()
                else: MYSQL.rollback()
            
        except Exception as error: print(error, '\n')
    
    DRIVER.close()
    print('\nDone')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='insert records', 
        )
    parser.add_argument(
        '-e', '--extract', type=bool,
        help='Mode argument (default True)',
        default=True
        )
    parser.add_argument(
        '-a', '--add', type=str,
        help='Initial argument (default "")',
        default=''
        )

    args = parser.parse_args()
    
    start(args.extract, args.add)