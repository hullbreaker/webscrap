volume = 'Volume: 59 issue: 4, page(s): 675-695'
print(volume[8:10])
print(volume[18])
page_num = volume.split(',')[1].replace(" page(s): ",'')
print(page_num)