def level(number):
    switcher = {
        9: "7級",
        8: "6強",
        7: "6弱",
        6: "5強",
        5: "5弱",
        4: "4級",
        3: "3級",
        2: "2級",
        1: "1級"
    }
    return switcher.get(number, "0級")
