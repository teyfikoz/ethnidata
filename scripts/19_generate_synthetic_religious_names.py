"""
Script 19: Generate Synthetic Religious Names
Hedef: 2M+ kayıt için sentetik isim üretimi

Kaynak Dağılımı:
- Islam: 500K kayıt (Ortadoğu, Kuzey Afrika, Endonezya, Pakistan, Bangladeş)
- Hinduism: 300K kayıt (Hindistan, Nepal)
- Buddhism: 200K kayıt (Tayland, Myanmar, Sri Lanka, Tibet, Japonya)
- Judaism: 100K kayıt (İsrail, ABD, Avrupa)
- Christianity: Mevcut 209K + 400K yeni = 609K
- Diğer: 100K (Afrika yerel dinleri, Sikhism, vs.)

Toplam: ~1.6M yeni kayıt
"""

import json
import random
from pathlib import Path
import itertools

OUTPUT_DIR = Path("data/synthetic")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# 1. ISLAM İSİMLERİ (500,000 kayıt)
# =============================================================================

ISLAM_FIRST_NAMES_MALE = [
    # Arapça (300+ isim)
    'muhammad', 'ahmed', 'ali', 'hassan', 'hussain', 'omar', 'umar', 'othman', 'uthman',
    'ibrahim', 'ismail', 'yusuf', 'musa', 'isa', 'adam', 'nuh', 'idris', 'saleh',
    'khalid', 'walid', 'tariq', 'zaid', 'zayd', 'malik', 'karim', 'rahim', 'rashid',
    'saeed', 'said', 'mahmud', 'mahmoud', 'hamza', 'talha', 'bilal', 'usman',
    'abdullah', 'abdulaziz', 'abdulrahman', 'abdulkarim', 'abdulmalik', 'abdulmajid',
    'abduljabbar', 'abdulhadi', 'abdulbasit', 'abdulhakim', 'abdulwahab', 'abdullatif',
    'fahad', 'faisal', 'fawaz', 'firas', 'jamal', 'jamil', 'kamal', 'nasser', 'nasir',
    'rami', 'sami', 'wael', 'adel', 'adil', 'basel', 'basil', 'marwan', 'mazin',
    'murad', 'mustafa', 'nawaf', 'raed', 'rayan', 'samir', 'shadi', 'tamer', 'yasir',
    'yaser', 'yousef', 'ziyad', 'ammar', 'anas', 'aws', 'bara', 'fadi', 'ghazi',
    'hadi', 'hatim', 'haytham', 'hisham', 'jihad', 'luay', 'majed', 'majid', 'osama',
    'qasim', 'rida', 'sahl', 'salah', 'salim', 'sameh', 'sufyan', 'taha', 'tariq',
    'usama', 'wasim', 'wisam', 'yazid', 'zakaria', 'zaki',
    # Türkçe-İslami
    'ahmet', 'mehmet', 'mustafa', 'kemal', 'osman', 'hasan', 'huseyin', 'suleyman',
    'selim', 'yusuf', 'omer', 'emir', 'emre', 'enes', 'eren', 'furkan', 'hamza',
    'ilyas', 'ismail', 'mert', 'muhammed', 'muhammet', 'murat', 'rasim', 'recep',
    'resul', 'ridvan', 'sahin', 'salih', 'taha', 'tahir', 'talha', 'umut', 'yasin',
    'yunus', 'yusuf', 'zafer', 'zeki',
    # Farsca-Urdu
    'reza', 'abbas', 'jafar', 'murtaza', 'mujtaba', 'hossein', 'morteza', 'mehdi',
    'mahdi', 'sajjad', 'javad', 'amir', 'arash', 'babak', 'bahram', 'bijan', 'cyrus',
    'darius', 'farshad', 'farzad', 'hamed', 'javid', 'kamran', 'kian', 'kourosh',
    'navid', 'omid', 'payam', 'peyman', 'pouya', 'ramin', 'roshan', 'saman', 'shahin',
    'shahram', 'shervin', 'siamak', 'sina', 'soroush', 'vahid',
    # Endonezya-Malay
    'ahmad', 'amin', 'arif', 'aziz', 'budi', 'daud', 'farid', 'habib', 'hakim',
    'halim', 'hamid', 'hanif', 'harun', 'idris', 'irfan', 'irwan', 'iqbal', 'iskandar',
    'joko', 'kadir', 'latif', 'lutfi', 'nasir', 'nazir', 'rahim', 'rahman', 'rais',
    'ridwan', 'rizki', 'rusdi', 'salam', 'shaleh', 'shafiq', 'syahrul', 'tahir',
    'taufik', 'toufik', 'umar', 'wahid', 'yusri', 'zakir', 'zulkifli',
    # Pakistan-Bangladeş
    'abdul', 'adnan', 'aslam', 'asad', 'ashraf', 'ayub', 'azhar', 'faizan', 'farhan',
    'ghulam', 'habib', 'hafeez', 'hameed', 'haris', 'hashim', 'hussain', 'imran',
    'iqbal', 'ishaq', 'jalal', 'junaid', 'khalil', 'maaz', 'majid', 'mansoor', 'masood',
    'nabeel', 'nadeem', 'naeem', 'naveed', 'noman', 'qamar', 'qasim', 'rafiq', 'rauf',
    'rehan', 'rizwan', 'saad', 'sabir', 'sadiq', 'shahid', 'shakeel', 'sharif', 'shoaib',
    'sohail', 'sulaiman', 'tanveer', 'tariq', 'usman', 'waqar', 'waseem', 'zahid', 'zubair'
]

