"""
Script 20: Generate Christian and African Names
Hedef:
- Christianity: 400K ek kayıt (Avrupa, Afrika, Amerika, Asya)
- Afrika kıtası genişletme: 200K+ kayıt
"""

import json
import random
from pathlib import Path

OUTPUT_DIR = Path("data/synthetic")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# CHRISTIAN İSİMLERİ - AVRUPA
# =============================================================================

CHRISTIAN_FIRST_NAMES_MALE_EUROPEAN = [
    # İngilizce
    'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph',
    'thomas', 'charles', 'christopher', 'daniel', 'matthew', 'anthony', 'mark', 'donald',
    'steven', 'paul', 'andrew', 'joshua', 'kenneth', 'kevin', 'brian', 'george', 'edward',
    'ronald', 'timothy', 'jason', 'jeffrey', 'ryan', 'jacob', 'gary', 'nicholas', 'eric',
    'jonathan', 'stephen', 'larry', 'justin', 'scott', 'brandon', 'benjamin', 'samuel',
    'frank', 'gregory', 'raymond', 'alexander', 'patrick', 'jack', 'dennis', 'jerry',
    # Almanca
    'hans', 'peter', 'wolfgang', 'klaus', 'jürgen', 'dieter', 'horst', 'werner', 'gerhard',
    'bernd', 'michael', 'thomas', 'andreas', 'christian', 'stefan', 'martin', 'matthias',
    'frank', 'rainer', 'jörg', 'manfred', 'helmut', 'otto', 'friedrich', 'karl', 'heinrich',
    # Fransızca
    'jean', 'pierre', 'michel', 'andré', 'philippe', 'alain', 'bernard', 'christian',
    'claude', 'daniel', 'pascal', 'olivier', 'jacques', 'françois', 'laurent', 'thierry',
    'nicolas', 'matthieu', 'julien', 'guillaume', 'antoine', 'christophe', 'sébastien',
    # İspanyolca
    'jose', 'juan', 'carlos', 'luis', 'miguel', 'pedro', 'francisco', 'antonio', 'manuel',
    'javier', 'fernando', 'jorge', 'rafael', 'alberto', 'sergio', 'pablo', 'ricardo',
    'ramon', 'eduardo', 'roberto', 'diego', 'daniel', 'raul', 'alvaro', 'gabriel',
    # İtalyanca
    'giuseppe', 'giovanni', 'antonio', 'mario', 'francesco', 'angelo', 'vincenzo', 'pietro',
    'salvatore', 'lorenzo', 'carlo', 'franco', 'andrea', 'stefano', 'paolo', 'marco',
    'giorgio', 'roberto', 'luca', 'alessandro', 'matteo', 'davide', 'simone', 'federico',
    # Portekizce
    'joao', 'jose', 'antonio', 'manuel', 'carlos', 'luis', 'paulo', 'pedro', 'francisco',
    'fernando', 'miguel', 'ricardo', 'rafael', 'bruno', 'tiago', 'andre', 'daniel',
    # Rusça
    'alexander', 'sergey', 'dmitry', 'andrey', 'alexey', 'vladimir', 'nikolay', 'ivan',
    'mikhail', 'maxim', 'evgeny', 'artem', 'pavel', 'oleg', 'anton', 'denis', 'roman',
    # Lehçe
    'jan', 'andrzej', 'piotr', 'krzysztof', 'stanislaw', 'tomasz', 'pawel', 'jozef',
    'marcin', 'marek', 'michal', 'grzegorz', 'jerzy', 'tadeusz', 'adam', 'lukasz',
    # Hollandaca
    'jan', 'piet', 'kees', 'henk', 'willem', 'gerard', 'hans', 'pieter', 'johan',
    'cornelis', 'adrianus', 'antonius', 'johannes', 'jacobus', 'franciscus',
    # İskandinav
    'lars', 'anders', 'erik', 'ole', 'per', 'nils', 'bjorn', 'sven', 'hans', 'karl',
    'johan', 'magnus', 'henrik', 'mikael', 'christian', 'martin', 'thomas', 'jakob'
]

