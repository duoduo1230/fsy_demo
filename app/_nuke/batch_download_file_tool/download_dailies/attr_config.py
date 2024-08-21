#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


COLOR_SPACE_CONFIG = {
    'xyzs': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'xyzs_slate'
    },
    'jjs': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'jjs_slate'
    },
    'default': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': ''
    },
    'yncg': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'yncg_slate'
    },
    'sia': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'sia_slate'
    },
    'hdw': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'hdw_slate'
    },
    'chosin': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'chosin_slate'
    },
    'jqrlb': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'jqrlb_slate'
    },
    'flrw': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'flrw_slate'
    },
    'bw': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'bw_slate'
    },
    'hx': {
            'color_space_input': '',
            'color_space_output': '',
            'working_space': '',
            'root': {
                'colorManagement': 'OCIO',
                'OCIO_config': 'aces_1.0.3',
                'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
                'workingSpaceLUT': 'ACES - ACEScg',
                'monitorLut': 'ACES/Rec.709',
                'int8Lut': 'Utility - sRGB - Texture',
                'int16Lut': 'ACES - ACEScc',
                'logLut': 'Input - ADX - ADX10',
                'floatLut': 'ACES - ACEScg'
            },
            'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                            'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
            'slate': 'hx_slate'
        },
    'qzsd': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'qzsd_slate_02'
    },
    'zhy': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'zhy_slate'
    },
    'mzh': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'mzh_slate'
    },
    'fc2': {
        'color_space_input': '',
        'color_space_output': '',
        'working_space': '',
        'root': {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'
        },
        'root_sorted': ['colorManagement', 'OCIO_config', 'customOCIOConfigPath', 'workingSpaceLUT',
                        'monitorLut', 'int8Lut', 'int16Lut', 'logLut', 'floatLut'],
        'slate': 'fc_slate'
    },
}

META_CODEC_DICT = {
    'h264': 'avc1',
    'prores 422': 'apcn',
    'prores 422 hq': 'apch',
    'prores 422 proxy': 'apco',
    'prores 4444': 'ap4h',
    'prores 422 lt': 'apcs',
    'prores 422 xq': 'ap4h',
    'tiff': 'tiff',
    'jpg': 'jpeg',
}