ISLAM_FIRST_NAMES_FEMALE = [
    # Arapça
    'aisha', 'ayesha', 'fatima', 'khadija', 'maryam', 'zainab', 'zaynab', 'ruqayyah',
    'hafsa', 'safiya', 'asma', 'sumayyah', 'umm', 'amina', 'aminah', 'alia', 'aliya',
    'amira', 'aya', 'dalia', 'dalal', 'dina', 'farah', 'ghada', 'hala', 'hanan',
    'hind', 'huda', 'iman', 'jamila', 'jannah', 'karima', 'laila', 'layla', 'leila',
    'lina', 'lubna', 'malak', 'mona', 'nada', 'naima', 'najla', 'noor', 'nour',
    'raja', 'rana', 'rania', 'rawda', 'reem', 'rima', 'sabah', 'sahar', 'saida',
    'sajida', 'salma', 'samia', 'samira', 'sara', 'sarah', 'sawsan', 'shadia', 'shaima',
    'shahla', 'soraya', 'suad', 'suha', 'sumaya', 'tasneem', 'wafa', 'widad', 'yasmin',
    'yasmine', 'yusra', 'zahra', 'zara', 'zuleika', 'zulekha',
    # Türkçe-İslami
    'ayse', 'emine', 'hatice', 'zeynep', 'fatma', 'havva', 'merve', 'sümeyye',
    'elif', 'esra', 'irem', 'meryem', 'nur', 'sena', 'zehra', 'busra', 'damla',
    'ebru', 'ece', 'emine', 'esma', 'fadime', 'filiz', 'gonca', 'gulbahar', 'halime',
    'kubra', 'latife', 'leyla', 'mediha', 'melek', 'mucella', 'nesrin', 'nihal',
    'rabia', 'rahime', 'ruken', 'safiye', 'saime', 'selma', 'semra', 'sibel', 'sinem',
    'sultan', 'sumeyra', 'tugba', 'ulviye', 'yasemin', 'yildiz', 'zuhal',
    # Farsca-Urdu
    'arezoo', 'darya', 'elnaz', 'fatemeh', 'golnaz', 'leila', 'mahsa', 'mitra',
    'mojgan', 'narges', 'nasrin', 'nazanin', 'niloofar', 'pari', 'parisa', 'pegah',
    'roxana', 'sadaf', 'sanaz', 'setareh', 'shadi', 'shirin', 'soheila', 'somayyeh',
    'taraneh', 'yasaman', 'zahra', 'zari',
    # Endonezya-Malay
    'aisyah', 'aminah', 'anisa', 'azizah', 'dewi', 'farah', 'farida', 'fatimah',
    'hanifa', 'hasna', 'laila', 'mariam', 'nabila', 'nurul', 'putri', 'rahma',
    'rani', 'ratna', 'safira', 'salwa', 'siti', 'soraya', 'syarifah', 'wardah',
    'zahra', 'zakiyah', 'zara', 'zulaikha',
    # Pakistan-Bangladeş
    'aalia', 'aeman', 'aiza', 'alina', 'amara', 'ambreen', 'areeba', 'asiya', 'ayesha',
    'benish', 'bisma', 'faiza', 'faryal', 'hana', 'hiba', 'hira', 'hoorain', 'huma',
    'kinza', 'maheen', 'mahnoor', 'malaika', 'maria', 'mehak', 'mehreen', 'misbah',
    'naila', 'nimra', 'rabia', 'rameen', 'rubab', 'saba', 'sadaf', 'saima', 'sana',
    'sania', 'sara', 'shanza', 'sidra', 'sumaira', 'tooba', 'urooj', 'zainab', 'zoya'
]

