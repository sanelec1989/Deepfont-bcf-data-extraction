# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 22:21:06 2021
"""
import struct
import os


'''
bcf file structure
<total_number_files><size_file1><size_file2>......<size_filen><file1_png><file2_png>.....<filen_png>
'''


bcf_file = open('E:/train.bcf', 'rb');

font_list = open('E:/fontlist.txt', 'rb');
fonts = font_list.readlines();
font_list.close()


output_image_dir = 'E:/deepfont-train-data/';

bcf_file.seek(0, os.SEEK_SET)
nb_images = struct.unpack('i', bcf_file.read(4))[0]
pngDataOffset = nb_images*8+8;

imageCount=0;
for i in range(len(fonts)):
    font = str(fonts[i].decode("utf-8").strip());
    outputDir = output_image_dir+font;
    if(not os.path.isdir(outputDir)):
        os.mkdir(outputDir)
    for n in range(1000):
        filePath = outputDir+'/'+font+'_'+str(n)+'.png'
        bcf_file.seek(imageCount*8+8, os.SEEK_SET)
        sizeFile = struct.unpack('i', bcf_file.read(4))[0];
        bcf_file.seek(pngDataOffset, os.SEEK_SET)
        imageCount=imageCount+1;
        pngDataOffset=pngDataOffset+sizeFile;
        pngRawData = bcf_file.read(sizeFile);
        fw = open(filePath,'wb');
        fw.write(pngRawData);
        fw.close();
    