CHRISTIAN_FIRST_NAMES_FEMALE_EUROPEAN = [
    # İngilizce
    'mary', 'patricia', 'jennifer', 'linda', 'barbara', 'elizabeth', 'susan', 'jessica',
    'sarah', 'karen', 'nancy', 'lisa', 'betty', 'margaret', 'sandra', 'ashley', 'dorothy',
    'kimberly', 'emily', 'donna', 'michelle', 'carol', 'amanda', 'melissa', 'deborah',
    'stephanie', 'rebecca', 'sharon', 'laura', 'cynthia', 'kathleen', 'amy', 'shirley',
    'angela', 'helen', 'anna', 'brenda', 'pamela', 'nicole', 'emma', 'samantha', 'katherine',
    # Almanca
    'ursula', 'maria', 'karin', 'monika', 'petra', 'birgit', 'sabine', 'andrea', 'martina',
    'christine', 'angelika', 'susanne', 'gabriele', 'katrin', 'stefanie', 'julia', 'nicole',
    'claudia', 'barbara', 'elisabeth', 'heike', 'inge', 'anna', 'margit', 'christa',
    # Fransızca
    'marie', 'nathalie', 'isabelle', 'sylvie', 'catherine', 'françoise', 'christine',
    'monique', 'sophie', 'nicole', 'martine', 'brigitte', 'anne', 'dominique', 'véronique',
    'chantal', 'sandrine', 'stephanie', 'valerie', 'aurelie', 'celine', 'claire', 'camille',
    # İspanyolca
    'maria', 'carmen', 'josefa', 'isabel', 'dolores', 'pilar', 'teresa', 'ana', 'francisca',
    'laura', 'antonia', 'mercedes', 'cristina', 'marta', 'rosa', 'lucia', 'paula', 'elena',
    'beatriz', 'raquel', 'patricia', 'monica', 'sandra', 'marina', 'andrea', 'silvia',
    # İtalyanca
    'maria', 'anna', 'giuseppina', 'rosa', 'angela', 'giovanna', 'teresa', 'lucia',
    'carmela', 'francesca', 'antonia', 'caterina', 'elisabetta', 'rita', 'paola', 'laura',
    'sara', 'chiara', 'alessandra', 'valentina', 'federica', 'giulia', 'martina', 'silvia',
    # Portekizce
    'maria', 'ana', 'francisca', 'antonia', 'manuela', 'isabel', 'fernanda', 'carolina',
    'juliana', 'beatriz', 'ines', 'mariana', 'rita', 'joana', 'catarina', 'patricia',
    # Rusça
    'maria', 'anna', 'elena', 'olga', 'tatiana', 'natalia', 'irina', 'ekaterina',
    'svetlana', 'ludmila', 'galina', 'marina', 'valentina', 'yulia', 'anastasia', 'victoria',
    # Lehçe
    'maria', 'anna', 'katarzyna', 'malgorzata', 'agnieszka', 'barbara', 'krystyna',
    'ewa', 'elzbieta', 'zofia', 'janina', 'teresa', 'magdalena', 'monika', 'joanna',
    # Hollandaca
    'maria', 'anna', 'johanna', 'cornelia', 'hendrika', 'wilhelmina', 'elisabeth',
    'geertruida', 'marinus', 'helena', 'sophia', 'catharina', 'adriana', 'petra',
    # İskandinav
    'anna', 'maria', 'karin', 'eva', 'kristina', 'birgitta', 'elisabeth', 'margareta',
    'ingrid', 'lena', 'emma', 'sara', 'helena', 'linnea', 'maja', 'ida', 'elin'
]