ISLAM_LAST_NAMES = [
    # Arapça soyadları
    'abdullah', 'abbas', 'abdallah', 'abdel', 'abdel-rahman', 'abdulaziz', 'abdulrahman',
    'ahmad', 'ahmed', 'al-ahmed', 'al-ali', 'al-hassan', 'al-hussein', 'al-said', 'al-salem',
    'alam', 'ali', 'alawi', 'asiri', 'attar', 'aziz', 'badawi', 'bahri', 'baker', 'basha',
    'ben-ali', 'daher', 'darwish', 'daud', 'fahmi', 'farah', 'farooq', 'ghanem', 'habib',
    'haddad', 'hafez', 'hamdan', 'hamdi', 'hamid', 'hamza', 'haq', 'hasan', 'hassan',
    'husain', 'hussain', 'hussein', 'ibrahim', 'iqbal', 'ismail', 'jaber', 'jamal',
    'jamil', 'jawad', 'kamal', 'kamel', 'kareem', 'karim', 'kassem', 'kazmi', 'khalid',
    'khalil', 'khan', 'khatib', 'mahmood', 'mahmoud', 'majeed', 'majid', 'malik', 'mansour',
    'masood', 'masri', 'matar', 'mazin', 'mehdi', 'moussa', 'mousa', 'mubarak', 'muhammed',
    'murad', 'musa', 'mustafa', 'nabil', 'nader', 'nadir', 'najjar', 'nasser', 'nassar',
    'nasir', 'nawaz', 'nazir', 'noor', 'omar', 'osman', 'othman', 'qadri', 'qasim',
    'rachid', 'rahim', 'rahman', 'ramadan', 'rashed', 'rashid', 'razaq', 'reza', 'rizvi',
    'sabri', 'sadiq', 'saeed', 'said', 'salah', 'saleh', 'salem', 'salim', 'samir',
    'sarwar', 'sayeed', 'shah', 'shahid', 'shaikh', 'shakir', 'shamsi', 'sharif', 'sheikh',
    'siddiqui', 'soliman', 'sulaiman', 'suleiman', 'sultan', 'tahir', 'tariq', 'tawfiq',
    'umar', 'usman', 'wahab', 'waheed', 'waleed', 'wali', 'waseem', 'yasin', 'yousef',
    'youssef', 'yousuf', 'yunus', 'yusuf', 'zafar', 'zahid', 'zaki', 'zaman', 'zia',
    # Türk soyadları
    'yilmaz', 'kaya', 'demir', 'celik', 'sahin', 'yildiz', 'yildirim', 'ozturk', 'aydin',
    'ozdemir', 'arslan', 'dogan', 'kilic', 'aslan', 'cetin', 'kara', 'koc', 'kurt', 'ozkan',
    'simsek', 'polat', 'erdogan', 'tas', 'karaca', 'acar', 'kaya', 'gul', 'coskun', 'korkmaz',
    # Pakistan-Hint soyadları (İslami)
    'khan', 'ahmed', 'ali', 'shah', 'hussain', 'akhtar', 'malik', 'sheikh', 'siddiqui',
    'chaudhry', 'butt', 'rana', 'mughal', 'mirza', 'baig', 'ansari', 'qureshi', 'rizvi',
    # Endonezya-Malay
    'rahman', 'hasan', 'ahmad', 'ismail', 'abdullah', 'mohamed', 'mohammed', 'ibrahim',
    'yusof', 'ali', 'hassan', 'hussein', 'amin', 'hamid', 'said', 'omar'
]

