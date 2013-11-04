rm -rf ./atlas
rm -rf ./QA
rm -rf ./movement

rm -rf ./*.conc
rm -rf ./*.glm
rm -rf ./*.lst
rm -rf ./*.vars
rm -rf ./*.csh
rm -rf ./*.rec

rm -rf ./run1
rm -rf ./run2
rm -rf ./run3
rm -rf ./run4
rm -rf ./run5

mv raw/MRCTR/* .

mv axial_ACPC_128x128.4/ study1
mv cor-t1-loc_128x128.3/ study2
mv localizer_512x512.1/ study3
mv mprage_512x416.6/ study4
mv functional_448x448.7/ study5
mv functional_448x448.9/ study6
mv functional_448x448.11/ study7
mv functional_448x448.13/ study8
mv sag-t1-loc_256x256.2/ study9
mv t2_tse_tra_1024_p2_1024x1024.5/ study10

mv *.fidl ../fidl
