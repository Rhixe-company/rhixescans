
# Args
# def add_variables(id, *args):
#    print(id, args)

# Kwargs
def add_variables(**kwargs):

    print(kwargs['name'])


def home():
    # add_variables("35619", "Living in an Abandoned Bus", "廃バスに住む", "https://avt.mkklcdnv6temp.com/28/q/22-1603039713.jpg",
    #              "Ichihi", "Slice of life", "Sep 21,2022 - 02:58", "364.3K", "Updating")
    info = {
        "id": "35562",
        "name": "Sennetsu",
        "nameother": "潜熱",
        "image": "https://avt.mkklcdnv6temp.com/26/j/22-1602063150.jpg",
        "author": "Noda Ayako",
        "genres": "Josei, Romance",
        "updatetime": "Sep 21,2022 - 02:58",
        "view": "260.2K",
        "description": "Ruri, a college student working part time at a convenience story, finds herself drawn to Nosegawa, a middle-aged customer who comes in every day to buy two packs of cigarettes. When she works up the nerve to ask him for a ride home one rainy day, their interaction in the car kindles something in Ruri's heart - a strange and unknown new heat..."
    }
    # add_variables(**info)
    add_variables(name='Sennetsu', nameother='潜熱')


home()