ISLAM_COUNTRIES = {
    # Ortadoğu
    'SAU': ('Saudi Arabia', 'Arabic', 'Asia'),
    'ARE': ('United Arab Emirates', 'Arabic', 'Asia'),
    'QAT': ('Qatar', 'Arabic', 'Asia'),
    'KWT': ('Kuwait', 'Arabic', 'Asia'),
    'BHR': ('Bahrain', 'Arabic', 'Asia'),
    'OMN': ('Oman', 'Arabic', 'Asia'),
    'YEM': ('Yemen', 'Arabic', 'Asia'),
    'JOR': ('Jordan', 'Arabic', 'Asia'),
    'SYR': ('Syria', 'Arabic', 'Asia'),
    'LBN': ('Lebanon', 'Arabic', 'Asia'),
    'IRQ': ('Iraq', 'Arabic', 'Asia'),
    'PSE': ('Palestine', 'Arabic', 'Asia'),
    # Kuzey Afrika
    'EGY': ('Egypt', 'Arabic', 'Africa'),
    'DZA': ('Algeria', 'Arabic', 'Africa'),
    'MAR': ('Morocco', 'Arabic', 'Africa'),
    'TUN': ('Tunisia', 'Arabic', 'Africa'),
    'LBY': ('Libya', 'Arabic', 'Africa'),
    'SDN': ('Sudan', 'Arabic', 'Africa'),
    'SOM': ('Somalia', 'Somali', 'Africa'),
    'MRT': ('Mauritania', 'Arabic', 'Africa'),
    # Asya-Pasifik
    'IDN': ('Indonesia', 'Indonesian', 'Asia'),
    'PAK': ('Pakistan', 'Urdu', 'Asia'),
    'BGD': ('Bangladesh', 'Bengali', 'Asia'),
    'MYS': ('Malaysia', 'Malay', 'Asia'),
    'TUR': ('Turkey', 'Turkish', 'Asia'),
    'IRN': ('Iran', 'Persian', 'Asia'),
    'AFG': ('Afghanistan', 'Pashto', 'Asia'),
    'AZE': ('Azerbaijan', 'Azerbaijani', 'Asia'),
    'UZB': ('Uzbekistan', 'Uzbek', 'Asia'),
    'KAZ': ('Kazakhstan', 'Kazakh', 'Asia'),
    'TKM': ('Turkmenistan', 'Turkmen', 'Asia'),
    'KGZ': ('Kyrgyzstan', 'Kyrgyz', 'Asia'),
    'TJK': ('Tajikistan', 'Tajik', 'Asia'),
    # Sub-Saharan Afrika
    'NGA': ('Nigeria', 'English', 'Africa'),
    'SEN': ('Senegal', 'French', 'Africa'),
    'MLI': ('Mali', 'French', 'Africa'),
    'NER': ('Niger', 'French', 'Africa'),
    'TCD': ('Chad', 'French', 'Africa'),
}

# =============================================================================
# 2. HINDUISM İSİMLERİ (300,000 kayıt)
# =============================================================================

HINDU_FIRST_NAMES_MALE = [
    'aditya', 'akash', 'amit', 'anand', 'anil', 'ankit', 'arjun', 'aryan', 'ashish',
    'ashok', 'atul', 'ajay', 'bharat', 'deepak', 'dev', 'dinesh', 'gaurav', 'hardik',
    'harsh', 'hemant', 'jay', 'karan', 'kartik', 'kiran', 'krishna', 'kunal', 'lakshman',
    'manoj', 'mohit', 'mukesh', 'naman', 'naveen', 'nikhil', 'nitin', 'pradeep', 'prakash',
    'pranav', 'prashant', 'prateek', 'rahul', 'raj', 'rajat', 'rajesh', 'raju', 'rakesh',
    'ram', 'raman', 'ravi', 'rohit', 'sachin', 'sagar', 'sahil', 'sanjay', 'sandeep',
    'santosh', 'saurabh', 'shailesh', 'shivam', 'shubham', 'siddharth', 'sudhir', 'sumit',
    'sunil', 'suraj', 'suresh', 'tanmay', 'tarun', 'umesh', 'varun', 'vijay', 'vikram',
    'vikrant', 'vinay', 'vineet', 'vinod', 'vishal', 'vikas', 'yash', 'yogesh'
]

