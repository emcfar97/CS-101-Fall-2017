import piexif, bs4, requests, re, tempfile, hashlib, ast
from . import ROOT, USER, EXT
from math import log
from io import BytesIO
from ffprobe import FFProbe
from imagehash import dhash
from progress.bar import IncrementalBar
from PIL import Image, UnidentifiedImageError, ImageFile
from cv2 import VideoCapture, imencode, cvtColor, COLOR_BGR2RGB

ImageFile.LOAD_TRUNCATED_IMAGES = True
PATH = USER / r'Dropbox\ん'
RESIZE = [1320, 1000]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }

METADATA = {
    'audio':'audio|has_audio',
    '3d_cg': '3d',
    'game_cg':'game_cg',
    'official_art':'official_art',
    'novel_illustration':'novel_illustration',
    'nude_filter':'nude_filter',
    'screen_capture':'screencap',
    }
GENERAL = {
    'age_difference': 'age_difference|teenage_girl_and_younger_boy',
    'bottomless': 'bottomless AND NOT (topless OR nude)', 
    'cowgirl_position': '(cowgirl_position OR reverse_cowgirl_position) AND sex', 
    'cum': 'cum|precum|semen|cumdrip|cum_in_mouth|cum_in_container|cum_in_pussy|cum_in_ass|cum_in_nipple|cum_on_feet|cum_on_body|cum_on_upper_body|cum_on_breasts|semen',
    'censored': 'mosaic_censor|blur_censor|bar_censor|novelty_censor',
    'dancing': 'dancing|dancer', 
    'gesugao': 'crazy_smile|crazy_eyes|gesugao', 
    'girl_on_top': 'girl_on_top AND sex',
    'japanese_clothes': 'yamakasa|tabi|sarashi|fundoshi|hakama|short_yukata|yukata|short_kimono|kimono|geta|happi|zori',
    'male_focus': '(male_focus OR (solo AND 1boy) OR (1boy AND NOT (1girl OR 2girls OR 3girls OR multiple_girls)))',
    'mature': '(large_areolae OR plump OR fat OR belly) AND (sagging_breasts OR veiny_breasts) OR milf',
    'muscular': '(solo OR (1girl AND NOT (1boy OR 2boys OR 3boys OR multiple_boys))) AND (muscular OR muscle OR muscular_female OR abs)', 
    'nude': 'nude AND NOT functionally_nude',
    'functionally_nude': '(functionally_nude OR (bottomless AND topless)) AND NOT nude', 
    'open_clothes': 'open_clothes|open_coat|open_jacket|open_shirt|open_robe|open_kimono|open_fly|open_shorts', 
    'oral': 'fellatio|cunnilingus|blowjob',
    'orgasm': 'orgasm|ejaculation', 
    'piercing': 'piercings|earrings|navel_piercings|areola_piercing|back_piercing|navel_piercing|nipple_piercing|ear_piercing|eyebrow_piercing|eyelid_piercing|lip_piercing|nose_piercing|tongue_piercing|clitoris_piercing|labia_piercing|penis_piercing|testicle_piercing|nipple_chain|linked_piercing', 
    'presenting': 'presenting OR top-down_bottom-up OR ((spread_legs OR spread_pussy) AND (trembling OR (heavy_breathing OR breath) OR (parted_lips AND NOT clenched_teeth))) OR spread_pussy', 
    'pussy': 'pussy|vagina|shaved_pussy', 
    'pussy_juice': 'pussy_juice|pussy_juices|pussy_juice_trail|pussy_juice_puddle|pussy_juice_stain|pussy_juice_drip_through_clothes', 
    'revealing_clothes': 'revealing_clothes|torn_clothes|micro_bikini|crop_top|pussy_peek|midriff|cleavage_cutout|wardrobe_malfunction|breast_slip|nipple_slip|areola_slip|no_panties|no_bra|pelvic_curtain|side_slit|breasts_outside|see-through|partially_visible_vulva|functionally_nude|breastless_clothes|bare_shoulders|one_breast_out',
    'sex': '(sex OR aftersex OR vaginal OR anal OR oral OR fellatio OR cunnilingus OR blowjob OR handjob OR frottage OR tribadism OR group_sex OR hetero OR yaoi OR yuri OR clothed_sex OR paizuri) AND NOT solo', 
    'sex_toy': 'sex_toys|vibrator|dildo|butt_plug|artificial_vagina',
    # 'solo': 'solo OR (1girl AND NOT (1boy OR 2boys OR 3boys OR multiple_boys)) OR (1boy AND NOT (1girl OR 2girls OR 3girls OR multiple_girls) OR NOT sex)', 
    'standing_sex': '(standing_on_one_leg OR (standing AND (leg_up OR leg_lift))) AND sex',
    'sportswear': 'sports_bra|yoga_pants',
    'suggestive': 'sexually_suggestive OR (naughty_smile OR fellatio_gesture OR teasing OR blush OR spread_legs OR pulled_by_self OR lifted_by_self OR (come_hither OR beckoning) OR (tongue_out AND (open_mouth OR licking_lips)) OR (bent_over AND (looking_back OR looking_at_viewer)) OR (trembling OR (saliva OR sweat) OR ((heavy_breathing OR breath) OR (parted_lips AND NOT clenched_teeth))) OR (skirt_lift OR bra_lift OR dress_lift OR shirt_lift OR wind_lift OR breast_lift OR kimono_pull) AND NOT (vaginal OR anal OR sex OR erection OR aftersex OR ejaculation OR pussy OR penis))', 
    'suspended_congress': '(suspended_congress OR reverse_suspended_congress) AND sex',
    'topless': 'topless AND bare_shoulders AND NOT (bottomless OR nude)', 
    'underwear': 'underwear|panties|bra|briefs',
    }