CHRISTIAN_LAST_NAMES_EUROPEAN = [
    # İngilizce
    'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis',
    'rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez', 'wilson', 'anderson',
    'thomas', 'taylor', 'moore', 'jackson', 'martin', 'lee', 'thompson', 'white',
    'harris', 'clark', 'lewis', 'robinson', 'walker', 'hall', 'allen', 'young',
    # Almanca
    'müller', 'schmidt', 'schneider', 'fischer', 'weber', 'meyer', 'wagner', 'becker',
    'schulz', 'hoffmann', 'schäfer', 'koch', 'bauer', 'richter', 'klein', 'wolf',
    'schröder', 'neumann', 'schwarz', 'zimmermann', 'braun', 'krüger', 'hartmann',
    # Fransızca
    'martin', 'bernard', 'dubois', 'thomas', 'robert', 'richard', 'petit', 'durand',
    'leroy', 'moreau', 'simon', 'laurent', 'lefebvre', 'michel', 'garcia', 'david',
    'bertrand', 'roux', 'vincent', 'fournier', 'morel', 'girard', 'andre', 'mercier',
    # İspanyolca
    'garcia', 'rodriguez', 'martinez', 'lopez', 'gonzalez', 'perez', 'sanchez', 'ramirez',
    'torres', 'flores', 'rivera', 'gomez', 'diaz', 'cruz', 'morales', 'reyes', 'jimenez',
    'hernandez', 'ruiz', 'alvarez', 'castillo', 'romero', 'gutierrez', 'fernandez',
    # İtalyanca
    'rossi', 'russo', 'ferrari', 'esposito', 'bianchi', 'romano', 'colombo', 'ricci',
    'marino', 'greco', 'bruno', 'gallo', 'conti', 'de luca', 'costa', 'giordano',
    'mancini', 'rizzo', 'lombardi', 'moretti', 'barbieri', 'fontana', 'santoro',
    # Portekizce
    'silva', 'santos', 'ferreira', 'oliveira', 'costa', 'rodrigues', 'martins', 'jesus',
    'sousa', 'fernandes', 'goncalves', 'gomes', 'lopes', 'marques', 'alves', 'pereira',
    # Rusça
    'ivanov', 'smirnov', 'kuznetsov', 'popov', 'sokolov', 'lebedev', 'kozlov', 'novikov',
    'morozov', 'petrov', 'volkov', 'solovyov', 'vasilyev', 'zaytsev', 'pavlov', 'semyonov',
    # Lehçe
    'nowak', 'kowalski', 'wisniewski', 'wojcik', 'kowalczyk', 'kaminski', 'lewandowski',
    'zielinski', 'szymanski', 'wozniak', 'dabrowski', 'mazur', 'krawczyk', 'krol',
    # Hollandaca
    'de jong', 'jansen', 'de vries', 'van den berg', 'van dijk', 'bakker', 'janssen',
    'visser', 'smit', 'meijer', 'de boer', 'mulder', 'de groot', 'bos', 'vos',
    # İskandinav
    'johansson', 'andersson', 'karlsson', 'nilsson', 'eriksson', 'larsson', 'olsson',
    'persson', 'svensson', 'gustafsson', 'pettersson', 'jonsson', 'jansson', 'hansson'
]

# =============================================================================
# AFRİKA İSİMLERİ
# =============================================================================

AFRICAN_FIRST_NAMES_MALE = [
    # Batı Afrika (Nijerya, Gana, Senegal)
    'kwame', 'kofi', 'yaw', 'kojo', 'kwesi', 'kwaku', 'kwabena', 'aba', 'ama', 'akua',
    'adwoa', 'abena', 'afia', 'esi', 'chidi', 'chinedu', 'chibueze', 'chukwudi', 'emeka',
    'ikechukwu', 'obinna', 'uchenna', 'adebayo', 'abiola', 'babatunde', 'oluwaseun',
    'oluwatobi', 'olamide', 'segun', 'tunde', 'femi', 'kola', 'ayo', 'dele',
    # Doğu Afrika (Kenya, Tanzania, Uganda, Etiyopya)
    'kipchoge', 'kiprop', 'kipruto', 'kimani', 'kamau', 'mwangi', 'njoroge', 'otieno',
    'ochieng', 'owino', 'juma', 'rashidi', 'said', 'salim', 'hamisi', 'habib',
    'abebe', 'bekele', 'gebre', 'haile', 'tesfaye', 'yohannes', 'dawit', 'daniel',
    # Güney Afrika
    'thabo', 'sipho', 'mandla', 'bongani', 'sello', 'kgosi', 'lerato', 'tshepo',
    'jacob', 'pieter', 'johannes', 'andries', 'francois', 'hendrik', 'willem',
    # Kuzey Afrika (Mısır, Sudan)
    'mohamed', 'ahmed', 'ali', 'omar', 'hassan', 'ibrahim', 'youssef', 'mahmoud',
    'mustafa', 'said', 'khaled', 'abdullah', 'amr', 'tarek', 'karim', 'hossam'
]