HINDU_FIRST_NAMES_FEMALE = [
    'aarti', 'aditi', 'akshara', 'ananya', 'anjali', 'anita', 'anu', 'anuja', 'archana',
    'asha', 'asmita', 'avni', 'bhavana', 'chitra', 'deepa', 'deepika', 'devika', 'diya',
    'divya', 'gayatri', 'geeta', 'gita', 'hema', 'isha', 'jaya', 'jyoti', 'kajal',
    'kalpana', 'kamala', 'kanchan', 'kavita', 'kiran', 'komal', 'krishna', 'lakshmi',
    'lata', 'laxmi', 'leela', 'madhu', 'madhuri', 'mahima', 'mala', 'malini', 'mamta',
    'manisha', 'mansi', 'maya', 'meena', 'meera', 'megha', 'mira', 'mohini', 'nalini',
    'nandini', 'neelam', 'neha', 'nidhi', 'nisha', 'nita', 'parvati', 'pooja', 'poonam',
    'pragati', 'prarthana', 'pratibha', 'preethi', 'preeti', 'priya', 'priyanka', 'puja',
    'pushpa', 'radha', 'rani', 'rashmi', 'ratna', 'rekha', 'renu', 'ritu', 'roshni',
    'rukmini', 'sadhana', 'sangeeta', 'sangita', 'sarita', 'sarla', 'sarojini', 'savita',
    'shanti', 'sheela', 'shilpa', 'shobha', 'shraddha', 'shreya', 'shweta', 'sita',
    'smita', 'sneha', 'sonal', 'sonali', 'sonia', 'sridevi', 'sudha', 'sujata', 'sulochana',
    'sumati', 'sumitra', 'sunita', 'sunitha', 'supriya', 'sushma', 'tanvi', 'tara',
    'usha', 'vani', 'vanita', 'veena', 'vidya', 'vijaya', 'yamini'
]

HINDU_LAST_NAMES = [
    'agarwal', 'sharma', 'kumar', 'singh', 'patel', 'gupta', 'reddy', 'iyer', 'rao',
    'desai', 'joshi', 'nair', 'menon', 'pillai', 'verma', 'malhotra', 'kapoor', 'mehta',
    'chopra', 'bose', 'das', 'dutta', 'ghosh', 'mukherjee', 'banerjee', 'chatterjee',
    'chakraborty', 'bhattacharya', 'roy', 'sen', 'saxena', 'sinha', 'mishra', 'pandey',
    'tiwari', 'dwivedi', 'trivedi', 'jain', 'soni', 'shah', 'thakur', 'rathore', 'chauhan',
    'rajput', 'yadav', 'patil', 'kulkarni', 'deshpande', 'gokhale', 'kale', 'joshi',
    'naik', 'sawant', 'kamath', 'shetty', 'hegde', 'bhat', 'pai', 'krishnan', 'swamy',
    'murthy', 'raman', 'venkat', 'subramaniam', 'nathan', 'narayanan', 'gopal', 'mohan'
]

HINDU_COUNTRIES = {
    'IND': ('India', 'Hindi', 'Asia'),
    'NPL': ('Nepal', 'Nepali', 'Asia'),
    'LKA': ('Sri Lanka', 'Sinhala', 'Asia'),
    'BTN': ('Bhutan', 'Dzongkha', 'Asia'),
    'MUS': ('Mauritius', 'English', 'Africa'),
    'FJI': ('Fiji', 'English', 'Oceania'),
}

# =============================================================================
# 3. BUDDHISM İSİMLERİ (200,000 kayıt)
# =============================================================================

BUDDHIST_FIRST_NAMES_MALE = [
    # Tayland
    'somchai', 'somsak', 'somporn', 'surachai', 'surin', 'suthat', 'thawat', 'thongchai',
    'wichai', 'wirat', 'wisit', 'yutthana', 'ananda', 'anucha', 'arun', 'chaiwat',
    'chatchai', 'kriangsak', 'nattapong', 'panya', 'prayoon', 'preecha', 'prasit',
    'sanguan', 'sanya', 'sarawut', 'sirichai', 'somkiat', 'sompong', 'songkran',
    # Myanmar
    'aung', 'hla', 'htun', 'kyaw', 'maung', 'min', 'myint', 'naing', 'nyein', 'soe',
    'than', 'thein', 'thet', 'tin', 'tun', 'win', 'ye', 'zaw', 'htet', 'ko',
    # Tibet-Bhutan
    'dorje', 'tenzin', 'karma', 'sonam', 'tsering', 'phuntsok', 'rinchen', 'jamyang',
    'lobsang', 'ngawang', 'thubten', 'choegyal', 'dakpa', 'dorji', 'lhamo', 'namgyal',
    'palden', 'pema', 'samten', 'wangchuk', 'yeshe',
    # Sri Lanka
    'bandula', 'dilan', 'gamini', 'kasun', 'kumara', 'lalith', 'mahinda', 'nimal',
    'pradeep', 'priyantha', 'roshan', 'sampath', 'sanjeewa', 'saman', 'sunil', 'tissa',
    'upul', 'vijitha', 'wasantha',
    # Japonya (Zen)
    'akira', 'daichi', 'haruto', 'hiroshi', 'ichiro', 'kaito', 'kenji', 'koji', 'makoto',
    'masato', 'naoki', 'ryo', 'satoshi', 'takeshi', 'takumi', 'taro', 'yuki', 'yuto'
]