CUSTOM = {
    'naked_clothes': 'naked_apron|naked_belt|naked_bandage|naked_cape|naked_cloak|naked_overalls|naked_ribbon|naked_robe|naked_shirt', 
    'aphorisms': '((((nipples OR nipple_slip OR areolae OR areola_slip OR breasts_outside OR no_bra OR pasties) OR (no_panties OR pussy OR penis OR no_underwear))) AND ((bare_shoulders OR breast_cutout OR breastless_clothes OR breast_curtain OR capelet OR cape OR corset OR halter_neck OR open_jacket OR sash OR shawl OR shrug_<clothing> OR underboob OR underbust OR o_ring_top) OR (belt OR corset OR dress OR japanese_clothes OR loincloth OR pelvic_curtain OR sarong OR sash OR skirt OR showgirl_skirt OR side_slit OR tabard))) OR (condom_belt OR leggings OR thighhighs OR thigh_boots) OR naked_clothes OR amazon_position OR nipple_chain OR belly_chain OR femboy',
    'clothes_lift': 'clothes_lift|skirt_lift|shirt_lift|dress_lift|sweater_lift|bra_lift|bikini_lift|kimino_lift|apron_lift',
    'hand_expression': 'lactation AND (grabbing OR grabbing_own_breasts)',
    'leaning': 'leaning|leaning_forward|leaning_back|leaning_on_object|leaning_on_table|leaning_on_rail',
    'loops': 'loops|thigh_strap|necklace|neck_ring|anklet|bracelet|armlet',  
    'pokies': 'nipples_visible_through_clothes',
    }
