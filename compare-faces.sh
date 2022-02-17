#!/bin/bash 


person=$1
picture_resize=300


function create_thumbnails() {
	tb_exist=$(ls images/${person}/tb*|wc -l 2>/dev/null)
	if [ ${tb_exist} = "0" ]; 
	then 

		for pic in $(ls images/${person}/*.png); 
		do
			echo ">> Resizing ${pic}.......................OK"
			convert -resize ${picture_resize} ${pic} images/${person}/tb_$(basename ${pic})
		done
	fi
}

function compare_faces() {
	echo "Comparing faces for ${person}"
	echo "FOTO 1:"
	imgcat images/${person}/tb_foto1.png
	echo "FOTO 2:"
	imgcat images/${person}/tb_foto2.png
	python3 ./rekognition.py ${person}
	imgcat output.png
}

function cleanup() {
	rm output.png 2>/dev/null
}

create_thumbnails
compare_faces
cleanup