BUDDHIST_FIRST_NAMES_FEMALE = [
    # Tayland
    'amporn', 'apsara', 'chanya', 'kulap', 'mali', 'malee', 'nareerat', 'nittaya',
    'nong', 'noppawan', 'nuch', 'nida', 'orathai', 'pensri', 'pim', 'rattana',
    'siriwan', 'somjai', 'suda', 'sumalee', 'supaporn', 'supattra', 'sutida', 'wannee',
    # Myanmar
    'aye', 'cho', 'hla', 'khin', 'ma', 'may', 'moe', 'mon', 'myat', 'nway', 'nu',
    'phyu', 'san', 'saw', 'su', 'thet', 'thida', 'thin', 'win', 'yi',
    # Tibet-Bhutan
    'dawa', 'dekyi', 'dolma', 'lhamo', 'ngawang', 'pema', 'sonam', 'tashi', 'tsomo',
    'yangchen', 'yeshe', 'zangmo', 'choden', 'dechen', 'kunzang', 'metok', 'nyima',
    # Sri Lanka
    'anoma', 'champika', 'chandrika', 'dilani', 'kumari', 'lalitha', 'malini', 'nilanthi',
    'padma', 'rangani', 'sandya', 'shyamali', 'sunethra', 'thilini', 'udayani', 'vasanthi',
    # Japonya
    'aiko', 'akiko', 'asuka', 'ayaka', 'emi', 'hana', 'haruka', 'hiroko', 'kaori',
    'keiko', 'kumiko', 'mai', 'maki', 'mariko', 'mayumi', 'megumi', 'mika', 'naoko',
    'rie', 'sachiko', 'sakura', 'sato', 'sayuri', 'tomoko', 'yoko', 'yuki', 'yumi'
]

BUDDHIST_LAST_NAMES = [
    # Tayland
    'saetang', 'saelim', 'chaiyaporn', 'chutima', 'jantharatip', 'kaewmanee', 'maneerat',
    'pattaya', 'phongam', 'ratanaporn', 'sangthong', 'sirisopa', 'somsak', 'srisuwan',
    'tangsomboon', 'vanichakul', 'wattana', 'yodyingyong',
    # Myanmar
    'hlaing', 'htoo', 'khin', 'kyaw', 'maung', 'myint', 'naing', 'oo', 'soe', 'thein',
    'thant', 'thet', 'thu', 'tin', 'tun', 'win', 'ye', 'zaw',
    # Tibet-Bhutan
    'dorji', 'lama', 'sherpa', 'tamang', 'gurung', 'wangchuk', 'pema', 'tenzin', 'karma',
    # Sri Lanka
    'fernando', 'silva', 'perera', 'de silva', 'jayawardena', 'wickramasinghe', 'dissanayake',
    'gunathilaka', 'kumaratunga', 'ratnayake', 'siriwardena', 'wijesinghe',
    # Japonya
    'sato', 'suzuki', 'takahashi', 'tanaka', 'watanabe', 'ito', 'yamamoto', 'nakamura',
    'kobayashi', 'kato', 'yoshida', 'yamada', 'sasaki', 'yamaguchi', 'matsumoto', 'inoue'
]

BUDDHIST_COUNTRIES = {
    'THA': ('Thailand', 'Thai', 'Asia'),
    'MMR': ('Myanmar', 'Burmese', 'Asia'),
    'LKA': ('Sri Lanka', 'Sinhala', 'Asia'),
    'BTN': ('Bhutan', 'Dzongkha', 'Asia'),
    'KHM': ('Cambodia', 'Khmer', 'Asia'),
    'LAO': ('Laos', 'Lao', 'Asia'),
    'VNM': ('Vietnam', 'Vietnamese', 'Asia'),
    'JPN': ('Japan', 'Japanese', 'Asia'),
    'TWN': ('Taiwan', 'Chinese', 'Asia'),
    'MNG': ('Mongolia', 'Mongolian', 'Asia'),
}

