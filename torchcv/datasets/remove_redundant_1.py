'''
그림파일 없이 xml 파일만 남아있는 경우 삭제,
annotation 안된 그림파일 있는 폴더가 나오면 중지.
'''
import os

img_path = '/home/dokyoung/Desktop/server/vanno_data/celeb'
anno_path = '/home/dokyoung/Desktop/server/vanno_results/celeb'

dirs = os.listdir(img_path); dirs.sort()
dirs2 = os.listdir(anno_path); dirs2.sort()

if dirs != dirs2:
    raise Exception

for dir in dirs:
    ls = os.listdir(img_path + '/' + dir); ls.sort()
    ls_no_ext = [f.split('.')[0] for f in ls]
    ls2 = os.listdir(anno_path + '/' + dir); ls2.sort()
    ls2_no_ext = [f.split('.')[0] for f in ls2]
    no = len(ls_no_ext)
    no2 = len(ls2_no_ext)
    diff = no2 - no
    if ls_no_ext == ls2_no_ext:
        print('Nothing to do for ' + dir)
    elif diff < 0:
        print('There are %d unannotated files in ' % (-diff) + dir)
        raise Exception
    else:
        dir_full = os.path.join(anno_path, dir)
        files = os.listdir(dir_full)

        for f in files:
            if f.split('.')[0] not in ls_no_ext:
                os.remove(os.path.join(dir_full, f))
        print('%d Redundant files deleted for ' % diff + dir)

# 30 Redundant files deleted for 0
# 20 Redundant files deleted for 1
# 13 Redundant files deleted for 10
# 7 Redundant files deleted for 11
# 8 Redundant files deleted for 12
# 12 Redundant files deleted for 13
# 15 Redundant files deleted for 14
# 4 Redundant files deleted for 15
# 12 Redundant files deleted for 16
# 13 Redundant files deleted for 17
# 4 Redundant files deleted for 18
# 9 Redundant files deleted for 19
# 17 Redundant files deleted for 2
# 12 Redundant files deleted for 20
# 15 Redundant files deleted for 21
# 7 Redundant files deleted for 22
# 9 Redundant files deleted for 23
# 4 Redundant files deleted for 24
# 6 Redundant files deleted for 25
# 18 Redundant files deleted for 26
# 9 Redundant files deleted for 27
# 13 Redundant files deleted for 28
# 11 Redundant files deleted for 29
# 26 Redundant files deleted for 3
# 16 Redundant files deleted for 30
# 17 Redundant files deleted for 31
# 16 Redundant files deleted for 32
# 4 Redundant files deleted for 33
# 19 Redundant files deleted for 34
# 15 Redundant files deleted for 35
# 15 Redundant files deleted for 36
# 15 Redundant files deleted for 37
# 13 Redundant files deleted for 38
# 21 Redundant files deleted for 39
# 15 Redundant files deleted for 4
# 26 Redundant files deleted for 40
# 103 Redundant files deleted for 41
# 9 Redundant files deleted for 42
# 18 Redundant files deleted for 43
# 19 Redundant files deleted for 44
# 9 Redundant files deleted for 45
# 6 Redundant files deleted for 5
# 21 Redundant files deleted for 6
# 21 Redundant files deleted for 7
# 15 Redundant files deleted for 8
# 30 Redundant files deleted for 9


###
# Nothing to do for 0
# Nothing to do for 1
# Nothing to do for 10
# There are 1 unannotated files in 11
# There are 2 unannotated files in 12
# Nothing to do for 13
# Nothing to do for 14
# Nothing to do for 15
# Nothing to do for 16
# Nothing to do for 17
# Nothing to do for 18
# Nothing to do for 19
# Nothing to do for 2
# Nothing to do for 20
# Nothing to do for 21
# Nothing to do for 22
# Nothing to do for 23
# Nothing to do for 24
# Nothing to do for 25
# Nothing to do for 26
# Nothing to do for 27
# Nothing to do for 28
# Nothing to do for 29
# Nothing to do for 3
# Nothing to do for 30
# Nothing to do for 31
# Nothing to do for 32
# Nothing to do for 33
# There are 1 unannotated files in 34
# Nothing to do for 35
# Nothing to do for 36
# Nothing to do for 37
# Nothing to do for 38
# There are 1 unannotated files in 39
# Nothing to do for 4
# Nothing to do for 40
# Nothing to do for 41
# Nothing to do for 42
# Nothing to do for 43
# Nothing to do for 44
# Nothing to do for 45
# Nothing to do for 5
# Nothing to do for 6
# Nothing to do for 7
# Nothing to do for 8
# Nothing to do for 9