RATING = {
    3: 'sex|aftersex|hetero|vaginal|anal|anus|cum|penis|vagina|pussy|pussy_juice|vaginal_juices|spread_pussy|erection|clitoris|anus|oral|fellatio|fingering|handjob|masturbation|object_insertion', 
    2: 'NOT (sex OR aftersex OR hetero OR vaginal OR anal OR anus OR cum OR penis OR vagina OR pussy OR pussy_juice OR vaginal_juices OR spread_pussy OR erection OR clitoris OR anus OR oral OR fellatio OR fingering OR handjob OR masturbation OR object_insertion) AND (nipples OR areola OR areolae OR covered_nipples OR cameltoe OR wedgie OR torn_clothes OR pubic_hair OR topless OR bottomless OR sexually_suggestive OR nude OR wet_panties OR no_panties OR spanking OR bondage OR vore OR bdsm OR open_clothes OR revealing_clothes OR breast_slip OR areoala_slip OR spread_ass OR orgasm OR vibrator OR sex_toy OR bulge OR lactation OR panty_pull OR panties_around_leg OR panties_removed OR partially_visible_vulva OR breast_sucking OR birth OR naked_clothes OR used_condom OR (suggestive AND (blush AND (spread_legs OR undressing OR erect_nipples OR ((miniskirt OR microskirt) AND underwear) OR (clothes_lift AND underwear)))))',
    1: 'NOT (sex OR aftersex OR hetero OR vaginal OR anal OR anus OR cum OR penis OR vagina OR pussy OR pussy_juice OR vaginal_juices OR spread_pussy OR erection OR clitoris OR anus OR oral OR fellatio OR fingering OR handjob OR masturbation OR object_insertion OR nipples OR areola OR areolae OR covered_nipples OR cameltoe OR wedgie OR torn_clothes OR pubic_hair OR topless OR bottomless OR sexually_suggestive OR nude OR wet_panties OR no_panties OR spanking OR bondage OR vore OR bdsm OR open_clothes OR revealing_clothes OR breast_slip OR areoala_slip OR spread_ass OR orgasm OR vibrator OR sex_toy OR bulge OR lactation OR panty_pull OR panties_around_leg OR panties_removed OR partially_visible_vulva OR breast_sucking OR birth OR naked_clothes OR used_condom OR (suggestive AND (blush AND (spread_legs OR undressing OR erect_nipples OR ((miniskirt OR microskirt) AND underwear) OR (clothes_lift AND underwear)))))'
    }