# =============================================================================
# 4. JUDAISM İSİMLERİ (100,000 kayıt)
# =============================================================================

JEWISH_FIRST_NAMES_MALE = [
    'aaron', 'abraham', 'adam', 'ari', 'asher', 'benjamin', 'caleb', 'daniel', 'david',
    'eli', 'elijah', 'ethan', 'ezra', 'gabriel', 'isaac', 'isaiah', 'jacob', 'jonah',
    'joseph', 'joshua', 'levi', 'michael', 'moses', 'nathan', 'noah', 'samuel', 'simon',
    'solomon', 'yosef', 'yitzhak', 'yaakov', 'moshe', 'shlomo', 'chaim', 'avraham', 'menachem',
    'mordechai', 'yehuda', 'shimon', 'reuven', 'zvi', 'baruch', 'dov', 'eitan', 'gershon',
    'hillel', 'noam', 'oren', 'tal', 'uri', 'yair', 'zalman', 'zev'
]

JEWISH_FIRST_NAMES_FEMALE = [
    'abigail', 'deborah', 'dinah', 'esther', 'hannah', 'judith', 'leah', 'miriam', 'naomi',
    'rachel', 'rebecca', 'ruth', 'sarah', 'tamar', 'chaya', 'rivka', 'shira', 'shoshana',
    'tova', 'yael', 'zippora', 'avigail', 'chana', 'dina', 'eliana', 'maya', 'michal',
    'noa', 'orly', 'penina', 'raizel', 'talia', 'tziporah', 'yaffa', 'yehudit'
]

JEWISH_LAST_NAMES = [
    # Ashkenazi
    'cohen', 'levy', 'levi', 'goldberg', 'goldman', 'goldstein', 'goldsmith', 'silver',
    'silverman', 'silverstein', 'stein', 'steinberg', 'rosenberg', 'rosenfeld', 'rosen',
    'berg', 'berger', 'bergman', 'blum', 'blumenthal', 'diamond', 'diamant', 'feldman',
    'feld', 'fisher', 'fischer', 'friedman', 'green', 'greenberg', 'gross', 'grossman',
    'kaplan', 'katz', 'klein', 'kleinman', 'kramer', 'levin', 'levine', 'levinson',
    'lieberman', 'miller', 'newman', 'perlman', 'rabin', 'rabinowitz', 'reich', 'richman',
    'roth', 'rothman', 'rothschild', 'rubin', 'rubinstein', 'schneider', 'schwartz',
    'shapiro', 'sherman', 'siegel', 'siegelman', 'singer', 'stern', 'sternberg', 'wein',
    'weinberg', 'weiner', 'weinstein', 'weiss', 'weisman', 'wolf', 'wolff', 'zimmerman',
    # Sephardi
    'abadi', 'abramov', 'alhadeff', 'behar', 'benaim', 'benasayag', 'benveniste', 'cardozo',
    'castro', 'cordova', 'elbaz', 'franco', 'gabbay', 'hakim', 'levy', 'medina', 'mizrahi',
    'molho', 'nahum', 'perez', 'salem', 'shamash', 'soriano', 'toledo', 'toledano',
    # Israeli (modern)
    'amir', 'ben-david', 'cohen', 'dayan', 'golan', 'keren', 'lev', 'meir', 'sharon',
    'tal', 'tamir', 'yaron', 'zohar'
]

JEWISH_COUNTRIES = {
    'ISR': ('Israel', 'Hebrew', 'Asia'),
    'USA': ('United States', 'English', 'Americas'),
    'GBR': ('United Kingdom', 'English', 'Europe'),
    'FRA': ('France', 'French', 'Europe'),
    'CAN': ('Canada', 'English', 'Americas'),
    'ARG': ('Argentina', 'Spanish', 'Americas'),
    'DEU': ('Germany', 'German', 'Europe'),
    'AUS': ('Australia', 'English', 'Oceania'),
    'RUS': ('Russia', 'Russian', 'Europe'),
    'UKR': ('Ukraine', 'Ukrainian', 'Europe'),
}