AFRICAN_FIRST_NAMES_FEMALE = [
    # Batı Afrika
    'ama', 'akua', 'adwoa', 'abena', 'afia', 'esi', 'yaa', 'efua', 'aku', 'adjoa',
    'ada', 'amara', 'chioma', 'chinwe', 'ngozi', 'nneka', 'ify', 'chiamaka', 'ebere',
    'adanna', 'folake', 'omolara', 'titi', 'funke', 'bisi', 'yemi', 'nike', 'adenike',
    # Doğu Afrika
    'wanjiru', 'njeri', 'wairimu', 'wambui', 'nyambura', 'mumbi', 'wangari', 'atieno',
    'akinyi', 'adhiambo', 'awino', 'amina', 'fatuma', 'halima', 'mariam', 'zainab',
    'bethlehem', 'eden', 'ruth', 'sara', 'hana', 'mekdes', 'tigist', 'seble',
    # Güney Afrika
    'nomsa', 'thandi', 'zanele', 'nokuthula', 'precious', 'busisiwe', 'zinhle', 'ntombi',
    'annika', 'mieke', 'elsie', 'sannie', 'elizabeth', 'maria', 'johanna',
    # Kuzey Afrika
    'fatma', 'aisha', 'mariam', 'nour', 'salma', 'heba', 'yasmin', 'aya', 'nada',
    'dina', 'rana', 'hana', 'malak', 'farida', 'layla', 'sarah', 'mona'
]

AFRICAN_LAST_NAMES = [
    # Nijerya
    'adebayo', 'okonkwo', 'okoro', 'okafor', 'nwankwo', 'eze', 'chukwu', 'ojo', 'williams',
    'johnson', 'oluwole', 'adeleke', 'balogun', 'afolabi', 'adeyemi', 'adekunle', 'adeola',
    # Gana
    'mensah', 'boateng', 'asante', 'owusu', 'appiah', 'agyeman', 'osei', 'antwi', 'agyei',
    # Kenya
    'kamau', 'mwangi', 'njoroge', 'kariuki', 'kimani', 'gitau', 'wanjiku', 'otieno', 'odhiambo',
    'omondi', 'owino', 'mutua', 'musyoka', 'muturi', 'kibet', 'kipchoge', 'rotich',
    # Tanzania
    'rashid', 'hussein', 'abdallah', 'juma', 'said', 'hassan', 'salim', 'hamisi', 'mwita',
    # Güney Afrika
    'ngubane', 'nkosi', 'dlamini', 'mahlangu', 'mokoena', 'molefe', 'modise', 'khumalo',
    'van der merwe', 'botha', 'pretorius', 'van wyk', 'steyn', 'du plessis', 'fourie',
    # Etiyopya
    'tesfaye', 'bekele', 'abebe', 'gebre', 'haile', 'desta', 'tadesse', 'alemu', 'wolde',
    # Mısır
    'mohamed', 'ahmed', 'ali', 'hassan', 'ibrahim', 'abdel', 'said', 'fahmy', 'sayed'
]

