# List of check tools and their names
CHECK_TOOLS = {
    'nvda': {
        'ja': 'NVDA',
        'en': 'NVDA'
    },
    'macos-vo': {
        'ja': 'macOS VoiceOver',
        'en': 'macOS VoiceOver'
    },
    'axe': {
        'ja': 'axe DevTools',
        'en': 'axe DevTools'
    },
    'ios-vo': {
        'ja': 'iOS VoiceOver',
        'en': 'iOS VoiceOver'
    },
    'android-tb': {
        'ja': 'Android TalkBack',
        'en': 'Android TalkBack'
    },
    'keyboard': {
        'ja': 'キーボード操作',
        'en': 'Keyboard'
    },
    'misc': {
        'ja': 'その他の手段',
        'en': 'Miscellaneous Methods'
    }
}

# Check targets
CHECK_TARGETS = {
    'design': {
        'ja': 'デザイン',
        'en': 'Design'
    },
    'code': {
        'ja': 'コード',
        'en': 'Code'
    },
    'product': {
        'ja': 'プロダクト',
        'en': 'Product'
    }
}

# Names for checks/guidelines/procedures target platforms
PLATFORM_NAMES = {
    'web': {
        'ja': 'Web',
        'en': 'Web'
    },
    'mobile': {
        'ja': 'モバイル',
        'en': 'Mobile'
    },
    'general': {
        'ja': 'Web、モバイル',
        'en': 'Web, Mobile'
    },
    'ios': {
        'ja': 'iOS',
        'en': 'iOS'
    },
    'android': {
        'ja': 'Android',
        'en': 'Android'
    }
}

# Severity tags and its display names
SEVERITY_TAGS = {
    'critical': {
        'ja': '[CRITICAL]',
        'en': '[CRITICAL]'
    },
    'major': {
        'ja': '[MAJOR]',
        'en': '[MAJOR]'
    },
    'normal': {
        'ja': '[NORMAL]',
        'en': '[NORMAL]'
    },
    'minor': {
        'ja': '[MINOR]',
        'en': '[MINOR]'
    }
}

# Possible targets for implementation examples
IMPLEMENTATION_TARGETS = {
    'web': {
        'ja': 'Web',
        'en': 'Web'
    },
    'android': {
        'ja': 'Android',
        'en': 'Android'
    },
    'ios': {
        'ja': 'iOS',
        'en': 'iOS'
    }
}

# for axe rules
AXE_CORE = {
    'submodule_name': 'vendor/axe-core',
    'base_dir': 'vendor/axe-core',  # 追加: yaml2rstでも使用
    'deque_url': 'https://dequeuniversity.com/rules/axe/',
    'msg_ja_file': 'locales/ja.json',
    'pkg_file': 'package.json',
    'rules_dir': 'lib/rules',
    'locale_dir': 'locales',  # 追加: yaml2rstでも使用
    'locale_ja_file': 'ja.json'  # 追加: yaml2rstでも使用
}