# =============================================================================
# SENTETIK VERİ ÜRETIMI
# =============================================================================

def generate_synthetic_names(religion, first_names_male, first_names_female, last_names, countries, target_count):
    """Sentetik isim verisi üret"""

    data = []

    # Gender dağılımı (50-50)
    male_count = target_count // 2
    female_count = target_count - male_count

    print(f"\n{religion} için {target_count:,} kayıt üretiliyor...")
    print(f"  - Erkek: {male_count:,}")
    print(f"  - Kadın: {female_count:,}")

    # Erkek isimleri
    for i in range(male_count):
        first_name = random.choice(first_names_male)
        last_name = random.choice(last_names)
        country_code, (country_name, language, region) = random.choice(list(countries.items()))

        # First name
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

        # Last name
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

    # Kadın isimleri
    for i in range(female_count):
        first_name = random.choice(first_names_female)
        last_name = random.choice(last_names)
        country_code, (country_name, language, region) = random.choice(list(countries.items()))

        # First name
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

        # Last name
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

# =============================================================================
# ANA FONKSİYON
# =============================================================================

def main():
    """Ana üretim fonksiyonu"""

    print("=" * 80)
    print("SENTETİK DİNİ İSİM VERİSİ ÜRETİMİ")
    print("=" * 80)

    all_data = []

    # 1. Islam isimleri (500K)
    islam_data = generate_synthetic_names(
        religion='Islam',
        first_names_male=ISLAM_FIRST_NAMES_MALE,
        first_names_female=ISLAM_FIRST_NAMES_FEMALE,
        last_names=ISLAM_LAST_NAMES,
        countries=ISLAM_COUNTRIES,
        target_count=250000  # 250K kişi = 500K kayıt (first + last)
    )
    all_data.extend(islam_data)
    print(f"✓ Islam: {len(islam_data):,} kayıt")

    # 2. Hinduism isimleri (300K)
    hindu_data = generate_synthetic_names(
        religion='Hinduism',
        first_names_male=HINDU_FIRST_NAMES_MALE,
        first_names_female=HINDU_FIRST_NAMES_FEMALE,
        last_names=HINDU_LAST_NAMES,
        countries=HINDU_COUNTRIES,
        target_count=150000  # 150K kişi = 300K kayıt
    )
    all_data.extend(hindu_data)
    print(f"✓ Hinduism: {len(hindu_data):,} kayıt")

    # 3. Buddhism isimleri (200K)
    buddhist_data = generate_synthetic_names(
        religion='Buddhism',
        first_names_male=BUDDHIST_FIRST_NAMES_MALE,
        first_names_female=BUDDHIST_FIRST_NAMES_FEMALE,
        last_names=BUDDHIST_LAST_NAMES,
        countries=BUDDHIST_COUNTRIES,
        target_count=100000  # 100K kişi = 200K kayıt
    )
    all_data.extend(buddhist_data)
    print(f"✓ Buddhism: {len(buddhist_data):,} kayıt")

    # 4. Judaism isimleri (100K)
    jewish_data = generate_synthetic_names(
        religion='Judaism',
        first_names_male=JEWISH_FIRST_NAMES_MALE,
        first_names_female=JEWISH_FIRST_NAMES_FEMALE,
        last_names=JEWISH_LAST_NAMES,
        countries=JEWISH_COUNTRIES,
        target_count=50000  # 50K kişi = 100K kayıt
    )
    all_data.extend(jewish_data)
    print(f"✓ Judaism: {len(jewish_data):,} kayıt")

    # JSON olarak kaydet
    output_file = OUTPUT_DIR / "synthetic_religious_names.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 80}")
    print(f"TOPLAM: {len(all_data):,} kayıt oluşturuldu")
    print(f"Dosya: {output_file}")
    print(f"{'=' * 80}")

    # İstatistikler
    print("\nDin Dağılımı:")
    from collections import Counter
    religion_counts = Counter(d['religion'] for d in all_data)
    for religion, count in religion_counts.most_common():
        print(f"  {religion:15s}: {count:>8,} kayıt")

    print("\nBölge Dağılımı:")
    region_counts = Counter(d['region'] for d in all_data if d['region'])
    for region, count in region_counts.most_common():
        print(f"  {region:15s}: {count:>8,} kayıt")

if __name__ == "__main__":
    main()