AFRICAN_COUNTRIES = {
    # Batı Afrika
    'NGA': ('Nigeria', 'English', 'Africa', 'Christianity'),
    'GHA': ('Ghana', 'English', 'Africa', 'Christianity'),
    'SEN': ('Senegal', 'French', 'Africa', 'Islam'),
    'MLI': ('Mali', 'French', 'Africa', 'Islam'),
    'CIV': ('Ivory Coast', 'French', 'Africa', 'Christianity'),
    'BFA': ('Burkina Faso', 'French', 'Africa', 'Islam'),
    'NER': ('Niger', 'French', 'Africa', 'Islam'),
    'TGO': ('Togo', 'French', 'Africa', 'Christianity'),
    'BEN': ('Benin', 'French', 'Africa', 'Christianity'),
    'GMB': ('Gambia', 'English', 'Africa', 'Islam'),
    'GNB': ('Guinea-Bissau', 'Portuguese', 'Africa', 'Islam'),
    'GIN': ('Guinea', 'French', 'Africa', 'Islam'),
    'SLE': ('Sierra Leone', 'English', 'Africa', 'Islam'),
    'LBR': ('Liberia', 'English', 'Africa', 'Christianity'),
    # Doğu Afrika
    'KEN': ('Kenya', 'Swahili', 'Africa', 'Christianity'),
    'TZA': ('Tanzania', 'Swahili', 'Africa', 'Christianity'),
    'UGA': ('Uganda', 'English', 'Africa', 'Christianity'),
    'RWA': ('Rwanda', 'Kinyarwanda', 'Africa', 'Christianity'),
    'BDI': ('Burundi', 'French', 'Africa', 'Christianity'),
    'ETH': ('Ethiopia', 'Amharic', 'Africa', 'Christianity'),
    'ERI': ('Eritrea', 'Tigrinya', 'Africa', 'Christianity'),
    'SOM': ('Somalia', 'Somali', 'Africa', 'Islam'),
    'DJI': ('Djibouti', 'French', 'Africa', 'Islam'),
    # Güney Afrika
    'ZAF': ('South Africa', 'English', 'Africa', 'Christianity'),
    'NAM': ('Namibia', 'English', 'Africa', 'Christianity'),
    'BWA': ('Botswana', 'English', 'Africa', 'Christianity'),
    'ZWE': ('Zimbabwe', 'English', 'Africa', 'Christianity'),
    'MOZ': ('Mozambique', 'Portuguese', 'Africa', 'Christianity'),
    'MWI': ('Malawi', 'English', 'Africa', 'Christianity'),
    'ZMB': ('Zambia', 'English', 'Africa', 'Christianity'),
    'AGO': ('Angola', 'Portuguese', 'Africa', 'Christianity'),
    'LSO': ('Lesotho', 'English', 'Africa', 'Christianity'),
    'SWZ': ('Eswatini', 'English', 'Africa', 'Christianity'),
    # Merkez Afrika
    'COD': ('DR Congo', 'French', 'Africa', 'Christianity'),
    'COG': ('Congo', 'French', 'Africa', 'Christianity'),
    'CAF': ('Central African Republic', 'French', 'Africa', 'Christianity'),
    'TCD': ('Chad', 'French', 'Africa', 'Islam'),
    'CMR': ('Cameroon', 'French', 'Africa', 'Christianity'),
    'GAB': ('Gabon', 'French', 'Africa', 'Christianity'),
    'GNQ': ('Equatorial Guinea', 'Spanish', 'Africa', 'Christianity'),
    # Kuzey Afrika
    'EGY': ('Egypt', 'Arabic', 'Africa', 'Islam'),
    'SDN': ('Sudan', 'Arabic', 'Africa', 'Islam'),
    'LBY': ('Libya', 'Arabic', 'Africa', 'Islam'),
    'TUN': ('Tunisia', 'Arabic', 'Africa', 'Islam'),
    'DZA': ('Algeria', 'Arabic', 'Africa', 'Islam'),
    'MAR': ('Morocco', 'Arabic', 'Africa', 'Islam'),
    'MRT': ('Mauritania', 'Arabic', 'Africa', 'Islam'),
}