ARTIST = {
    '774': ['774_(nanashi)', 0],
    'initial-g': ['a1', 0],
    'ぁぁぁぁ': ['aaaa_(quad-a)', 0],
    'aaaa': ['aaaa_(quad-a)', 0],
    'あぶぶ@凍結解除されたよ': ['abubu', 0],
    'あぶぶ＠復旧率069_162': ['abubu', 0],
    'afrobull': ['afrobull', -1],
    'ryoagawa': ['agawa_ryou', 0],
    'akchu': ['akchu', -1],
    'ringoya_(alp)': ['alp', 0],
    'aomori': ['aomori', 1],
    'ばん!': ['ban', -1],
    'bigdeadalive': ['bigdead93', 1],
    'bow': ['bow_(bhp)', 0],
    'crescentia': ['crescentia', -1],
    'nayuru': ['crescentia', -1],
    'ドウモウ_doumou': ['doumou', 0],
    'uejini': ['gashi-gashi', -1],
    'gray_eggs_n_ham': ['gray_eggs_n_ham', 1],
    'graydoodles_': ['gray_eggs_n_ham', 1],
    'enigmagyaru': ['gyarusatan', 1],
    'gyarusatan': ['gyarusatan', 1],
    'hara': ['hara_(harayutaka)', 0],
    'へら': ['hara_(harayutaka)', 0],
    'ichan': ['ignition_crisis', 0],
    'iskra': ['iskra', 1],
    'ittla': ['ittla', 1],
    'kimjunho': ['jjanda', 0],
    'jjuneジュン': ['jjune', 0],
    'kajin': ['kajin_(kajinman)', 1],
    'kon_kit': ['konkitto', 0],
    'ryuun_(stiil)': ['konoshige_(ryuun)', 0],
    '0lightsource': ['lightsource', -1],
    'lmsketch': ['lm_(legoman)', 1],
    '【丁髷帝国】まげきち': ['magekichi', -1],
    'kinucakes': ['mariel_cartwright', -1],
    'mucha': ['mucha_(muchakai)', 0],
    'mutyakai': ['mucha_(muchakai)', 0],
    'mukka': ['mukka', -1],
    'なまにくatK（あったかい）': ['namaniku_atk', -1],
    'ななひめ': ['nanahime', -1],
    '♣3': ['nanaya_(daaijianglin)', 0],
    '♣3@金曜日西り02a': ['nanaya_(daaijianglin)', 0],
    'thiccwithaq': ['nyantcha', 0],
    'にの子': ['ninoko', -1],
    'xin&obiwan': ['obiwan', 0],
    'xin&obiコミ1a11ab': ['obiwan', 0],
    'xin&obi月曜日れ34a': ['obiwan', 0],
    'xin&obi月曜日れ34ab': ['obiwan', 0],
    'typo_(requiemdusk)': ['optionaltypo', 1],
    'owler': ['owler', 1],
    'personal_ami': ['personalami', 1],
    'otmm': ['redrop', 0],
    'otsumami': ['redrop', 0],
    'redrop_おつまみ': ['redrop', 0],
    'rtil': ['rtil', 1],
    'xtilxtil': ['rtil', 1],
    'saitom': ['saitou_masatsugu', -1],
    'seinen': ['seinen', -1],
    'laminaria':['shiokonbu', 0],
    'laminaria_(shiokonbu)':['shiokonbu', 0],
    'nekofondue': ['soduki', -1],
    'splash_brush': ['splashbrush'],
    'splashbrush': ['splashbrush'],
    'stormcow': ['stormcow', -1],
    'sue': ['suertee34', -1],
    'arctic char': ['tabata_hisayuki', -1],
    'arcticchar': ['tabata_hisayuki', -1],
    'てだいん': ['tedain', -1],
    'tetisuka': ['tetisuka', -1],
    'tetsu': ['tetsu_(kimuchi)', 0],
    'てつお': ['tetsuo_(tetuo1129)', -1],
    'tofuubear': ['tofuubear', -1],
    'tukudani01': ['tsukudani', 0],
    'tsukiwani': ['tsukiwani', 0],
    'watatanza': ['watatanza', -1],
    'crimeglass': ['x-t3al2', -1],
    'yd': ['yang-do', 0],
    'yd@4日目西a': ['yang-do', 0],
    'zako': ['zako_(arvinry)', -1],
    'paul_kwon': ['zeronis', -1],
    'puu_no_puupuupuu': ['zeroshiki_kouichi', 1],
    'puuzaki_puuna': ['zeroshiki_kouichi', 1],
    'zheng': ['zheng', 0],
    'ぞんだ': ['zonda', -1],
    }
REMOVE = {
    '3d', 'photorealistic', 'realistic', 'photo', 'blurry',
    'cum', 'cum_in_pussy', 'pov', 'solo',
    'blurry', 'blurry_foreground', 'blurry_background',
    'sex', 'after_sex', 'sex_from_behind', 'vaginal', 'anal',
    'doggystyle', 'missionary', 'cowgirl_position', 'cowgirl', 'boy_on_top'
    'mosaic_censoring', 'censored', 'uncensored',
    'male_focus', 'multiple_boys', 'multiple_girls', 
    'pantyhose', 'no_humans', 'scenery', 'asian', 'what'
    'animal_ears', 'slut'
    }
