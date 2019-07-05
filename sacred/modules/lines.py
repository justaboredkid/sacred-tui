import sys

if sys.stdout.encoding == 'UTF-8':
    '''
    0 = top, 1 = top right, 
    2 = right, 3 = bottom right,
    4 = bottom, 5 = bottom left, 
    6 = left,  7 = top left
    
    Basically just clockwise starting from the top.
    '''
    line = {
        'reg': [
            '\u2500', '\u2510', '\u2502', '\u2518', '\u2500', '\u2514',
            '\u2502', '\u250C'
        ],
        'heavy': [
            '\u2501', '\u2513', '\u2503', '\u251B', '\u2501', '\u2517',
            '\u2503', '\u250F'
        ],
        'dashed': [
            '\u254C', '\u2510', '\u254E', '\u2518', '\u254C', '\u2514',
            '\u254E', '\u250C'
        ],
        'dashedTight': [
            '\u2504', '\u2510', '\u2506', '\u2518', '\u2504', '\u2514',
            '\u2506', '\u250C'
        ],
        'dashedTighter': [
            '\u2508', '\u2510', '\u250A', '\u2518', '\u2508', '\u2514',
            '\u250A', '\u250C'
        ]
    }

else:
    line = None