CHRISTIAN_EUROPEAN_COUNTRIES = {
    # Batı Avrupa
    'GBR': ('United Kingdom', 'English', 'Europe'),
    'IRL': ('Ireland', 'English', 'Europe'),
    'FRA': ('France', 'French', 'Europe'),
    'DEU': ('Germany', 'German', 'Europe'),
    'NLD': ('Netherlands', 'Dutch', 'Europe'),
    'BEL': ('Belgium', 'French', 'Europe'),
    'LUX': ('Luxembourg', 'French', 'Europe'),
    'CHE': ('Switzerland', 'German', 'Europe'),
    'AUT': ('Austria', 'German', 'Europe'),
    # Güney Avrupa
    'ESP': ('Spain', 'Spanish', 'Europe'),
    'PRT': ('Portugal', 'Portuguese', 'Europe'),
    'ITA': ('Italy', 'Italian', 'Europe'),
    'GRC': ('Greece', 'Greek', 'Europe'),
    'MLT': ('Malta', 'English', 'Europe'),
    'AND': ('Andorra', 'Catalan', 'Europe'),
    'SMR': ('San Marino', 'Italian', 'Europe'),
    'VAT': ('Vatican City', 'Italian', 'Europe'),
    # Doğu Avrupa
    'POL': ('Poland', 'Polish', 'Europe'),
    'CZE': ('Czech Republic', 'Czech', 'Europe'),
    'SVK': ('Slovakia', 'Slovak', 'Europe'),
    'HUN': ('Hungary', 'Hungarian', 'Europe'),
    'ROU': ('Romania', 'Romanian', 'Europe'),
    'BGR': ('Bulgaria', 'Bulgarian', 'Europe'),
    'SRB': ('Serbia', 'Serbian', 'Europe'),
    'HRV': ('Croatia', 'Croatian', 'Europe'),
    'SVN': ('Slovenia', 'Slovenian', 'Europe'),
    'BIH': ('Bosnia and Herzegovina', 'Bosnian', 'Europe'),
    'MKD': ('North Macedonia', 'Macedonian', 'Europe'),
    'ALB': ('Albania', 'Albanian', 'Europe'),
    'MNE': ('Montenegro', 'Montenegrin', 'Europe'),
    # Kuzey Avrupa
    'SWE': ('Sweden', 'Swedish', 'Europe'),
    'NOR': ('Norway', 'Norwegian', 'Europe'),
    'DNK': ('Denmark', 'Danish', 'Europe'),
    'FIN': ('Finland', 'Finnish', 'Europe'),
    'ISL': ('Iceland', 'Icelandic', 'Europe'),
    # Doğu Avrupa (Slavic)
    'RUS': ('Russia', 'Russian', 'Europe'),
    'UKR': ('Ukraine', 'Ukrainian', 'Europe'),
    'BLR': ('Belarus', 'Belarusian', 'Europe'),
    'LTU': ('Lithuania', 'Lithuanian', 'Europe'),
    'LVA': ('Latvia', 'Latvian', 'Europe'),
    'EST': ('Estonia', 'Estonian', 'Europe'),
    # Amerika (Christian majority)
    'USA': ('United States', 'English', 'Americas'),
    'CAN': ('Canada', 'English', 'Americas'),
    'MEX': ('Mexico', 'Spanish', 'Americas'),
    'BRA': ('Brazil', 'Portuguese', 'Americas'),
    'ARG': ('Argentina', 'Spanish', 'Americas'),
    'CHL': ('Chile', 'Spanish', 'Americas'),
    'COL': ('Colombia', 'Spanish', 'Americas'),
    'PER': ('Peru', 'Spanish', 'Americas'),
    'VEN': ('Venezuela', 'Spanish', 'Americas'),
    'ECU': ('Ecuador', 'Spanish', 'Americas'),
}