REPLACE = {
    '3d': '3d_cg',
    '69':'69_position',
    '[4-9]boys': 'multiple_boys',
    '[4-9]girls': 'multiple_girls',
    'animate.*_gif': 'animated',
    'anal_object_insertion':'anal object_insertion',
    'anal_masturbation|penile_masturbation|vaginal_masturbation': 'masturbation',
    'mosaic_censoring': 'mosaic_censor',
    'bar_censoring': 'bar_censor',
    'blur_censoring': 'blur_censor',
    'blowjob': 'fellatio',
    '(female|male)_pubic_hair': 'pubic_hair',
    '(female|male)_solo|solo_focus': 'solo',
    'insertion': 'object_insertion',
    'kissing':'kiss',
    'legs_spread|legs_apart': 'spread_legs',
    'female': '1girl',
    'male': '1boy',
    'mature_female': 'mature',
    'mostly_nude': 'functionally_nude',
    'muscle': 'muscular',
    'nipple_tweak':'nipple_tweaking',
    'no_pan': 'no_panties',
    'on_all_fours': 'all_fours',
    'oshiri': 'ass',
    'pantsu': 'panties',
    'plugsuit': 'bodysuit',
    '\w*pointed_ears': 'pointed_ears',
    'shaking':'trembling',
    'squatting_cowgirl_position': 'squatting cowgirl_position',
    'standing_sex': 'standing sex',
    'thigh_sex': 'intercrural',
    'vagina': 'pussy',
    'vaginal_object_insertion': 'vaginal object_insertion',
    'virgin|uncensored|nipples_visible_through_clothes|hetero|yuri|yaoi|excessive_.+|(fat|ugly|old)_man|object_insertion_from_behind|(rating|score):\w+': '',
    }

def save_image(name, image=None, exif=b''):
    '''Save image to name (with optional exif metadata)'''

    try:
        if re.search('jp.*g|png', name.suffix):

            if image.endswith('jpeg'): name = name.with_suffix('.jpg')
            if image:
                img = Image.open(BytesIO(
                        requests.get(image, headers=HEADERS).content
                    ))
                img.thumbnail(RESIZE)
            else: img = Image.open(name)
            img.save(name, exif=exif)

        elif re.search('gif|webm|mp4', name.suffix):
            
            name.write_bytes(
                requests.get(image, headers=HEADERS, stream=True).content
                )
    
    except UnidentifiedImageError: return False
    except OSError as error:
        if 'trunc' not in error.args:
            try: img.save(name.with_suffix('.gif'))
            except: pass
    except: pass
    return name.exists()

def get_name(path, hasher=1):
    '''Return pathname (from optional hash of image)'''
    
    stem = path

    if hasher:
        if isinstance(path, str):
            data = requests.get(path, headers=HEADERS).content
        else: data = path.read_bytes()
        hasher = hashlib.md5(data)

        stem = f'{hasher.hexdigest()}.{re.findall(EXT, str(path), re.IGNORECASE)[0]}'
    
    return PATH / stem[0:2] / stem[2:4] / stem.lower().replace('jpeg','jpg')

def get_hash(image, src=False):
    '''Return perceptual hash of image'''
        
    if src:
        
        try:
            image = Image.open(
                BytesIO(requests.get(image, headers=HEADERS).content)
                )
        except: return None
    
    elif re.search('jp.*g|png|gif', image.suffix, re.IGNORECASE): 
        
        try: image = Image.open(image)
        except: return None

    elif re.search('webm|mp4', image.suffix, re.IGNORECASE):
        
        try:
            video_capture = VideoCapture(str(image)).read()[-1]
            image = cvtColor(video_capture, COLOR_BGR2RGB)
            image = Image.fromarray(image)
        except: return None
    
    image.thumbnail([32, 32])
    image = image.convert('L')

    return f'{dhash(image)}'

