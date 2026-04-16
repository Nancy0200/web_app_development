"""
八字排盤核心邏輯模組
實作天干地支換算、生辰八字產生與基礎命格解析。
"""

# 天干（十天干）
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支（十二地支）
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 五行對應天干
STEM_ELEMENT = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

# 五行對應地支
BRANCH_ELEMENT = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 地支對應生肖
BRANCH_ZODIAC = {
    '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
    '辰': '龍', '巳': '蛇', '午': '馬', '未': '羊',
    '申': '猴', '酉': '雞', '戌': '狗', '亥': '豬',
}

# 五行性格解析
ELEMENT_PERSONALITY = {
    '木': '具有仁慈、進取與創造力，富有同情心，適合從事教育、藝術或社會服務。',
    '火': '熱情奔放、充滿活力，領導力強，個性直爽，適合從事管理或公關工作。',
    '土': '穩重踏實、值得信賴，重視家庭，擅長規劃，適合從事建設或行政工作。',
    '金': '剛毅果斷、意志堅定，重義氣，適合從事法律、金融或軍警工作。',
    '水': '聰明靈活、善於溝通，思維敏銳，適合從事學術研究或文化創意產業。',
}

# 月份對應節氣天干（簡化版）
MONTH_STEM_BASE = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]


def get_year_pillar(year):
    """
    計算年柱天干地支。

    Args:
        year (int): 西元年份

    Returns:
        dict: 含 stem（天干）、branch（地支）、element（五行）、zodiac（生肖）
    """
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    return {
        'stem': stem,
        'branch': branch,
        'element': STEM_ELEMENT[stem],
        'zodiac': BRANCH_ZODIAC[branch],
        'pillar': stem + branch,
    }


def get_month_pillar(year, month):
    """
    計算月柱天干地支（以節氣月為基準的簡化版本）。

    Args:
        year (int): 西元年份
        month (int): 月份（1-12）

    Returns:
        dict: 含 stem、branch、element
    """
    year_stem_idx = (year - 4) % 10
    # 月干以年干為基準，按五虎遁年起月法
    month_stem_base = (year_stem_idx % 5) * 2
    stem_idx = (month_stem_base + month - 1) % 10
    # 月支：寅月(寅=index 2)為正月，以此排列
    branch_idx = (month + 1) % 12
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    return {
        'stem': stem,
        'branch': branch,
        'element': STEM_ELEMENT[stem],
        'pillar': stem + branch,
    }


def get_day_pillar(year, month, day):
    """
    計算日柱天干地支（以已知基準日推算）。
    基準：2000年1月1日 為甲子日（天干=甲=0, 地支=子=0）

    Args:
        year (int): 西元年份
        month (int): 月份
        day (int): 日

    Returns:
        dict: 含 stem、branch、element
    """
    # 計算距基準日的天數
    from datetime import date
    try:
        target = date(year, month, day)
        base = date(2000, 1, 1)
        delta = (target - base).days
    except ValueError:
        delta = 0

    stem_idx = delta % 10
    branch_idx = delta % 12
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    return {
        'stem': stem,
        'branch': branch,
        'element': STEM_ELEMENT[stem],
        'pillar': stem + branch,
    }


def get_hour_pillar(day_stem, birth_time):
    """
    計算時柱天干地支（五鼠遁日起時法）。

    Args:
        day_stem (str): 日柱天干
        birth_time (int | None): 出生時辰（0-23），每2小時一個時辰

    Returns:
        dict: 含 stem、branch、element
    """
    if birth_time is None:
        return {'stem': '?', 'branch': '?', 'element': '不詳', 'pillar': '??'}

    # 時支：子時 = 0或23，排序固定
    hour_branch_idx = ((birth_time + 1) // 2) % 12
    # 時干以日干為基準（五鼠遁）
    day_stem_idx = HEAVENLY_STEMS.index(day_stem) if day_stem in HEAVENLY_STEMS else 0
    hour_stem_base = (day_stem_idx % 5) * 2
    hour_stem_idx = (hour_stem_base + hour_branch_idx) % 10

    stem = HEAVENLY_STEMS[hour_stem_idx]
    branch = EARTHLY_BRANCHES[hour_branch_idx]
    return {
        'stem': stem,
        'branch': branch,
        'element': STEM_ELEMENT[stem],
        'pillar': stem + branch,
    }


def calculate_bazi(birth_year, birth_month, birth_day, birth_time, gender):
    """
    主要八字計算函式，回傳完整的排盤結果。

    Args:
        birth_year (int): 出生年份
        birth_month (int): 出生月份（1-12）
        birth_day (int): 出生日期（1-31）
        birth_time (int | None): 出生時辰（0-23），可為 None
        gender (str): 'M'（男）或 'F'（女）

    Returns:
        dict: 完整八字排盤結果，包含四柱、五行統計與命格解析
    """
    year_pillar = get_year_pillar(birth_year)
    month_pillar = get_month_pillar(birth_year, birth_month)
    day_pillar = get_day_pillar(birth_year, birth_month, birth_day)
    hour_pillar = get_hour_pillar(day_pillar['stem'], birth_time)

    # 五行統計
    elements = [
        year_pillar['element'], month_pillar['element'],
        day_pillar['element'], hour_pillar['element'],
    ]
    element_branch = [
        BRANCH_ELEMENT.get(year_pillar['branch'], ''),
        BRANCH_ELEMENT.get(month_pillar['branch'], ''),
        BRANCH_ELEMENT.get(day_pillar['branch'], ''),
        BRANCH_ELEMENT.get(hour_pillar['branch'], ''),
    ]
    all_elements = elements + [e for e in element_branch if e]

    element_count = {}
    for e in ['木', '火', '土', '金', '水']:
        element_count[e] = all_elements.count(e)

    # 命主五行（日柱天干決定命主）
    dominant_element = day_pillar['element']

    # 基礎命格解析
    personality = ELEMENT_PERSONALITY.get(dominant_element, '')
    gender_label = '男命' if gender == 'M' else '女命'

    return {
        'year_pillar': year_pillar,
        'month_pillar': month_pillar,
        'day_pillar': day_pillar,
        'hour_pillar': hour_pillar,
        'zodiac': year_pillar['zodiac'],
        'dominant_element': dominant_element,
        'element_count': element_count,
        'personality': personality,
        'gender_label': gender_label,
        'birth_info': {
            'year': birth_year,
            'month': birth_month,
            'day': birth_day,
            'time': birth_time,
            'gender': gender,
        }
    }