def generate_christian_names(target_count):
    """Christian isimleri üret"""
    data = []
    male_count = target_count // 2
    female_count = target_count - male_count

    print(f"\nChristianity için {target_count:,} kayıt üretiliyor...")

    for i in range(male_count):
        first_name = random.choice(CHRISTIAN_FIRST_NAMES_MALE_EUROPEAN)
        last_name = random.choice(CHRISTIAN_LAST_NAMES_EUROPEAN)
        country_code, (country_name, language, region) = random.choice(list(CHRISTIAN_EUROPEAN_COUNTRIES.items()))

        data.append({
            'name': first_name,
            'name_type': 'first',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': 'Christianity',
            'gender': 'M',
            'source': 'synthetic'
        })

        data.append({
            'name': last_name,
            'name_type': 'last',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': 'Christianity',
            'gender': None,
            'source': 'synthetic'
        })

    for i in range(female_count):
        first_name = random.choice(CHRISTIAN_FIRST_NAMES_FEMALE_EUROPEAN)
        last_name = random.choice(CHRISTIAN_LAST_NAMES_EUROPEAN)
        country_code, (country_name, language, region) = random.choice(list(CHRISTIAN_EUROPEAN_COUNTRIES.items()))

        data.append({
            'name': first_name,
            'name_type': 'first',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': 'Christianity',
            'gender': 'F',
            'source': 'synthetic'
        })

        data.append({
            'name': last_name,
            'name_type': 'last',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': 'Christianity',
            'gender': None,
            'source': 'synthetic'
        })

    return data

def generate_african_names(target_count):
    """Afrika isimleri üret"""
    data = []
    male_count = target_count // 2
    female_count = target_count - male_count

    print(f"\nAfrika kıtası için {target_count:,} kayıt üretiliyor...")

    for i in range(male_count):
        first_name = random.choice(AFRICAN_FIRST_NAMES_MALE)
        last_name = random.choice(AFRICAN_LAST_NAMES)
        country_code, (country_name, language, region, religion) = random.choice(list(AFRICAN_COUNTRIES.items()))

        data.append({
            'name': first_name,
            'name_type': 'first',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': religion,
            'gender': 'M',
            'source': 'synthetic'
        })

        data.append({
            'name': last_name,
            'name_type': 'last',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': religion,
            'gender': None,
            'source': 'synthetic'
        })

    for i in range(female_count):
        first_name = random.choice(AFRICAN_FIRST_NAMES_FEMALE)
        last_name = random.choice(AFRICAN_LAST_NAMES)
        country_code, (country_name, language, region, religion) = random.choice(list(AFRICAN_COUNTRIES.items()))

        data.append({
            'name': first_name,
            'name_type': 'first',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': religion,
            'gender': 'F',
            'source': 'synthetic'
        })

        data.append({
            'name': last_name,
            'name_type': 'last',
            'country_code': country_code,
            'region': region,
            'language': language,
            'religion': religion,
            'gender': None,
            'source': 'synthetic'
        })

    return data

def main():
    """Ana fonksiyon"""

    print("=" * 80)
    print("CHRISTIAN VE AFRICA İSİMLERİ ÜRETİMİ")
    print("=" * 80)

    all_data = []

    # Christian isimleri (400K)
    christian_data = generate_christian_names(200000)  # 200K kişi = 400K kayıt
    all_data.extend(christian_data)
    print(f"✓ Christianity: {len(christian_data):,} kayıt")

    # Afrika isimleri (200K)
    african_data = generate_african_names(100000)  # 100K kişi = 200K kayıt
    all_data.extend(african_data)
    print(f"✓ Africa expansion: {len(african_data):,} kayıt")

    # JSON olarak kaydet
    output_file = OUTPUT_DIR / "synthetic_christian_african_names.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 80}")
    print(f"TOPLAM: {len(all_data):,} kayıt oluşturuldu")
    print(f"Dosya: {output_file}")
    print(f"{'=' * 80}")

    # İstatistikler
    from collections import Counter
    print("\nDin Dağılımı:")
    religion_counts = Counter(d['religion'] for d in all_data if d['religion'])
    for religion, count in religion_counts.most_common():
        print(f"  {religion:15s}: {count:>8,} kayıt")

    print("\nBölge Dağılımı:")
    region_counts = Counter(d['region'] for d in all_data)
    for region, count in region_counts.most_common():
        print(f"  {region:15s}: {count:>8,} kayıt")

if __name__ == "__main__":
    main()