def get_tags(driver, path, filter=False):

    tags = set()
    frames = []
    video = path.suffix in ('.gif', '.webm', '.mp4')

    if video:

        tags.add('animated')
        if path.suffix in ('.webm', '.mp4'):
            try:
                for stream in FFProbe(str(path)).streams:
                    if stream.codec_type == 'audio': 
                        tags.add('audio')
                        break
            except: pass
        temp_dir = tempfile.TemporaryDirectory()
        vidcap = VideoCapture(str(path))
        success, frame = vidcap.read()
 
        while success:
            
            temp = ROOT.parent / temp_dir.name / f'{next(tempfile._get_candidate_names())}.jpg'
            temp.write_bytes(imencode('.jpg', frame)[-1])
            frames.append(temp)
            success, frame = vidcap.read()

        else:
            step = 90 * log((len(frames) * .002) + 1) + 1
            frames = frames[::round(step)]
    
    else: frames.append(path)
    
    for frame in frames:

        driver.get('http://dev.kanotype.net:8003/deepdanbooru/')
        driver.find('//*[@id="exampleFormControlFile1"]', str(frame))
        driver.find('//button[@type="submit"]', click=True)

        for _ in range(4):
            html = bs4.BeautifulSoup(driver.page_source(), 'lxml')
            try:
                tags.update([
                    tag.text for tag in html.find('tbody').findAll(href=True)
                    ])
                break
            except AttributeError:
                if driver.current_url().endswith('deepdanbooru/'):
                    driver.find('//*[@id="exampleFormControlFile1"]',str(frame))
                    driver.find('//button[@type="submit"]', click=True)
                driver.refresh()
    
    else:
        if video: temp_dir.cleanup()
        if filter: tags.difference_update(REMOVE)
    
    return ' '.join(tags)

def generate_tags(general, metadata=0, custom=0, artists=[], rating=0, exif=1):
    
    tags = ['qwd']

    if general:
        
        tags.extend(
            key for key in GENERAL if evaluate(general, GENERAL[key])
            )
    if metadata:
        
        tags.extend(
            key for key in METADATA if evaluate(metadata, METADATA[key])
            )
    if custom:
        
        tags.extend(
            key for key in CUSTOM if evaluate(general, CUSTOM[key])
            )
    if rating:
        
        tags = set(tags + general.split())
        rating = [
            key for key in RATING if evaluate(
                f' {" ".join(tags)} ', RATING[key]
                )
            ]
    
    if exif:
        
        custom = tags.copy()
        custom.remove('qwd')
        
        zeroth_ifd = {
            piexif.ImageIFD.XPKeywords: [
                byte for char in '; '.join(custom) 
                for byte in [ord(char), 0]
                if 0 <= byte <= 255
                ],
            piexif.ImageIFD.XPAuthor: [
                byte for char in '; '.join(artists) 
                for byte in [ord(char), 0]
                if 0 <= byte <= 255
                ]
            }
        exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u'2000:1:1 00:00:00'}
        
        exif = piexif.dump({"0th":zeroth_ifd, "Exif":exif_ifd})
        rating.append(exif)
    
    tags = " ".join(tags)
    for key, value in REPLACE.items():
        tags = re.sub(f' {key} ', f' {value} ', tags)
    else: tags = tags.replace('-', '_')

    return [tags] + rating if rating else tags

def evaluate(tags, pattern):
    
    if re.search('AND|OR|NOT', pattern):
        query = tuple(pattern.replace('(', '( ').replace(')', ' )').split(' '))
        query = str(query).replace("'(',", '(').replace(", ')'", ')')
        query = query.replace('<','(').replace('>',')')
        # query = re.sub('(\w+)', r'"\1",', pattern)
        # query = re.sub('(\([^(\([^()]*\))]*\))', r'\1,', query)
        # # query = re.sub('([))])', '),),', query)
        query = ast.literal_eval(query)
                
        return parse(tags.split(), query)

    else: return re.search(f' ({pattern}) ', tags)

def parse(tags, search):
    
    if (len(search) == 1) and isinstance(search[0], tuple): search, = search
    
    elif all(op not in search for op in ['AND','OR','NOT']):
        if isinstance(search, str): return search in tags
        else: return search[0] in tags

    if 'AND' in search: 
        num = search.index('AND')
        return parse(tags, search[:num]) and parse(tags,search[num+1:])
    
    elif 'OR' in search: 
        num = search.index('OR')
        return parse(tags, search[:num]) or parse(tags, search[num+1:])
    
    elif 'NOT' in search: return not parse(tags, search[1])