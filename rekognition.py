#!/usr/bin/python3


import boto3
import cv2
import numpy as np
import sys
import json
from pygments import highlight, lexers, formatters



person = sys.argv[1]

def compare_faces(sourceFile, targetFile):

    client=boto3.client('rekognition')
   
    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response=client.compare_faces(SimilarityThreshold=80,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    # detect if we have a match
    if len(response['FaceMatches']) > 0:
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('>> The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + similarity + '% confidence')

        imageSource.close()
        imageTarget.close()     

        # print response in pretty json and color with pygments
        print(highlight(json.dumps(response, indent=4, sort_keys=True), lexers.JsonLexer(), formatters.TerminalFormatter()))

        # print(response)
        srcimg = cv2.imread(targetFile)
        # get image size
        width, heigth, channels = srcimg.shape
        imgWidth = (srcimg.shape[1])
        imgHeight = (srcimg.shape[0])

        # construct bounding box
        # print(position)
        (x, y, w, h) = position['Left'], position['Top'], position['Width'], position['Height']
        x = int(x * imgWidth)
        y = int(y * imgHeight)
        w = int(w * imgWidth)
        h = int(h * imgHeight)

        # draw bounding box
        cv2.rectangle(srcimg, (x, y), (x + w,y + h), (0, 255, 0), 1)

        # write name under bounding box
        cv2.putText(srcimg, similarity, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imwrite('output.png', srcimg)
        
        
        return len(response['FaceMatches'])

    else:
        return False

    

def main():
    source_file='images/'+ person + '/foto1.png'
    target_file='images/' + person + '/foto2.png'
    face_matches=compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))



if __name__ == "__main__":
    main()
