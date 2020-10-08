district_db = [[1, 2, 3, 4, 5, 6],
               [7, 8],
               [14, 15, 16],
               [9, 10],
               [11, 12, 13],
               [17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25, 26, 27],
               [28, 29, 30],
               [31, 32, 33],
               [34, 35, 36, 37],
               [38, 39, 40, 41],
               [42, 43, 44, 45],
               [46, 47, 48],
               [49, 50, 81],
               [51, 52],
               [53, 54, 55, 82],
               [56, 57],
               [58, 59],
               [60, 61, 62, 63, 64],
               [65, 66, 67, 68],
               [69, 70, 71],
               [72, 73],
               [77, 78],
               [75, 76],
               [79, 80]]
dist_count = [6, 2, 3, 2, 3, 1, 2, 2, 2, 4, 3, 3, 4, 4, 4, 3, 3, 2, 4, 2, 2, 5, 4, 3, 2, 2, 2, 2]

dbarray1k = [[1,2,3,4,5,6],[7,8],[14,15,16],[9,10],[11,12,13],[17],[18,19],[20,21],[22,23],[24,25,26,27],[28,29,30],[31,32,33],[34,35,36,37],[38,39,40,41],[42,43,44,45],[46,47,48],
           [49,50,81],[51,52],[53,54,55,82],[56,57],[58,59],[60,61,62,63,64],[65,66,67,68],[69,70,71],[72,73],[77,78],[75,76],[79,80]]
dbcounter1k = [6,2,3,2,3,1,2,2,2,4,3,3,4,4,4,3,3,2,4,2,2,5,4,3,2,2,2,2]

dbarray2k = [[6,7,15],[6,4],[4,5,10,9,6],[2,3,5],[3,4,10,21],[1,2,3,7],[1,6,8,9],[7,9,12],[3,7,8,10],[3,5,21,11,9],[20,21,10,12],[8,11,13],[12,20,19,14],[13,15,16],[1,14,16],[15,14,18,17],[16,18],[19,16,17],[18,28,20,13],[11,12,13,19,26,28],[5,10,11,23],[24,23,5],[22,24,25,21],[22,23],[23,27],[20,28,27],[25,26,28],[19,20,26]]
dbcounter2k = [3,2,5,3,4,4,4,3,4,5,4,3,4,3,3,4,2,3,4,6,4,3,4,2,2,3,3,3]

dbarray3k =[[6,7,15,2,14],[6,4,3,7,1],[4,5,10,9,6,8,7],[2,3,5,6,9,10],[3,4,10,21,2,6,9],[1,2,3,7,4,9],[1,6,8,9,10,3,11,12,14,13],[7,9,12,1,10,11,13,14,15],[3,7,8,10,1,6,11,12],[3,5,21,11,9,4,8],[20,21,10,12,9,8],[8,11,13,9,20,14],[12,20,19,14,8,11,15],[13,15,16,1,8,12],[1,14,16,7,8],[15,14,18,17,19],[16,18,15,14,19],[19,16,17,14],[18,28,20,13,14,16],[11,12,13,19,26,28,21],[5,10,11,23,22],[24,23,5,21],[22,24,25,21],[22,23,25],[23,27,24,26],[20,28,27,25],[25,26,28],[19,20,26,27]]
dbcounter3k = [5,5,7,6,7,6,10,9,8,7,6,6,7,6,5,5,5,4,6,7,5,4,4,3,4,4,3,4]


def postal1km(homepostal):
    ctrl1k = 0
    a = homepostal[:2]
    a = int(a)
    for i in range(0, 28):
        for j in range(0,dbcounter1k[i]):
            if a == dbarray1k[i][j]:
                ctrl1k = i

    return dbarray1k[ctrl1k]


def postal2km(homepostal):
    a = homepostal[:2]
    a = int(a)
    dbctrl = 0
    for i in range(0,27):
        for j in range(0, dist_count[i] - 1):
            if a == district_db[i][j]:
                dbctrl = i
    return dbarray2k[dbctrl]


def postal3km(homepostal):
    a = homepostal[:2]
    a = int(a)
    dbctrl = 0
    for i in range(0,27):
        for j in range(0, dist_count[i] - 1):
            if a == district_db[i][j]:
                dbctrl = i
    return dbarray3k[dbctrl]


def get_postal_code_within_km(postal_code, km):
    """
    Function to get the postal codes that are within the stated distance range from
    postal_code.
    :param postal_code: 6-digit Singapore postal code
    :param km: "1" for within 1 km from postal_code, "2" for within 2km and "3" for within 3km
    :return: List of numbers as strings. These are the first two digit of postal codes within km of postal_code
    """
    final_list = []
    if km == '1':
        final_list = postal1km(postal_code)
    elif km == '2':
        final_list = postal1km(postal_code) + postal2km(postal_code)    # 1km is common, uncommon radius add = 1 or 2 km depending on choice
    elif km == '3':
        final_list = postal1km(postal_code) + postal3km(postal_code)    # Output are list which needs to be checked against 1st 2 digits of postal code of chidlcare

    return [str(i) for i in final_list]